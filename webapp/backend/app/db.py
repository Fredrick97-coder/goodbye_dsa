"""
Connection handling, pragmas, retries, transactions, and schema migrations.

SQLite is a real database and will serve a real rollout, but only if it is
configured for concurrency rather than left on its defaults. Four things matter,
and all four were missing before:

1. **WAL.** In the default rollback journal a reader blocks a writer and a
   writer blocks readers. Under WAL, readers never block and one writer proceeds
   alongside them -- which is exactly the shape of this workload (many reads of
   the problem list, occasional writes on submit).

2. **busy_timeout.** Without it, a write that collides with another gets an
   instant `database is locked`. With it, SQLite waits. This is set as a pragma
   *and* as the connect timeout, because the two cover different paths.

3. **Retry on lock.** `busy_timeout` cannot help when the conflict is
   `SQLITE_BUSY_SNAPSHOT` on a write transaction, so genuinely contended writes
   are retried with backoff.

4. **foreign_keys.** Off by default in SQLite, per connection. Without it,
   `ON DELETE CASCADE` is decoration -- deleting a user would silently orphan
   their submissions.

One connection per thread, kept in a thread-local. FastAPI runs sync endpoints
in a bounded threadpool, so this is a small pool that costs nothing to maintain
and avoids reopening the file on every query.

**On moving to Postgres:** everything SQLite-specific lives in this module --
`connect()`, the pragmas, the retry predicate, and the migration runner's use of
`user_version`. `store.py` above it only issues queries and never touches a
pragma or a driver detail.
"""

from __future__ import annotations

import logging
import random
import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Any, Callable, Iterator, List, Optional, Tuple

from .settings import settings

log = logging.getLogger("forge.db")

_local = threading.local()
_init_lock = threading.Lock()
_initialised = False


# ---------------------------------------------------------------- backends

#: Which engine is in use. Decided once, from the configuration.
DIALECT = "postgres" if settings.database_url else "sqlite"

_local = threading.local()
_init_lock = threading.Lock()
_pool = None                       # psycopg_pool.ConnectionPool, when Postgres


class _Sqlite:
    """
    The original backend, unchanged in behaviour.

    One connection per thread, kept in a thread-local: FastAPI runs sync
    endpoints in a bounded threadpool, so this is a small pool that costs
    nothing and avoids reopening the file per query.
    """

    name = "sqlite"
    placeholder = "?"

    def integrity_errors(self):
        return (sqlite3.IntegrityError,)

    def connect(self):
        conn = getattr(_local, "conn", None)
        if conn is not None:
            return conn
        settings.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(
            settings.db_path,
            timeout=settings.db_timeout,
            isolation_level=None,        # explicit transactions, see transaction()
            check_same_thread=True,      # one connection per thread, enforced
        )
        conn.row_factory = sqlite3.Row
        conn.execute(f"PRAGMA busy_timeout = {int(settings.db_timeout * 1000)}")
        conn.execute("PRAGMA foreign_keys = ON")
        if settings.wal:
            conn.execute("PRAGMA journal_mode = WAL")
            # NORMAL is the right pairing with WAL: a crash can lose the last
            # transactions but the database is never corrupted, and it removes
            # an fsync from every commit.
            conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA temp_store = MEMORY")
        _local.conn = conn
        return conn

    def release(self, conn) -> None:
        """Nothing to do: the connection lives for the thread's lifetime."""

    def close_thread(self) -> None:
        conn = getattr(_local, "conn", None)
        if conn is not None:
            conn.close()
            _local.conn = None

    def is_retryable(self, exc) -> bool:
        if not isinstance(exc, sqlite3.OperationalError):
            return False
        message = str(exc).lower()
        return any(f in message for f in
                   ("database is locked", "database table is locked",
                    "database schema is locked"))

    def begin(self, conn) -> None:
        # IMMEDIATE takes the write lock up front. Deferred transactions take it
        # on the first write, which is where SQLite's upgrade deadlock comes
        # from: two readers that both later try to write.
        conn.execute("BEGIN IMMEDIATE")

    def in_transaction(self, conn) -> bool:
        return bool(conn.in_transaction)

    def script(self, conn, sql: str) -> None:
        conn.executescript(sql)

    def read_version(self, conn) -> int:
        row = conn.execute("PRAGMA user_version").fetchone()
        return int(row[0]) if row else 0

    def write_version(self, conn, version: int) -> None:
        # Not parameterisable: PRAGMA takes a literal. The value is an int from
        # our own migration list, never user input.
        conn.execute(f"PRAGMA user_version = {int(version)}")

    def before_migration(self, conn):
        # Foreign keys must be off while migration 2 rebuilds tables, or the
        # DROP would cascade the rows away. This is the documented procedure.
        had = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        conn.execute("PRAGMA foreign_keys = OFF")
        return had

    def after_migration(self, conn, saved) -> None:
        broken = conn.execute("PRAGMA foreign_key_check").fetchall()
        if saved:
            conn.execute("PRAGMA foreign_keys = ON")
        if broken:
            raise RuntimeError(f"migration left {len(broken)} broken references")

    def stats(self, conn) -> Dict[str, Any]:
        page_size = conn.execute("PRAGMA page_size").fetchone()[0]
        page_count = conn.execute("PRAGMA page_count").fetchone()[0]
        return {
            "sizeBytes": page_size * page_count,
            "journalMode": conn.execute("PRAGMA journal_mode").fetchone()[0],
        }


