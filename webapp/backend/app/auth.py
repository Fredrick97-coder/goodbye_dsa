"""
Password hashing, sessions, and the request dependencies that use them.

Design choices, and why:

* **scrypt from the standard library**, not a new dependency. It is a real
  memory-hard KDF (n=2^15, so 32 MB and ~50 ms per verification), which is what
  makes a stolen database expensive to attack. A bare SHA-256 would be worse
  than useless here.

* **Opaque server-side sessions**, not JWTs. A random token in an HttpOnly
  cookie, stored hashed. This gives real logout and real "sign out everywhere"
  -- a self-contained JWT cannot be revoked before it expires without keeping a
  server-side blocklist, at which point it has become a session with extra
  steps.

* **The cookie is HttpOnly and SameSite=Lax**, so page JavaScript can never read
  the token and a cross-site form POST never carries it. `Secure` is set
  whenever the request is not plain-http localhost, so it is correct the moment
  this is served over TLS without needing a config flag.

* **Uniform failure.** Login says "email or password is incorrect" whichever was
  wrong, and an unknown email still pays the full hashing cost, so response
  timing does not reveal which accounts exist.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import time
from typing import Any, Dict, Optional, Tuple

from fastapi import Depends, HTTPException, Request, Response, status

from . import store

# --------------------------------------------------------------- passwords

_SCRYPT_N = 2 ** 15          # 32 MB, ~50 ms -- see the module docstring
_SCRYPT_R = 8
_SCRYPT_P = 1
_DKLEN = 32
_MAXMEM = 128 * 1024 * 1024

# The parameters live in the stored string, so they can be raised later without
# invalidating existing passwords -- verify reads whatever each hash was made
# with, and `needs_rehash` reports the stale ones.
_HASH_RE = re.compile(r"^scrypt\$(\d+)\$(\d+)\$(\d+)\$([0-9a-f]+)\$([0-9a-f]+)$")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=_SCRYPT_N,
                            r=_SCRYPT_R, p=_SCRYPT_P, dklen=_DKLEN,
                            maxmem=_MAXMEM)
    return (f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}"
            f"${salt.hex()}${digest.hex()}")


def verify_password(password: str, stored: str) -> bool:
    match = _HASH_RE.match(stored or "")
    if not match:
        return False
    n, r, p = int(match.group(1)), int(match.group(2)), int(match.group(3))
    salt = bytes.fromhex(match.group(4))
    expected = bytes.fromhex(match.group(5))
    try:
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r,
                                p=p, dklen=len(expected), maxmem=_MAXMEM)
    except ValueError:
        return False
    # Constant-time: a short-circuiting == would leak how much of the hash
    # matched, one byte at a time.
    return hmac.compare_digest(actual, expected)


def needs_rehash(stored: str) -> bool:
    match = _HASH_RE.match(stored or "")
    if not match:
        return True
    return (int(match.group(1)) < _SCRYPT_N or int(match.group(2)) != _SCRYPT_R
            or int(match.group(3)) != _SCRYPT_P)


# A real hash of a throwaway password. Verifying against this on an unknown
# email costs exactly what a real verification costs, so login timing does not
# answer "does this account exist?".
_DUMMY_HASH = hash_password(secrets.token_urlsafe(16))


def waste_time() -> None:
    verify_password("not the password", _DUMMY_HASH)


# -------------------------------------------------------------- validation

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")
MIN_PASSWORD = 8
MAX_PASSWORD = 200           # scrypt cost is independent of length, but an
                             # unbounded field is still a free CPU sink
MAX_EMAIL = 254
MAX_NAME = 60


def clean_email(raw: str) -> str:
    """Lowercased and trimmed, which is also how it is stored and compared."""
    email = (raw or "").strip().lower()
    if len(email) > MAX_EMAIL or not _EMAIL_RE.match(email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "that does not look like an email address")
    return email


def check_password(password: str) -> str:
    if not isinstance(password, str) or len(password) < MIN_PASSWORD:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"password must be at least {MIN_PASSWORD} characters")
    if len(password) > MAX_PASSWORD:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            f"password must be under {MAX_PASSWORD} characters")
    return password


def clean_name(raw: Optional[str], email: str) -> str:
    name = (raw or "").strip()
    if not name:
        name = email.split("@")[0]
    return name[:MAX_NAME]


# ------------------------------------------------------------ rate limiting

_WINDOW = 15 * 60            # seconds
_MAX_ATTEMPTS = 8            # per key, per window
_attempts: Dict[str, list] = {}


def _prune(key: str, now: float) -> list:
    kept = [t for t in _attempts.get(key, []) if now - t < _WINDOW]
    if kept:
        _attempts[key] = kept
    else:
        _attempts.pop(key, None)
    return kept


def rate_limit(request: Request, bucket: str) -> None:
    """
    Throttle repeated failures per client per bucket.

    In-process, so it resets when the server restarts -- which is honest for a
    single-process local tool and still stops an online guessing loop. Moving
    this to the database is the change to make if this ever runs multi-worker.
    """
    now = time.time()
    client = request.client.host if request.client else "unknown"
    key = f"{bucket}:{client}"
    recent = _prune(key, now)
    if len(recent) >= _MAX_ATTEMPTS:
        wait = int(_WINDOW - (now - recent[0])) // 60 + 1
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            f"too many attempts -- try again in about {wait} minute"
            f"{'s' if wait != 1 else ''}")


def record_failure(request: Request, bucket: str) -> None:
    now = time.time()
    client = request.client.host if request.client else "unknown"
    key = f"{bucket}:{client}"
    _attempts.setdefault(key, []).append(now)


def clear_failures(request: Request, bucket: str) -> None:
    client = request.client.host if request.client else "unknown"
    _attempts.pop(f"{bucket}:{client}", None)


# ---------------------------------------------------------------- sessions

COOKIE_NAME = "forge_session"
SESSION_DAYS = 30
_RENEW_AFTER = 24 * 3600     # only touch the row once a day, not per request


def new_session(user_id: str, request: Request) -> str:
    """Create a session and return the raw token (stored only as a hash)."""
    token = secrets.token_urlsafe(32)
    agent = (request.headers.get("user-agent") or "")[:200]
    store.create_session(token_hash(token), user_id,
                         ttl_seconds=SESSION_DAYS * 86400, user_agent=agent)
    return token


def token_hash(token: str) -> str:
    """
    SHA-256 is right here, unlike for passwords.

    A session token is 32 random bytes, so there is no guessable input to grind
    -- the reason to hash it at all is that a leaked database should not hand
    over live sessions.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def set_session_cookie(response: Response, token: str, request: Request) -> None:
    response.set_cookie(
        COOKIE_NAME, token,
        max_age=SESSION_DAYS * 86400,
        httponly=True,
        samesite="lax",
        secure=_is_secure(request),
        path="/",
    )


