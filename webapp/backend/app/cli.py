"""
Operational commands: `python -m app.cli <command>`.

These exist because the alternative is a rollout where routine maintenance means
opening a SQLite shell and hoping. Every one of them is safe to run against a
live server -- `backup` uses the online backup API, `migrate` is idempotent, and
`delete-user` relies on the cascade rather than deleting from five tables in the
right order by hand.

    python -m app.cli check                  configuration and health
    python -m app.cli migrate                bring the schema to head
    python -m app.cli backup [path]          consistent copy, safe while running
    python -m app.cli vacuum                 reclaim space
    python -m app.cli users                  list accounts
    python -m app.cli delete-user EMAIL      remove an account and its data
    python -m app.cli reset-password EMAIL   set a new password, end sessions
    python -m app.cli purge-sessions         drop expired sessions
"""

from __future__ import annotations

import getpass
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from . import languages, auth, db, executors, settings as config, store
from .settings import settings


def _fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def cmd_check() -> int:
    """Everything a deployment should verify before taking traffic."""
    print(json.dumps(config.summary(), indent=2))
    db.init()
    ok, detail = db.healthy()
    print(f"\ndatabase: {'ok' if ok else 'DEGRADED'} -- {detail}")
    print(json.dumps(db.stats(), indent=2))

    have = executors.availability()
    print(f"\ndatabase: {db.backend.name}")
    print("\nlanguages:")
    for entry in languages.status():
        mark = "available" if entry["available"] else "unavailable"
        print(f"  {entry['id']:11} {mark:12} {entry['detail']}")

    print("\nexecutors:")
    for name in ("docker", "seatbelt", "local"):
        mark = "available  " if have[name] else "unavailable"
        print(f"  {name:9} {mark} {have[f'{name}_reason']}")

    resolved = config.resolve_executor()
    safe = executors.is_safe(resolved)
    print(f"\nresolved: {resolved} (sandboxed: {safe})")
    try:
        config.check_safety(resolved)
    except config.ConfigError as exc:
        return _fail(str(exc))
    if not safe:
        print("WARNING: submissions run without a sandbox. Fine locally, "
              "never for a deployment.")
    return 0 if ok else 1


def cmd_migrate() -> int:
    db.connect()
    before = db.current_version()
    applied = db.migrate()
    print(f"schema v{before} -> v{db.current_version()}"
          f"{' (applied ' + ', '.join(map(str, applied)) + ')' if applied else ' (nothing to do)'}")
    return 0


def cmd_backup(argv: list) -> int:
    db.init()
    if argv:
        target = Path(argv[0])
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = settings.db_path.parent / "backups" / f"forge-{stamp}.db"
    db.backup(target)
    size = target.stat().st_size
    print(f"backed up to {target} ({size:,} bytes)")
    return 0


def cmd_vacuum() -> int:
    db.init()
    before = db.stats()["sizeBytes"]
    db.vacuum()
    after = db.stats()["sizeBytes"]
    print(f"vacuumed: {before:,} -> {after:,} bytes")
    return 0


def cmd_users() -> int:
    db.init()
    rows = db.query_all(
        "SELECT u.id, u.email, u.name, u.created_at, u.last_login_at, "
        "(SELECT COUNT(*) FROM submissions s WHERE s.user_id = u.id) AS subs, "
        "(SELECT COUNT(*) FROM sessions x WHERE x.user_id = u.id "
        " AND x.expires_at > ?) AS live "
        "FROM users u ORDER BY u.created_at", (time.time(),))
    if not rows:
        print("no accounts")
        return 0
    print(f"{'email':34} {'name':16} {'subs':>5} {'sessions':>8}  created")
    for r in rows:
        created = datetime.fromtimestamp(r["created_at"]).strftime("%Y-%m-%d")
        print(f"{r['email'][:34]:34} {r['name'][:16]:16} {r['subs']:>5} "
              f"{r['live']:>8}  {created}")
    return 0


def cmd_delete_user(argv: list) -> int:
    if not argv:
        return _fail("usage: delete-user EMAIL")
    db.init()
    email = argv[0].strip().lower()
    user = store.user_by_email(email)
    if user is None:
        return _fail(f"no account for {email}")
    count = len(store.submissions(user["id"], limit=100_000))
    confirm = input(f"delete {email} and {count} submission(s)? [y/N] ")
    if confirm.strip().lower() != "y":
        print("cancelled")
        return 1
    store.delete_user(user["id"])
    print(f"deleted {email}")
    return 0


def cmd_reset_password(argv: list) -> int:
    """
    For the missing password-reset flow: an operator sets it directly.

    There is no email path in this deployment, so a self-service reset link would
    be a link nobody can receive. This is the honest substitute, and it ends every
    session for that account exactly as a self-service change would.
    """
    if not argv:
        return _fail("usage: reset-password EMAIL")
    db.init()
    email = argv[0].strip().lower()
    user = store.user_by_email(email)
    if user is None:
        return _fail(f"no account for {email}")
    password = getpass.getpass("new password: ")
    again = getpass.getpass("again: ")
    if password != again:
        return _fail("passwords do not match")
    if len(password) < auth.MIN_PASSWORD:
        return _fail(f"password must be at least {auth.MIN_PASSWORD} characters")
    store.set_password(user["id"], auth.hash_password(password))
    ended = store.delete_user_sessions(user["id"])
    print(f"password set for {email}; {ended} session(s) ended")
    return 0


def cmd_purge_sessions() -> int:
    db.init()
    print(f"purged {store.purge_expired_sessions()} expired session(s)")
    return 0


COMMANDS = {
    "check": lambda argv: cmd_check(),
    "migrate": lambda argv: cmd_migrate(),
    "backup": cmd_backup,
    "vacuum": lambda argv: cmd_vacuum(),
    "users": lambda argv: cmd_users(),
    "delete-user": cmd_delete_user,
    "reset-password": cmd_reset_password,
    "purge-sessions": lambda argv: cmd_purge_sessions(),
}


def main(argv: list) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    command, rest = argv[0], argv[1:]
    if command not in COMMANDS:
        return _fail(f"unknown command {command!r}. Try --help.")
    return COMMANDS[command](rest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