class _Postgres:
    """
    The Postgres backend, for when one writer at a time stops being enough.

    A pooled connection is checked out per operation rather than pinned to a
    thread: a thread that held one for its lifetime would exhaust the pool as
    soon as there were more request threads than connections.
    """

    name = "postgres"
    placeholder = "%s"

    def __init__(self) -> None:
        import psycopg                                    # noqa: F401
        self._psycopg = psycopg

    def integrity_errors(self):
        return (self._psycopg.errors.IntegrityError,)

    def _ensure_pool(self):
        global _pool
        if _pool is None:
            from psycopg.rows import dict_row
            from psycopg_pool import ConnectionPool
            _pool = ConnectionPool(
                settings.database_url,
                min_size=settings.db_pool_min,
                max_size=settings.db_pool_max,
                timeout=settings.db_timeout,
                kwargs={"row_factory": dict_row, "autocommit": True},
                open=True,
            )
            _pool.wait(timeout=10)
        return _pool

    def connect(self):
        conn = getattr(_local, "conn", None)
        if conn is not None:
            return conn
        conn = self._ensure_pool().getconn()
        _local.conn = conn
        _local.borrowed = True
        return conn

    def release(self, conn) -> None:
        if getattr(_local, "borrowed", False):
            _local.conn = None
            _local.borrowed = False
            self._ensure_pool().putconn(conn)

    def close_thread(self) -> None:
        conn = getattr(_local, "conn", None)
        if conn is not None:
            self.release(conn)

    def is_retryable(self, exc) -> bool:
        # Deadlocks and serialization failures are the retryable ones; a unique
        # violation is not, and retrying it would just fail again.
        return isinstance(exc, (self._psycopg.errors.DeadlockDetected,
                                self._psycopg.errors.SerializationFailure))

    def begin(self, conn) -> None:
        conn.execute("BEGIN")

    def in_transaction(self, conn) -> bool:
        status = conn.info.transaction_status
        return status != self._psycopg.pq.TransactionStatus.IDLE

    def script(self, conn, sql: str) -> None:
        # psycopg sends a statement with no parameters through the simple query
        # protocol, which accepts several separated by semicolons.
        conn.execute(sql)

    def read_version(self, conn) -> int:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_version ("
                     "  version INTEGER NOT NULL)")
        row = conn.execute("SELECT version FROM schema_version "
                           "ORDER BY version DESC LIMIT 1").fetchone()
        return int(row["version"]) if row else 0

    def write_version(self, conn, version: int) -> None:
        conn.execute("DELETE FROM schema_version")
        conn.execute("INSERT INTO schema_version (version) VALUES (%s)",
                     (int(version),))

    def before_migration(self, conn):
        return None

    def after_migration(self, conn, saved) -> None:
        """Nothing: Postgres enforces its constraints during the migration."""

    def stats(self, conn) -> Dict[str, Any]:
        row = conn.execute(
            "SELECT pg_database_size(current_database()) AS bytes").fetchone()
        return {"sizeBytes": int(row["bytes"]), "journalMode": "wal"}


