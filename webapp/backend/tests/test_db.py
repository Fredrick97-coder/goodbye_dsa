"""The storage layer: migrations, pragmas, constraints, transactions, backup."""

from __future__ import annotations

import sqlite3
import threading

import os

import pytest

#: Some behaviour is engine-specific and should be asserted on that engine only
#: -- but skipping must be visible, so it states which engine it needs.
sqlite_only = pytest.mark.skipif(
    bool(os.environ.get("FORGE_TEST_DATABASE_URL")),
    reason="asserts SQLite internals; the suite is running on Postgres")
postgres_only = pytest.mark.skipif(
    not os.environ.get("FORGE_TEST_DATABASE_URL"),
    reason="needs FORGE_TEST_DATABASE_URL")


def test_migrations_run_to_head_and_are_idempotent(database):
    assert database.current_version() == database.SCHEMA_VERSION
    # Running again applies nothing -- the guard every deployment relies on.
    assert database.migrate() == []


def test_the_schema_version_is_recorded(database):
    """Portable: however each engine stores it, the runner agrees with it."""
    assert database.current_version() == database.SCHEMA_VERSION
    assert database.healthy() == (True, "ok")


@sqlite_only
def test_migration_is_recorded_in_the_file_not_a_table(database):
    """user_version lives in the header, so it cannot drift from the schema."""
    version = database.connect().execute("PRAGMA user_version").fetchone()[0]
    assert version == database.SCHEMA_VERSION


@sqlite_only
def test_pragmas_are_actually_set(database):
    conn = database.connect()
    assert conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert conn.execute("PRAGMA busy_timeout").fetchone()[0] > 0


def test_foreign_keys_cascade(database):
    from app import store
    store.create_user("u1", "a@b.co", "A", "hash")
    store.record_submission("u1", "01-01", "python", "src",
                            {"verdict": "accepted", "passed": 1, "total": 1}, 1.0)
    store.toggle_bookmark("01-01", "u1")
    store.save_note("01-01", "note", "u1")

    assert store.delete_user("u1") is True
    assert store.submissions("u1") == []
    assert store.bookmarks("u1") == []
    assert store.note("01-01", "u1")["body"] == ""


def test_orphan_rows_cannot_be_inserted(database):
    """
    Without the foreign key being enforced, this would silently succeed.

    `db.IntegrityError` is the portable name: sqlite3 and psycopg raise
    different classes, and pinning the test to one of them would have made it a
    SQLite test wearing a portable coat.
    """
    from app import store
    with pytest.raises(database.IntegrityError):
        store.record_submission("ghost", "01-01", "python", "src",
                                {"verdict": "accepted", "passed": 1,
                                 "total": 1}, 1.0)


def test_unique_email_is_enforced_by_the_index(database):
    from app import store
    store.create_user("u1", "dup@example.com", "A", "hash")
    with pytest.raises(store.EmailTaken):
        store.create_user("u2", "dup@example.com", "B", "hash")


def test_transaction_rolls_back_on_error(database):
    from app import store
    store.create_user("u1", "a@b.co", "A", "hash")
    with pytest.raises(RuntimeError):
        with database.transaction() as conn:
            conn.execute("UPDATE users SET name = 'changed' WHERE id = 'u1'")
            raise RuntimeError("boom")
    assert store.user_by_id("u1")["name"] == "A"


def test_concurrent_writers_all_succeed(database):
    """
    WAL plus busy_timeout plus retry should mean no writer is simply refused.

    This is the property that makes SQLite usable for a rollout at all, so it is
    worth an actual thread race rather than trust.
    """
    from app import store
    store.create_user("u1", "a@b.co", "A", "hash")
    errors = []

    def writer(n):
        try:
            from app import db as dbmod
            dbmod.close_thread_connection()      # a real second connection
            for i in range(10):
                store.record_submission(
                    "u1", f"0{n}-0{i}", "python", "src",
                    {"verdict": "accepted", "passed": 1, "total": 1}, 1.0)
        except Exception as exc:                              # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=writer, args=(n,)) for n in range(1, 5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == [], f"writers failed: {errors}"
    assert len(store.submissions("u1", limit=500)) == 40


@sqlite_only
def test_backup_produces_a_readable_copy(database, tmp_path):
    from app import store
    store.create_user("u1", "a@b.co", "A", "hash")
    target = tmp_path / "backup" / "copy.db"
    database.backup(target)

    # Read the copy with a plain connection: a backup that only our own code can
    # open is not a backup.
    conn = sqlite3.connect(target)
    try:
        assert conn.execute("SELECT email FROM users").fetchone()[0] == "a@b.co"
        assert conn.execute("PRAGMA user_version").fetchone()[0] == \
            database.SCHEMA_VERSION
    finally:
        conn.close()


def test_health_reports_a_schema_mismatch(database):
    """
    A half-finished rollout must fail its health check, not serve errors.

    Written through the backend so it holds on both engines -- one stores the
    version in the file header, the other in a table.
    """
    ok, _ = database.healthy()
    assert ok

    with database.transaction() as conn:
        database.backend.write_version(conn._conn, 999)
    ok, detail = database.healthy()
    assert not ok and "999" in detail


@postgres_only
def test_backup_points_at_pg_dump_instead_of_writing_a_bad_one(database, tmp_path):
    """
    Refusing beats reimplementing pg_dump badly.

    A half-correct dump that restores into a subtly different database is worse
    than an error telling you which tool to use.
    """
    with pytest.raises(RuntimeError, match="pg_dump"):
        database.backup(tmp_path / "copy.dump")
