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


# ------------------------------------------------------------- connections

def _configure(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    conn.execute(f"PRAGMA busy_timeout = {int(settings.db_timeout * 1000)}")
    conn.execute("PRAGMA foreign_keys = ON")
    if settings.wal:
        conn.execute("PRAGMA journal_mode = WAL")
        # NORMAL is the right pairing with WAL: a crash can lose the last
        # transactions but the database is never corrupted, and it removes an
        # fsync from every commit.
        conn.execute("PRAGMA synchronous = NORMAL")
    # Keep temp tables and sort scratch in memory rather than on disk.
    conn.execute("PRAGMA temp_store = MEMORY")


def connect() -> sqlite3.Connection:
    """A configured connection for the calling thread."""
    conn: Optional[sqlite3.Connection] = getattr(_local, "conn", None)
    if conn is not None:
        return conn
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(
        settings.db_path,
        timeout=settings.db_timeout,
        isolation_level=None,        # explicit transactions, see transaction()
        check_same_thread=True,      # one connection per thread, enforced
    )
    _configure(conn)
    _local.conn = conn
    return conn


def close_thread_connection() -> None:
    conn: Optional[sqlite3.Connection] = getattr(_local, "conn", None)
    if conn is not None:
        conn.close()
        _local.conn = None


def close_all() -> None:
    """Best effort on shutdown; only reaches the calling thread's connection."""
    close_thread_connection()


# ------------------------------------------------------------- retry + tx

_RETRYABLE = ("database is locked", "database table is locked",
              "database schema is locked")


def _is_retryable(exc: sqlite3.OperationalError) -> bool:
    message = str(exc).lower()
    return any(fragment in message for fragment in _RETRYABLE)


def with_retry(fn: Callable[[], Any], what: str = "query") -> Any:
    """
    Run `fn`, retrying briefly if SQLite reports a lock.

    Jittered backoff, because two writers retrying on the same schedule collide
    again on the same schedule.
    """
    attempts = settings.db_busy_retries + 1
    delay = 0.02
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except sqlite3.OperationalError as exc:
            if attempt == attempts or not _is_retryable(exc):
                raise
            sleep_for = delay * (2 ** (attempt - 1)) * (0.5 + random.random())
            log.warning("sqlite busy on %s, retry %d/%d in %.0f ms",
                        what, attempt, attempts - 1, sleep_for * 1000)
            time.sleep(sleep_for)
    raise AssertionError("unreachable")


@contextmanager
def transaction(immediate: bool = True) -> Iterator[sqlite3.Connection]:
    """
    An explicit transaction that commits on success and rolls back on error.

    `BEGIN IMMEDIATE` takes the write lock up front. Deferred transactions take
    it on the first write, which is where SQLite's upgrade deadlock comes from:
    two readers that both later try to write. Since every caller here intends to
    write, taking it immediately turns a possible deadlock into a short wait.
    """
    conn = connect()
    if conn.in_transaction:
        # Nested use joins the outer transaction rather than committing early.
        yield conn
        return
    conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
    try:
        yield conn
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()


@contextmanager
def reading() -> Iterator[sqlite3.Connection]:
    """A plain connection for reads. No transaction, no write lock."""
    yield connect()


def query_all(sql: str, args: Tuple = ()) -> List[sqlite3.Row]:
    return with_retry(lambda: connect().execute(sql, args).fetchall(), sql[:40])


def query_one(sql: str, args: Tuple = ()) -> Optional[sqlite3.Row]:
    return with_retry(lambda: connect().execute(sql, args).fetchone(), sql[:40])


def execute(sql: str, args: Tuple = ()) -> sqlite3.Cursor:
    def run() -> sqlite3.Cursor:
        with transaction() as conn:
            return conn.execute(sql, args)
    return with_retry(run, sql[:40])


# ------------------------------------------------------------- migrations

#: Forward-only migrations, applied in order. Each entry is
#: (version, description, SQL script). The version recorded in the database is
#: `PRAGMA user_version`, which SQLite stores in the file header -- no bespoke
#: table, and it is impossible to get out of step with the schema it describes.
#:
#: Rules for adding one: append, never edit a shipped migration, and keep each
#: script idempotent enough to be safe if a previous run half-applied it (the
#: runner wraps each in a transaction, so on SQLite that is mostly free -- DDL
#: is transactional here, unlike some other engines).
MIGRATIONS: List[Tuple[int, str, str]] = [
    (1, "users, sessions, submissions, bookmarks, notes", """
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
    """),

    (2, "cascade deletes and referential integrity for user-owned rows", """
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
    """),

    (3, "durable rate limiting, so a restart is not a way around the limit", """
        CREATE TABLE IF NOT EXISTS auth_attempts (
            bucket     TEXT NOT NULL,
            client     TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_attempts_lookup
            ON auth_attempts (bucket, client, created_at);
    """),

    (4, "per-account preferences (chosen language, and whatever comes next)", """
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
    """),

    (5, "lesson progress, so reading is tracked as well as solving", """
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
    """),
]

SCHEMA_VERSION = max(version for version, _, _ in MIGRATIONS)


def current_version() -> int:
    row = connect().execute("PRAGMA user_version").fetchone()
    return int(row[0]) if row else 0


def migrate(target: Optional[int] = None) -> List[int]:
    """
    Apply every migration above the recorded version. Returns what it applied.

    Each runs inside its own transaction, and `user_version` is bumped in the
    same transaction -- so a failure leaves the database at the last version
    that fully succeeded, never halfway through one.
    """
    goal = SCHEMA_VERSION if target is None else target
    conn = connect()
    applied: List[int] = []
    for version, description, script in MIGRATIONS:
        if version <= current_version() or version > goal:
            continue
        log.info("applying migration %d: %s", version, description)
        started = time.perf_counter()
        # Foreign keys must be off while tables are rebuilt, or the DROP in
        # migration 2 would cascade rows away. This is the documented procedure.
        had_fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        conn.execute("PRAGMA foreign_keys = OFF")
        try:
            with transaction() as tx:
                tx.executescript(script)
                tx.execute(f"PRAGMA user_version = {version}")
            check = conn.execute("PRAGMA foreign_key_check").fetchall()
            if check:
                raise RuntimeError(
                    f"migration {version} left {len(check)} broken references")
        finally:
            if had_fk:
                conn.execute("PRAGMA foreign_keys = ON")
        applied.append(version)
        log.info("migration %d applied in %.0f ms", version,
                 (time.perf_counter() - started) * 1000)
    return applied


def init() -> None:
    """Open the database and bring the schema up to date. Idempotent."""
    global _initialised
    with _init_lock:
        connect()
        migrate()
        _initialised = True


def healthy() -> Tuple[bool, str]:
    """A real check: can we read, and is the schema the one this code expects?"""
    try:
        connect().execute("SELECT 1").fetchone()
    except Exception as exc:                                # noqa: BLE001
        return False, f"unreadable: {type(exc).__name__}: {exc}"
    version = current_version()
    if version != SCHEMA_VERSION:
        return False, f"schema is v{version}, code expects v{SCHEMA_VERSION}"
    return True, "ok"


def stats() -> dict:
    """Size and row counts, for /api/health and for spotting runaway growth."""
    conn = connect()
    page_size = conn.execute("PRAGMA page_size").fetchone()[0]
    page_count = conn.execute("PRAGMA page_count").fetchone()[0]
    counts = {}
    for table in ("users", "sessions", "submissions", "bookmarks", "notes"):
        try:
            counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        except sqlite3.Error:
            counts[table] = None
    return {
        "schemaVersion": current_version(),
        "expectedVersion": SCHEMA_VERSION,
        "sizeBytes": page_size * page_count,
        "journalMode": conn.execute("PRAGMA journal_mode").fetchone()[0],
        "rows": counts,
    }


def vacuum() -> None:
    """Reclaim space. Must run outside a transaction, hence its own path."""
    connect().execute("VACUUM")


def backup(destination) -> None:
    """
    A consistent copy while the server is running.

    `sqlite3`'s online backup API, not a file copy -- copying a WAL database
    with `cp` can capture a torn state, because the newest committed data is in
    the -wal file that `cp` may not include.
    """
    from pathlib import Path
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    dest = sqlite3.connect(target)
    try:
        connect().backup(dest)
    finally:
        dest.close()