def _make_backend():
    if DIALECT == "postgres":
        return _Postgres()
    return _Sqlite()


backend = _make_backend()

#: `except db.IntegrityError` works whichever engine is underneath.
IntegrityError = backend.integrity_errors()


# ------------------------------------------------------------- connections

def connect():
    """A configured connection for the calling thread."""
    return backend.connect()


def close_thread_connection() -> None:
    backend.close_thread()


def close_all() -> None:
    """Shutdown. Closes this thread's connection and any pool."""
    global _pool
    backend.close_thread()
    if _pool is not None:
        _pool.close()
        _pool = None


# ---------------------------------------------------------- SQL portability

def translate(sql: str) -> str:
    """
    Rewrite `?` placeholders for the active driver.

    Queries are written once, in SQLite's style, and adapted here rather than
    duplicated per engine. Quoted literals are skipped, so a `?` inside a string
    is left alone -- a naive replace would corrupt any query containing one.
    """
    if backend.placeholder == "?":
        return sql
    out = []
    quote = None
    for ch in sql:
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
            continue
        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
        elif ch == "?":
            out.append(backend.placeholder)
        elif ch == "%":
            out.append("%%")          # a literal % must survive the driver
        else:
            out.append(ch)
    return "".join(out)


class _Cursorish:
    """
    Thin wrapper so both drivers answer `.execute(...).fetchall()` the same way.

    sqlite3 returns a cursor from `Connection.execute`; psycopg returns one too,
    but expects `%s` placeholders. Translating in one place keeps every call site
    engine-agnostic.
    """

    __slots__ = ("_conn",)

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, args=()):
        return self._conn.execute(translate(sql), tuple(args))

    def executescript(self, sql):
        return backend.script(self._conn, sql)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def wrap(conn):
    return _Cursorish(conn)


# ------------------------------------------------------------- retry + tx

def with_retry(fn: Callable[[], Any], what: str = "query") -> Any:
    """
    Run `fn`, retrying briefly on a contention error.

    Jittered backoff, because two writers retrying on the same schedule collide
    again on the same schedule.
    """
    attempts = settings.db_busy_retries + 1
    delay = 0.02
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:                            # noqa: BLE001
            if attempt == attempts or not backend.is_retryable(exc):
                raise
            sleep_for = delay * (2 ** (attempt - 1)) * (0.5 + random.random())
            log.warning("%s busy on %s, retry %d/%d in %.0f ms",
                        backend.name, what, attempt, attempts - 1,
                        sleep_for * 1000)
            time.sleep(sleep_for)
    raise AssertionError("unreachable")


@contextmanager
def transaction(immediate: bool = True) -> Iterator[Any]:
    """
    An explicit transaction that commits on success and rolls back on error.

    Nested use joins the outer transaction rather than committing early, so a
    helper that opens one inside another does not release the lock halfway.
    """
    raw = connect()
    if backend.in_transaction(raw):
        yield wrap(raw)
        return
    backend.begin(raw)
    try:
        yield wrap(raw)
    except BaseException:
        raw.rollback()
        raise
    else:
        raw.commit()
    finally:
        backend.release(raw)


@contextmanager
def reading() -> Iterator[Any]:
    """A connection for reads. No transaction, no write lock."""
    raw = connect()
    try:
        yield wrap(raw)
    finally:
        backend.release(raw)


def query_all(sql: str, args: Tuple = ()) -> List[Any]:
    def run():
        with reading() as conn:
            return conn.execute(sql, args).fetchall()
    return with_retry(run, sql[:40])


