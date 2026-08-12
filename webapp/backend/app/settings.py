"""
One place for every knob, read from the environment once at import.

Why a settings module rather than constants scattered across modules: the values
that must change between a laptop and a server -- database path, allowed
origins, cookie flags, execution limits, which sandbox to use -- were previously
hardcoded in five files. Rolling out meant editing code, and editing code to
deploy is how a `Secure` cookie flag ends up disabled in production.

Everything is prefixed `FORGE_`. Nothing here reads a file, so a container only
needs environment variables.

The one opinionated rule: **production refuses to boot with an unsandboxed
executor** unless you say so explicitly. That is not a style preference -- the
runner executes arbitrary submitted Python, and the difference between
`ENV=dev` and `ENV=prod` should not be the difference between "my laptop" and
"anyone can read my files".
"""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def _load_dotenv() -> None:
    """
    Read `backend/.env` into the environment, if it exists.

    Shipping a `.env.example` while nothing read `.env` was a trap: the file
    looked like configuration and was silently ignored, so a setting you thought
    you had changed had not changed at all.

    Real environment variables win over the file. That ordering matters -- a
    container or systemd unit setting `FORGE_DB_PATH` must not be overridden by a
    stale `.env` that happens to be in the image.
    """
    # Tests must not read the developer's .env: a suite whose result depends on
    # an untracked local file is not a suite you can trust.
    if os.environ.get("FORGE_SKIP_DOTENV"):
        return
    path = Path(__file__).resolve().parents[1] / ".env"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip one layer of matching quotes, so `X="a b"` means `a b`.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


class ConfigError(RuntimeError):
    """Raised at import time for a configuration that cannot be honoured."""


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(f"FORGE_{name}")
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def _flag(name: str, default: bool) -> bool:
    raw = _env(name)
    if raw is None:
        return default
    low = raw.lower()
    if low in _TRUE:
        return True
    if low in _FALSE:
        return False
    raise ConfigError(f"FORGE_{name} must be a boolean, got {raw!r}")


