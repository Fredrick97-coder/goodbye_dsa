"""The storage layer: migrations, pragmas, constraints, transactions, backup."""

from __future__ import annotations

import sqlite3
import threading

import pytest


def test_migrations_run_to_head_and_are_idempotent(database):
    assert database.current_version() == database.SCHEMA_VERSION
    # Running again applies nothing -- the guard every deployment relies on.
    assert database.migrate() == []


def test_migration_is_recorded_in_the_file_not_a_table(database):
    """user_version lives in the header, so it cannot drift from the schema."""
    version = database.connect().execute("PRAGMA user_version").fetchone()[0]
    assert version == database.SCHEMA_VERSION


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
    """Without ON DELETE CASCADE being enforced, this would silently succeed."""
    from app import store
    with pytest.raises(sqlite3.IntegrityError):
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
    ok, _ = database.healthy()
    assert ok
    database.connect().execute("PRAGMA user_version = 999")
    ok, detail = database.healthy()
    assert not ok and "999" in detail