def query_one(sql: str, args: Tuple = ()) -> Optional[Any]:
    def run():
        with reading() as conn:
            return conn.execute(sql, args).fetchone()
    return with_retry(run, sql[:40])


def execute(sql: str, args: Tuple = ()):
    def run():
        with transaction() as conn:
            return conn.execute(sql, args)
    return with_retry(run, sql[:40])


# ------------------------------------------------------------- migrations

#: Forward-only migrations, applied in order. Each entry is
#: (version, description, script), where `script` is either one SQL string used
#: by both backends, or a {dialect: sql} mapping where they must differ.
#:
#: The version is recorded in `PRAGMA user_version` on SQLite (stored in the
#: file header, so it cannot drift from the schema it describes) and in a
#: `schema_version` table on Postgres, which has no equivalent.
#:
#: Rules for adding one: append, never edit a shipped migration, and keep each
#: script idempotent enough to be safe if a previous run half-applied it. Both
#: engines have transactional DDL, so a failure rolls the whole step back.
#:
#: **`REAL` is not portable.** Every timestamp here is epoch seconds, which
#: needs ten significant digits; Postgres `REAL` is a 4-byte float with about
#: seven, so it would round `created_at` to the nearest ~30 seconds. The
#: Postgres variants use `double precision` throughout.
MIGRATIONS: List[Tuple[int, str, Any]] = [
    (1, "users, sessions, submissions, bookmarks, notes", {
        "sqlite": """
        CREATE TABLE IF NOT EXISTS users (
            id            TEXT PRIMARY KEY,
            email         TEXT NOT NULL,
            name          TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    REAL NOT NULL,
            last_login_at REAL
        );
        CREATE UNIQUE INDEX IF NOT EXISTS ux_users_email ON users (email);

        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at REAL NOT NULL,
            touched_at REAL NOT NULL,
            expires_at REAL NOT NULL,
            user_agent TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS ix_sessions_user ON sessions (user_id);
        CREATE INDEX IF NOT EXISTS ix_sessions_expiry ON sessions (expires_at);

        CREATE TABLE IF NOT EXISTS submissions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    TEXT NOT NULL,
            problem_id TEXT NOT NULL,
            language   TEXT NOT NULL,
            source     TEXT NOT NULL,
            verdict    TEXT NOT NULL,
            passed     INTEGER NOT NULL,
            total      INTEGER NOT NULL,
            elapsed_ms REAL NOT NULL,
            created_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_sub_user_problem
            ON submissions (user_id, problem_id, id DESC);
        CREATE INDEX IF NOT EXISTS ix_sub_user_time
            ON submissions (user_id, created_at);

        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id    TEXT NOT NULL,
            problem_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );

        CREATE TABLE IF NOT EXISTS notes (
            user_id    TEXT NOT NULL,
            problem_id TEXT NOT NULL,
            body       TEXT NOT NULL,
            updated_at REAL NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );
    """,
        "postgres": """
        -- Postgres gets the final shape in one step: it has no need for the
        -- table rebuild that migration 2 performs on SQLite, because a
        -- constraint can simply be declared here.
        CREATE TABLE IF NOT EXISTS users (
            id            TEXT PRIMARY KEY,
            email         TEXT NOT NULL,
            name          TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    DOUBLE PRECISION NOT NULL,
            last_login_at DOUBLE PRECISION
        );
        CREATE UNIQUE INDEX IF NOT EXISTS ux_users_email ON users (email);

        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at DOUBLE PRECISION NOT NULL,
            touched_at DOUBLE PRECISION NOT NULL,
            expires_at DOUBLE PRECISION NOT NULL,
            user_agent TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS ix_sessions_user ON sessions (user_id);
        CREATE INDEX IF NOT EXISTS ix_sessions_expiry ON sessions (expires_at);

        CREATE TABLE IF NOT EXISTS submissions (
            id         BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            language   TEXT NOT NULL,
            source     TEXT NOT NULL,
            verdict    TEXT NOT NULL,
            passed     INTEGER NOT NULL,
            total      INTEGER NOT NULL,
            elapsed_ms DOUBLE PRECISION NOT NULL,
            created_at DOUBLE PRECISION NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_sub_user_problem
            ON submissions (user_id, problem_id, id DESC);
        CREATE INDEX IF NOT EXISTS ix_sub_user_time
            ON submissions (user_id, created_at);
        CREATE INDEX IF NOT EXISTS ix_sub_user_verdict
            ON submissions (user_id, verdict);

        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            created_at DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );

        CREATE TABLE IF NOT EXISTS notes (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            body       TEXT NOT NULL,
            updated_at DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );
    """,
    }),

    (2, "cascade deletes and referential integrity for user-owned rows", {
        "sqlite": """
        -- v1 created these tables without foreign keys (submissions predates
        -- accounts entirely), so deleting a user left their rows behind. SQLite
        -- cannot ALTER a table to add a constraint, so the table is rebuilt --
        -- the standard 12-step procedure, minus the parts a transaction covers.
        CREATE TABLE submissions_new (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            language   TEXT NOT NULL,
            source     TEXT NOT NULL,
            verdict    TEXT NOT NULL,
            passed     INTEGER NOT NULL,
            total      INTEGER NOT NULL,
            elapsed_ms REAL NOT NULL,
            created_at REAL NOT NULL
        );
        INSERT INTO submissions_new
            SELECT s.id, s.user_id, s.problem_id, s.language, s.source,
                   s.verdict, s.passed, s.total, s.elapsed_ms, s.created_at
            FROM submissions s
            WHERE EXISTS (SELECT 1 FROM users u WHERE u.id = s.user_id);
        DROP TABLE submissions;
        ALTER TABLE submissions_new RENAME TO submissions;
        CREATE INDEX ix_sub_user_problem
            ON submissions (user_id, problem_id, id DESC);
        CREATE INDEX ix_sub_user_time
            ON submissions (user_id, created_at);
        CREATE INDEX ix_sub_user_verdict
            ON submissions (user_id, verdict);

        CREATE TABLE bookmarks_new (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            created_at REAL NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );
        INSERT INTO bookmarks_new
            SELECT b.user_id, b.problem_id, b.created_at FROM bookmarks b
            WHERE EXISTS (SELECT 1 FROM users u WHERE u.id = b.user_id);
        DROP TABLE bookmarks;
        ALTER TABLE bookmarks_new RENAME TO bookmarks;

        CREATE TABLE notes_new (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id TEXT NOT NULL,
            body       TEXT NOT NULL,
            updated_at REAL NOT NULL,
            PRIMARY KEY (user_id, problem_id)
        );
        INSERT INTO notes_new
            SELECT n.user_id, n.problem_id, n.body, n.updated_at FROM notes n
            WHERE EXISTS (SELECT 1 FROM users u WHERE u.id = n.user_id);
        DROP TABLE notes;
        ALTER TABLE notes_new RENAME TO notes;
    """,
        "postgres": """
        -- Nothing to do. Migration 2 exists because SQLite cannot ALTER a table
        -- to add a foreign key, so the SQLite path rebuilds three tables; the
        -- Postgres path declared the constraints in migration 1. The version
        -- number is still consumed so both backends agree on what "v2" means.
        SELECT 1;
    """,
    }),

    (3, "durable rate limiting, so a restart is not a way around the limit", {
        "sqlite": """
        CREATE TABLE IF NOT EXISTS auth_attempts (
            bucket     TEXT NOT NULL,
            client     TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_attempts_lookup
            ON auth_attempts (bucket, client, created_at);
    """,
        "postgres": """
        CREATE TABLE IF NOT EXISTS auth_attempts (
            bucket     TEXT NOT NULL,
            client     TEXT NOT NULL,
            created_at DOUBLE PRECISION NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_attempts_lookup
            ON auth_attempts (bucket, client, created_at);
    """,
    }),

    (4, "per-account preferences (chosen language, and whatever comes next)", {
        "sqlite": """
        -- Key/value rather than a column per setting: the next preference is
        -- then a whitelist entry in code, not a schema migration and a
        -- deployment. Values are TEXT and validated on the way in; there are
        -- few enough settings that typing them in SQL buys nothing.
        CREATE TABLE IF NOT EXISTS preferences (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            key        TEXT NOT NULL,
            value      TEXT NOT NULL,
            updated_at REAL NOT NULL,
            PRIMARY KEY (user_id, key)
        );
    """,
        "postgres": """
        -- Key/value rather than a column per setting: the next preference is
        -- then a whitelist entry in code, not a schema migration and a
        -- deployment. Values are TEXT and validated on the way in; there are
        -- few enough settings that typing them in SQL buys nothing.
        CREATE TABLE IF NOT EXISTS preferences (
            user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            key        TEXT NOT NULL,
            value      TEXT NOT NULL,
            updated_at DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (user_id, key)
        );
    """,
    }),

    (5, "lesson progress, so reading is tracked as well as solving", {
        "sqlite": """
        -- Content itself stays in files; this is the only thing a learner's
        -- reading adds to the database. `lesson_id` is "<module>/<slug>", a
        -- slug rather than a position, so inserting a section does not shift
        -- every id and silently reset progress.
        CREATE TABLE IF NOT EXISTS lesson_progress (
            user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            course_id    TEXT NOT NULL,
            lesson_id    TEXT NOT NULL,
            completed_at REAL NOT NULL,
            PRIMARY KEY (user_id, course_id, lesson_id)
        );
        CREATE INDEX IF NOT EXISTS ix_lesson_progress_user
            ON lesson_progress (user_id, course_id, completed_at);
    """,
        "postgres": """
        -- Content itself stays in files; this is the only thing a learner's
        -- reading adds to the database. `lesson_id` is "<module>/<slug>", a
        -- slug rather than a position, so inserting a section does not shift
        -- every id and silently reset progress.
        CREATE TABLE IF NOT EXISTS lesson_progress (
            user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            course_id    TEXT NOT NULL,
            lesson_id    TEXT NOT NULL,
            completed_at DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (user_id, course_id, lesson_id)
        );
        CREATE INDEX IF NOT EXISTS ix_lesson_progress_user
            ON lesson_progress (user_id, course_id, completed_at);
    """,
    }),

    (6, "explicit module unlocks, so progression is never a dead end", {
        "sqlite": """
        -- Records a learner choosing to skip ahead. Without this the gate has no
        -- escape hatch, and one Hard problem could wall someone out of the rest
        -- of the course.
        CREATE TABLE IF NOT EXISTS module_unlocks (
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            course_id   TEXT NOT NULL,
            module_id   TEXT NOT NULL,
            unlocked_at REAL NOT NULL,
            reason      TEXT NOT NULL DEFAULT 'skipped',
            PRIMARY KEY (user_id, course_id, module_id)
        );
    """,
        "postgres": """
        -- Records a learner choosing to skip ahead. Without this the gate has no
        -- escape hatch, and one Hard problem could wall someone out of the rest
        -- of the course.
        CREATE TABLE IF NOT EXISTS module_unlocks (
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            course_id   TEXT NOT NULL,
            module_id   TEXT NOT NULL,
            unlocked_at DOUBLE PRECISION NOT NULL,
            reason      TEXT NOT NULL DEFAULT 'skipped',
            PRIMARY KEY (user_id, course_id, module_id)
        );
    """,
    }),

    (7, "per-problem unlocks, for the sequential problem chain", {
        "sqlite": """
        -- The chain is strictly linear, so being stuck on one problem blocks
        -- every problem after it. This is the per-problem escape hatch; without
        -- it, one Hard problem walls off the rest of the course.
        CREATE TABLE IF NOT EXISTS problem_unlocks (
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id  TEXT NOT NULL,
            unlocked_at REAL NOT NULL,
            reason      TEXT NOT NULL DEFAULT 'skipped',
            PRIMARY KEY (user_id, problem_id)
        );
    """,
        "postgres": """
        CREATE TABLE IF NOT EXISTS problem_unlocks (
            user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id  TEXT NOT NULL,
            unlocked_at DOUBLE PRECISION NOT NULL,
            reason      TEXT NOT NULL DEFAULT 'skipped',
            PRIMARY KEY (user_id, problem_id)
        );
    """,
    }),
]

