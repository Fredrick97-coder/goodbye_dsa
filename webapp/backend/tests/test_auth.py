"""
Authentication, as properties rather than as a walkthrough.

Each test names the guarantee it protects, because the point of these is to fail
if someone later "simplifies" one of them away.
"""

from __future__ import annotations

import time

import pytest


# ------------------------------------------------------------- hashing

def test_password_round_trips_and_rejects_the_wrong_one(env):
    from app import auth
    stored = auth.hash_password("correct horse")
    assert auth.verify_password("correct horse", stored)
    assert not auth.verify_password("Correct horse", stored)
    assert not auth.verify_password("", stored)


def test_hash_is_salted(env):
    """Two identical passwords must not produce the same hash."""
    from app import auth
    assert auth.hash_password("same") != auth.hash_password("same")


def test_hash_records_its_parameters(env):
    from app import auth
    stored = auth.hash_password("pw")
    assert stored.startswith("scrypt$")
    n, r, p = stored.split("$")[1:4]
    assert (int(n), int(r), int(p)) == (env.settings.scrypt_n, 8, 1)


def test_production_uses_a_memory_hard_parameter(monkeypatch, tmp_path):
    """Tests lower this for speed; the default must stay expensive."""
    import importlib
    import sys
    monkeypatch.delenv("FORGE_SCRYPT_N", raising=False)
    monkeypatch.setenv("FORGE_DB_PATH", str(tmp_path / "d.db"))
    for name in [n for n in list(sys.modules) if n.startswith("app")]:
        del sys.modules[name]
    from app import settings as config
    importlib.reload(config)
    assert config.settings.scrypt_n >= 2 ** 15


def test_a_weaker_stored_hash_is_flagged_for_upgrade(env):
    from app import auth
    assert auth.needs_rehash(_hash_with_n("pw", 1024))
    assert not auth.needs_rehash(auth.hash_password("pw"))


def test_garbage_hashes_are_rejected_not_crashed_on(env):
    from app import auth
    for bad in ("", "nonsense", "scrypt$x$8$1$aa$bb", "scrypt$16384$8$1$zz$yy"):
        assert auth.verify_password("pw", bad) is False


def _hash_with_n(password: str, n: int) -> str:
    """
    A genuine hash at a chosen cost, for testing the upgrade path.

    Rewriting the parameter in an existing hash string does not work: the digest
    was computed with the other parameter, so it would simply fail to verify --
    which is what makes the stored parameters trustworthy in the first place.
    """
    import hashlib
    import secrets
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=n, r=8, p=1,
                            dklen=32, maxmem=128 * 1024 * 1024)
    return f"scrypt${n}$8$1${salt.hex()}${digest.hex()}"


def test_login_rehashes_an_outdated_password(database, env):
    from app import auth, store
    old = _hash_with_n("pw", 1024)
    assert auth.verify_password("pw", old)      # still valid, just weaker
    assert auth.needs_rehash(old)
    store.create_user("u1", "a@b.co", "A", old)
    user, reason = auth.authenticate("a@b.co", "pw")
    assert user is not None and reason == "ok"
    assert not auth.needs_rehash(store.user_by_id("u1")["password_hash"])


# ------------------------------------------------------------ validation

def test_email_is_normalised_and_validated(env):
    from app import auth
    assert auth.clean_email("  Ada@Example.COM ") == "ada@example.com"
    for bad in ("", "no-at-sign", "a@b", "a b@c.co", "a@@b.co", "x" * 250 + "@b.co"):
        with pytest.raises(Exception):
            auth.clean_email(bad)


def test_password_length_bounds(env):
    from app import auth
    with pytest.raises(Exception):
        auth.check_password("short")
    with pytest.raises(Exception):
        auth.check_password("x" * 500)
    assert auth.check_password("x" * 8) == "x" * 8


def test_name_defaults_to_the_email_local_part(env):
    from app import auth
    assert auth.clean_name(None, "ada@example.com") == "ada"
    assert auth.clean_name("   ", "ada@example.com") == "ada"
    assert auth.clean_name("A" * 200, "ada@example.com") == "A" * 60


# --------------------------------------------------------------- sessions

def test_session_token_is_stored_only_as_a_hash(database):
    from app import auth, store
    store.create_user("u1", "a@b.co", "A", "hash")

    class FakeRequest:
        headers = {"user-agent": "pytest"}
    token = auth.new_session("u1", FakeRequest())

    row = database.query_one("SELECT token_hash FROM sessions")
    assert token not in row["token_hash"]
    assert row["token_hash"] == auth.token_hash(token)
    assert store.session_user(auth.token_hash(token))["id"] == "u1"


def test_expired_sessions_do_not_resolve(database):
    from app import auth, store
    store.create_user("u1", "a@b.co", "A", "hash")
    # Inserted directly: create_session prunes expired rows as it writes, so
    # asking it to create an already-expired one deletes it again immediately.
    database.execute(
        "INSERT INTO sessions (token_hash, user_id, created_at, touched_at, "
        "expires_at, user_agent) VALUES (?,?,?,?,?,'')",
        (auth.token_hash("t"), "u1", 0.0, 0.0, 1.0))
    assert store.session_user(auth.token_hash("t")) is None
    assert store.purge_expired_sessions() == 1
    assert store.purge_expired_sessions() == 0