def _int(name: str, default: int, minimum: Optional[int] = None,
         maximum: Optional[int] = None) -> int:
    raw = _env(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ConfigError(f"FORGE_{name} must be an integer, got {raw!r}")
    if minimum is not None and value < minimum:
        raise ConfigError(f"FORGE_{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ConfigError(f"FORGE_{name} must be <= {maximum}")
    return value


def _float(name: str, default: float, minimum: float = 0.0) -> float:
    raw = _env(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError:
        raise ConfigError(f"FORGE_{name} must be a number, got {raw!r}")
    if value < minimum:
        raise ConfigError(f"FORGE_{name} must be >= {minimum}")
    return value


def _csv(name: str, default: List[str]) -> List[str]:
    raw = _env(name)
    if raw is None:
        return list(default)
    return [part.strip() for part in raw.split(",") if part.strip()]


# webapp/backend/app/settings.py -> repo root is four levels up
REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[1]

LOCAL_ORIGIN_PATTERN = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"


@dataclass(frozen=True)
class Settings:
    # ---------------------------------------------------------- environment
    env: str                         # "dev" | "prod"
    debug: bool

    # ---------------------------------------------------------------- store
    db_path: Path
    db_timeout: float                # seconds to wait on a locked database
    db_busy_retries: int
    wal: bool

    # ------------------------------------------------------------- sessions
    session_days: int
    cookie_name: str
    cookie_samesite: str
    cookie_secure: Optional[bool]    # None = decide per request
    cookie_domain: Optional[str]

    # -------------------------------------------------------------- hashing
    scrypt_n: int

    # --------------------------------------------------------- rate limiting
    rate_window_seconds: int
    rate_max_attempts: int

    # ----------------------------------------------------------------- http
    allowed_origins: List[str]
    allowed_origin_regex: Optional[str]
    max_body_bytes: int
    trust_proxy_headers: bool

    # ------------------------------------------------------------ execution
    executor: str                    # "auto" | "local" | "seatbelt" | "docker"
    allow_unsafe_executor: bool
    exec_wall_seconds: float
    exec_cpu_seconds: int
    exec_memory_mb: int
    exec_max_source_bytes: int
    #: How much of a run's output is kept. 8 KB silently cut the worked examples
    #: in half (topic 22 prints 16 KB), and a demo that stops mid-sentence is
    #: worse than no demo.
    exec_max_stdout_bytes: int
    exec_max_concurrent: int
    docker_image: str
    docker_binary: str
    docker_pids_limit: int

    # -------------------------------------------------------------- logging
    log_level: str
    log_json: bool
    log_requests: bool

    # ----------------------------------------------------------- curriculum
    python_root: Path
    #: Where course directories live. Each contains a course.json manifest, so a
    #: second course is a directory rather than a code change.
    courses_root: Path

    # Filled in by resolve_executor() once the platform is known.
    resolved_executor: str = field(default="", compare=False)

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"

    def cookie_secure_for(self, scheme: str, host: str) -> bool:
        """
        Should the session cookie carry `Secure`?

        Explicit setting wins. Otherwise: yes, unless this is plain-http
        localhost -- hardcoding False would ship a cleartext cookie, and
        hardcoding True would break local development.
        """
        if self.cookie_secure is not None:
            return self.cookie_secure
        if scheme == "https":
            return True
        return (host or "").lower() not in ("localhost", "127.0.0.1", "::1", "")


def _load() -> Settings:
    env = (_env("ENV", "dev") or "dev").lower()
    if env not in ("dev", "prod"):
        raise ConfigError(f"FORGE_ENV must be 'dev' or 'prod', got {env!r}")

    samesite = (_env("COOKIE_SAMESITE", "lax") or "lax").lower()
    if samesite not in ("lax", "strict", "none"):
        raise ConfigError("FORGE_COOKIE_SAMESITE must be lax, strict or none")
    if samesite == "none" and _env("COOKIE_SECURE", "").lower() in _FALSE:
        # Browsers ignore SameSite=None without Secure, which would silently
        # mean "no CSRF protection at all".
        raise ConfigError("SameSite=none requires FORGE_COOKIE_SECURE=true")

    secure_raw = _env("COOKIE_SECURE")
    cookie_secure: Optional[bool]
    if secure_raw is None or secure_raw.lower() == "auto":
        cookie_secure = None
    else:
        cookie_secure = _flag("COOKIE_SECURE", True)

    executor = (_env("EXECUTOR", "auto") or "auto").lower()
    if executor not in ("auto", "local", "seatbelt", "docker"):
        raise ConfigError("FORGE_EXECUTOR must be auto, local, seatbelt or docker")

    origins = _csv("ALLOWED_ORIGINS", [])
    origin_regex = _env("ALLOWED_ORIGIN_REGEX")
    if not origins and origin_regex is None:
        if env == "prod":
            raise ConfigError(
                "production needs FORGE_ALLOWED_ORIGINS (or "
                "FORGE_ALLOWED_ORIGIN_REGEX) -- defaulting to localhost would "
                "either break the deployment or, if widened, allow any origin")
        origin_regex = LOCAL_ORIGIN_PATTERN

    default_db = BACKEND_ROOT / "data" / "forge.db"

    return Settings(
        env=env,
        debug=_flag("DEBUG", env == "dev"),

        db_path=Path(_env("DB_PATH", str(default_db))).expanduser(),
        db_timeout=_float("DB_TIMEOUT", 10.0, minimum=0.1),
        db_busy_retries=_int("DB_BUSY_RETRIES", 4, minimum=0, maximum=20),
        wal=_flag("DB_WAL", True),

        session_days=_int("SESSION_DAYS", 30, minimum=1, maximum=400),
        cookie_name=_env("COOKIE_NAME", "forge_session") or "forge_session",
        cookie_samesite=samesite,
        cookie_secure=cookie_secure,
        cookie_domain=_env("COOKIE_DOMAIN"),

        # 2^15 is ~50 ms here. Lowered only for tests, where 30-odd password
        # hashes would otherwise dominate the run.
        scrypt_n=_int("SCRYPT_N", 2 ** 15, minimum=2 ** 10),

        rate_window_seconds=_int("RATE_WINDOW_SECONDS", 15 * 60, minimum=1),
        rate_max_attempts=_int("RATE_MAX_ATTEMPTS", 8, minimum=1),

        allowed_origins=origins,
        allowed_origin_regex=origin_regex,
        max_body_bytes=_int("MAX_BODY_BYTES", 1_000_000, minimum=1024),
        trust_proxy_headers=_flag("TRUST_PROXY_HEADERS", False),

        executor=executor,
        allow_unsafe_executor=_flag("ALLOW_UNSAFE_EXECUTOR", False),
        exec_wall_seconds=_float("EXEC_WALL_SECONDS", 10.0, minimum=0.5),
        exec_cpu_seconds=_int("EXEC_CPU_SECONDS", 5, minimum=1),
        exec_memory_mb=_int("EXEC_MEMORY_MB", 512, minimum=32),
        exec_max_source_bytes=_int("EXEC_MAX_SOURCE_BYTES", 200_000, minimum=256),
        exec_max_stdout_bytes=_int("EXEC_MAX_STDOUT_BYTES", 65_536, minimum=1024),
        exec_max_concurrent=_int("EXEC_MAX_CONCURRENT", 4, minimum=1, maximum=64),
        docker_image=_env("DOCKER_IMAGE", "forge-runner:latest") or "forge-runner:latest",
        docker_binary=_env("DOCKER_BINARY", "docker") or "docker",
        docker_pids_limit=_int("DOCKER_PIDS_LIMIT", 64, minimum=8),

        log_level=(_env("LOG_LEVEL", "INFO") or "INFO").upper(),
        log_json=_flag("LOG_JSON", env == "prod"),
        log_requests=_flag("LOG_REQUESTS", True),

        python_root=Path(_env("PYTHON_ROOT", str(REPO_ROOT / "python"))),
        courses_root=Path(_env("COURSES_ROOT", str(REPO_ROOT))),
    )


settings = _load()


def reload_settings() -> Settings:
    """Re-read the environment. Used by tests, never in a running server."""
    global settings
    settings = _load()
    return settings


# ---------------------------------------------------------------- executor

#: Executors that are safe to expose to untrusted code. `local` is not one of
#: them: it runs submitted Python as the server user with full filesystem access.
SAFE_EXECUTORS = {"docker", "seatbelt"}


def resolve_executor(available: Optional[dict] = None) -> str:
    """
    Turn `FORGE_EXECUTOR` into the executor actually in use.

    `auto` prefers the strongest option the host can provide. The result is
    logged at startup and reported by /api/health, because "which sandbox am I
    actually running?" must never be a guess.
    """
    from .executors import availability

    have = available if available is not None else availability()
    wanted = settings.executor

    if wanted != "auto":
        if not have.get(wanted, False):
            raise ConfigError(
                f"FORGE_EXECUTOR={wanted} is not usable on this host: "
                f"{have.get(wanted + '_reason', 'unavailable')}")
        return wanted

    for candidate in ("docker", "seatbelt"):
        if have.get(candidate):
            return candidate
    return "local"


def check_safety(resolved: str) -> None:
    """
    Refuse to serve untrusted code from an unsandboxed runner in production.

    A deployment that silently downgraded to `local` because the Docker socket
    was missing would look healthy and be wide open, so this is fatal rather
    than a warning.
    """
    if resolved in SAFE_EXECUTORS:
        return
    if not settings.is_prod:
        return
    if settings.allow_unsafe_executor:
        return
    raise ConfigError(
        f"refusing to start: FORGE_ENV=prod with the {resolved!r} executor, "
        f"which runs submitted code with this process's own filesystem access. "
        f"Set FORGE_EXECUTOR=docker (with a reachable daemon and the runner "
        f"image built), or set FORGE_ALLOW_UNSAFE_EXECUTOR=1 if you genuinely "
        f"accept that risk.")


def warnings_for(resolved: str) -> List[str]:
    """
    Configuration that is legal but probably a mistake.

    Logged at startup and returned by /api/health. `trust_proxy_headers` is the
    important one: with no proxy in front, `X-Forwarded-For` is attacker
    controlled, so trusting it turns the login rate limit into a formality --
    rotating the header per attempt never trips it.
    """
    out: List[str] = []
    if settings.trust_proxy_headers:
        out.append(
            "FORGE_TRUST_PROXY_HEADERS=1: X-Forwarded-For is trusted. Only "
            "correct behind a proxy that OVERWRITES that header -- otherwise "
            "the login rate limit can be bypassed by rotating it.")
    if resolved not in SAFE_EXECUTORS:
        out.append(
            f"the {resolved!r} executor runs submitted code with this "
            f"process's own filesystem access; it is not a sandbox.")
    if settings.is_prod and settings.debug:
        out.append("FORGE_DEBUG is on in production: error responses will "
                   "include exception text.")
    return out


def summary() -> dict:
    """Non-secret configuration, for logs and /api/health."""
    return {
        "env": settings.env,
        "executor": settings.resolved_executor or settings.executor,
        "dbPath": str(settings.db_path),
        "sessionDays": settings.session_days,
        "cookieSameSite": settings.cookie_samesite,
        "cookieSecure": "auto" if settings.cookie_secure is None
                        else settings.cookie_secure,
        "allowedOrigins": settings.allowed_origins or None,
        "allowedOriginRegex": settings.allowed_origin_regex,
        "execLimits": {
            "wallSeconds": settings.exec_wall_seconds,
            "cpuSeconds": settings.exec_cpu_seconds,
            "memoryMb": settings.exec_memory_mb,
            "maxSourceBytes": settings.exec_max_source_bytes,
            "maxStdoutBytes": settings.exec_max_stdout_bytes,
            "maxConcurrent": settings.exec_max_concurrent,
        },
        "coursesRoot": str(settings.courses_root),
        "python": sys.version.split()[0],
        "platform": platform.system(),
    }