SCHEMA_VERSION = max(version for version, _, _ in MIGRATIONS)


def script_for(entry, dialect: str = "") -> str:
    """The SQL for this dialect: one string for both, or a per-dialect map."""
    _, _, script = entry
    if isinstance(script, str):
        return script
    return script[dialect or DIALECT]


def current_version() -> int:
    with reading() as conn:
        return backend.read_version(conn._conn)


def migrate(target: Optional[int] = None) -> List[int]:
    """
    Apply every migration above the recorded version. Returns what it applied.

    Each runs inside its own transaction, and the version is bumped in the same
    transaction -- so a failure leaves the database at the last version that
    fully succeeded, never halfway through one. Both engines have transactional
    DDL, which is what makes that true.
    """
    goal = SCHEMA_VERSION if target is None else target
    applied: List[int] = []
    for entry in MIGRATIONS:
        version, description, _ = entry
        if version <= current_version() or version > goal:
            continue
        log.info("applying migration %d: %s (%s)", version, description,
                 backend.name)
        started = time.perf_counter()
        raw = connect()
        saved = backend.before_migration(raw)
        try:
            with transaction() as tx:
                tx.executescript(script_for(entry))
                backend.write_version(tx._conn, version)
            backend.after_migration(raw, saved)
        finally:
            backend.release(raw)
        applied.append(version)
        log.info("migration %d applied in %.0f ms", version,
                 (time.perf_counter() - started) * 1000)
    return applied