def clear_session_cookie(response: Response, request: Request) -> None:
    response.delete_cookie(COOKIE_NAME, path="/",
                           httponly=True, samesite="lax",
                           secure=_is_secure(request))


def _is_secure(request: Request) -> bool:
    """
    Set `Secure` unless this is plain-http local development.

    Hardcoding False would silently allow the cookie over cleartext in
    production; hardcoding True would break http://localhost.
    """
    if request.url.scheme == "https":
        return True
    host = (request.url.hostname or "").lower()
    return host not in ("localhost", "127.0.0.1", "::1", "")


# ------------------------------------------------------------ dependencies

def current_user_optional(request: Request) -> Optional[Dict[str, Any]]:
    """The signed-in user, or None. Never raises -- for public endpoints."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    row = store.session_user(token_hash(token))
    if row is None:
        return None
    # Sliding expiry, so an active user is not logged out mid-session, but the
    # write is throttled to once a day to keep reads cheap.
    if time.time() - row["session_touched"] > _RENEW_AFTER:
        store.touch_session(token_hash(token), SESSION_DAYS * 86400)
    return row


def current_user(
    user: Optional[Dict[str, Any]] = Depends(current_user_optional),
) -> Dict[str, Any]:
    """The signed-in user, or a 401. For everything that touches user data."""
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "sign in to do that")
    return user


def user_id_of(user: Dict[str, Any]) -> str:
    return user["id"]


def public_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Only the fields the browser is allowed to see -- never the hash."""
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "createdAt": user["created_at"],
    }


# ------------------------------------------------------------- CSRF guard

_ALLOWED_ORIGIN = re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$")


def check_origin(request: Request) -> None:
    """
    Reject cross-site state-changing requests.

    SameSite=Lax already stops the cookie riding along on a cross-site POST;
    this is the belt to that braces, and it costs one header comparison. A
    missing Origin is allowed so command-line clients still work -- browsers
    always send it on cross-origin POSTs, which is the case that matters.
    """
    origin = request.headers.get("origin")
    if origin and not _ALLOWED_ORIGIN.match(origin):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "cross-origin request refused")


def authenticate(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Check a credential pair.

    Returns (user, reason). `reason` is for logs only -- the caller sends the
    same message either way so the response cannot be used to enumerate
    accounts.
    """
    row = store.user_by_email(email)
    if row is None:
        waste_time()
        return None, "no such email"
    if not verify_password(password, row["password_hash"]):
        return None, "wrong password"
    if needs_rehash(row["password_hash"]):
        store.set_password(row["id"], hash_password(password))
    return row, "ok"