def test_creating_a_session_prunes_expired_ones(database):
    from app import auth, store
    store.create_user("u1", "a@b.co", "A", "hash")
    database.execute(
        "INSERT INTO sessions (token_hash, user_id, created_at, touched_at, "
        "expires_at, user_agent) VALUES (?,?,?,?,?,'')",
        (auth.token_hash("stale"), "u1", 0.0, 0.0, 1.0))
    store.create_session(auth.token_hash("fresh"), "u1", ttl_seconds=3600)
    rows = database.query_all("SELECT token_hash FROM sessions")
    assert [r["token_hash"] for r in rows] == [auth.token_hash("fresh")]


def test_uniform_failure_for_unknown_email_and_wrong_password(database):
    from app import auth, store
    store.create_user("u1", "a@b.co", "A", auth.hash_password("right pw"))
    unknown, r1 = auth.authenticate("nobody@example.com", "right pw")
    wrong, r2 = auth.authenticate("a@b.co", "wrong pw")
    assert unknown is None and wrong is None
    # The reasons differ internally (for logs) but both are failures, and the
    # route turns both into the same message -- see test_api.
    assert r1 != r2


def test_unknown_email_still_pays_the_hashing_cost(database):
    """
    Timing must not reveal whether an account exists.

    Measured, not assumed: the unknown-email path calls the same KDF against a
    dummy hash. A generous factor keeps this from flaking on a busy machine
    while still catching an early `return None`.
    """
    from app import auth, store
    store.create_user("u1", "a@b.co", "A", auth.hash_password("right pw"))

    def timed(email):
        best = None
        for _ in range(3):
            t0 = time.perf_counter()
            auth.authenticate(email, "some password")
            elapsed = time.perf_counter() - t0
            best = elapsed if best is None else min(best, elapsed)
        return best

    known = timed("a@b.co")
    unknown = timed("nobody@example.com")
    assert unknown > known / 4, (
        f"unknown-email path is suspiciously fast: {unknown*1000:.1f}ms "
        f"vs {known*1000:.1f}ms -- account enumeration by timing")


# ---------------------------------------------------------- rate limiting

def test_rate_limit_counts_per_client_and_bucket(database, env):
    from app import auth

    class Req:
        def __init__(self, ip): self.client = type("C", (), {"host": ip})()
        headers: dict = {}

    a, b = Req("1.1.1.1"), Req("2.2.2.2")
    for _ in range(env.settings.rate_max_attempts):
        auth.record_failure(a, "login")

    with pytest.raises(Exception) as exc:
        auth.rate_limit(a, "login")
    assert "too many attempts" in str(exc.value)

    auth.rate_limit(b, "login")             # a different client is unaffected
    auth.rate_limit(a, "register")          # a different bucket is unaffected

    auth.clear_failures(a, "login")
    auth.rate_limit(a, "login")             # cleared on success


def test_rate_limit_survives_a_restart(database, env):
    """
    The in-process version reset when the server restarted, which made the
    limit a formality. It is a table now.
    """
    from app import auth, db

    class Req:
        client = type("C", (), {"host": "9.9.9.9"})()
        headers: dict = {}

    for _ in range(env.settings.rate_max_attempts):
        auth.record_failure(Req(), "login")
    db.close_all()                          # simulate a process restart
    db.init()
    with pytest.raises(Exception):
        auth.rate_limit(Req(), "login")


def test_forwarded_headers_are_ignored_unless_trusted(database, env):
    from app import auth

    class Req:
        client = type("C", (), {"host": "10.0.0.1"})()
        headers = {"x-forwarded-for": "1.2.3.4, 5.6.7.8"}

    assert auth.client_ip(Req()) == "10.0.0.1"      # spoofable, so ignored


def test_forwarded_headers_are_used_when_trusted(monkeypatch, tmp_path):
    import importlib
    import sys
    monkeypatch.setenv("FORGE_DB_PATH", str(tmp_path / "d.db"))
    monkeypatch.setenv("FORGE_TRUST_PROXY_HEADERS", "1")
    monkeypatch.setenv("FORGE_SCRYPT_N", str(2 ** 12))
    for name in [n for n in list(sys.modules) if n.startswith("app")]:
        del sys.modules[name]
    from app import settings as config
    importlib.reload(config)
    from app import auth

    class Req:
        client = type("C", (), {"host": "10.0.0.1"})()
        headers = {"x-forwarded-for": "1.2.3.4, 5.6.7.8"}

    assert auth.client_ip(Req()) == "1.2.3.4"       # leftmost = real client


# --------------------------------------------------------------- origins

def test_origin_allowlist(env):
    from app import auth
    assert auth.origin_allowed("http://localhost:5173")
    assert auth.origin_allowed("http://127.0.0.1:8000")
    assert not auth.origin_allowed("https://evil.example")
    assert not auth.origin_allowed("http://localhost.evil.example")