def init() -> None:
    """Open the database and bring the schema up to date. Idempotent."""
    with _init_lock:
        migrate()


def healthy() -> Tuple[bool, str]:
    """A real check: can we read, and is the schema the one this code expects?"""
    try:
        with reading() as conn:
            conn.execute("SELECT 1").fetchone()
    except Exception as exc:                                # noqa: BLE001
        return False, f"unreadable: {type(exc).__name__}: {exc}"
    version = current_version()
    if version != SCHEMA_VERSION:
        return False, f"schema is v{version}, code expects v{SCHEMA_VERSION}"
    return True, "ok"


def stats() -> dict:
    """Size and row counts, for /api/health and for spotting runaway growth."""
    counts = {}
    with reading() as conn:
        engine = backend.stats(conn._conn)
        for table in ("users", "sessions", "submissions", "bookmarks", "notes",
                      "preferences", "lesson_progress", "module_unlocks"):
            try:
                row = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()
                counts[table] = int(row["n"])
            except Exception:                               # noqa: BLE001
                counts[table] = None
    return {
        "backend": backend.name,
        "schemaVersion": current_version(),
        "expectedVersion": SCHEMA_VERSION,
        **engine,
        "rows": counts,
    }


def vacuum() -> None:
    """Reclaim space. Must run outside a transaction, hence its own path."""
    raw = connect()
    try:
        if backend.name == "postgres":
            raw.execute("VACUUM")
        else:
            raw.execute("VACUUM")
    finally:
        backend.release(raw)


def backup(destination) -> None:
    """
    A consistent copy while the server is running.

    SQLite uses its online backup API rather than a file copy: `cp` on a WAL
    database can capture a torn state, because the newest committed data lives
    in the `-wal` file. Postgres has its own tooling and this deliberately does
    not reimplement it badly -- `pg_dump` is the answer, and the message says so
    instead of writing a half-correct dump.
    """
    if backend.name == "postgres":
        raise RuntimeError(
            "use pg_dump for Postgres backups, e.g.\n"
            "  pg_dump --no-owner --format=custom "
            "$FORGE_DATABASE_URL > forge.dump")
    from pathlib import Path
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    dest = sqlite3.connect(target)
    try:
        connect().backup(dest)
    finally:
        dest.close()
