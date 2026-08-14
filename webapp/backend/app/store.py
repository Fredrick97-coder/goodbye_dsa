"""
Queries. Nothing else.

Connection handling, pragmas, retries, transactions and migrations live in
`db.py`; the schema lives there too, as versioned migrations. This module only
issues SQL, which is what makes a future move to Postgres a matter of editing
`db.py` and any query that used a SQLite-ism, rather than untangling storage
concerns from application ones.

Every user-scoped function takes its user id explicitly. Nothing defaults to an
ambient "current user" -- a query that quietly fell back to one would be a single
refactor away from showing one account's progress to another.
"""

from __future__ import annotations

import time
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from . import db
from .settings import settings

# Kept only so a database written before accounts existed still opens; no
# session can ever resolve to it, because it is not a row in `users`.
LEGACY_USER = "local"

#: Re-exported so callers that report paths do not each reach into settings.
DB_PATH = settings.db_path


def init() -> None:
    """Open the database and run migrations. Delegates to db.init()."""
    db.init()


class EmailTaken(Exception):
    """Raised instead of leaking a raw sqlite3.IntegrityError to the route."""


# ------------------------------------------------------------------- users

def create_user(user_id: str, email: str, name: str,
                password_hash: str) -> Dict[str, Any]:
    now = time.time()
    with db.transaction() as conn:
        try:
            conn.execute(
                "INSERT INTO users (id, email, name, password_hash, created_at)"
                " VALUES (?,?,?,?,?)",
                (user_id, email, name, password_hash, now))
        except db.IntegrityError as exc:
            raise EmailTaken(email) from exc
    return {"id": user_id, "email": email, "name": name, "created_at": now,
            "password_hash": password_hash, "last_login_at": None}


def user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with db.reading() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?",
                           (email,)).fetchone()
    return dict(row) if row else None


def user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    with db.reading() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?",
                           (user_id,)).fetchone()
    return dict(row) if row else None


def set_password(user_id: str, password_hash: str) -> None:
    with db.transaction() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                     (password_hash, user_id))


def set_name(user_id: str, name: str) -> None:
    with db.transaction() as conn:
        conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))


def mark_login(user_id: str) -> None:
    with db.transaction() as conn:
        conn.execute("UPDATE users SET last_login_at = ? WHERE id = ?",
                     (time.time(), user_id))


def user_count() -> int:
    with db.reading() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()
        return int(row["n"])


# --------------------------------------------------------- lesson progress

def completed_lessons(user: str, course_id: str) -> Dict[str, float]:
    """lesson_id -> when it was completed, for one course."""
    rows = db.query_all(
        "SELECT lesson_id, completed_at FROM lesson_progress "
        "WHERE user_id = ? AND course_id = ?", (user, course_id))
    return {r["lesson_id"]: r["completed_at"] for r in rows}


def set_lesson_done(user: str, course_id: str, lesson_id: str,
                    done: bool) -> bool:
    """Mark or unmark. Returns the resulting state."""
    if done:
        db.execute(
            "INSERT INTO lesson_progress (user_id, course_id, lesson_id, "
            "completed_at) VALUES (?,?,?,?) "
            "ON CONFLICT(user_id, course_id, lesson_id) DO NOTHING",
            (user, course_id, lesson_id, time.time()))
    else:
        db.execute(
            "DELETE FROM lesson_progress WHERE user_id = ? AND course_id = ? "
            "AND lesson_id = ?", (user, course_id, lesson_id))
    return done


def lessons_read_count(user: str) -> int:
    row = db.query_one(
        "SELECT COUNT(*) AS n FROM lesson_progress WHERE user_id = ?", (user,))
    return int(row["n"]) if row else 0


def last_lesson_read(user: str, course_id: str) -> Optional[Dict[str, Any]]:
    """The most recently completed lesson, for "continue where you left off"."""
    row = db.query_one(
        "SELECT lesson_id, completed_at FROM lesson_progress "
        "WHERE user_id = ? AND course_id = ? "
        "ORDER BY completed_at DESC LIMIT 1", (user, course_id))
    if row is None:
        return None
    return {"lessonId": row["lesson_id"], "at": row["completed_at"]}


def granted_modules(user: str, course_id: str) -> set:
    """Modules this user has explicitly unlocked."""
    rows = db.query_all(
        "SELECT module_id FROM module_unlocks WHERE user_id = ? AND course_id = ?",
        (user, course_id))
    return {r["module_id"] for r in rows}


def grant_module(user: str, course_id: str, module_id: str,
                 reason: str = "skipped") -> None:
    db.execute(
        "INSERT INTO module_unlocks (user_id, course_id, module_id, "
        "unlocked_at, reason) VALUES (?,?,?,?,?) "
        "ON CONFLICT(user_id, course_id, module_id) DO NOTHING",
        (user, course_id, module_id, time.time(), reason))


def revoke_module(user: str, course_id: str, module_id: str) -> None:
    db.execute("DELETE FROM module_unlocks WHERE user_id = ? AND course_id = ? "
               "AND module_id = ?", (user, course_id, module_id))


def granted_problems(user: str) -> set:
    """Problems this user explicitly skipped past."""
    rows = db.query_all(
        "SELECT problem_id FROM problem_unlocks WHERE user_id = ?", (user,))
    return {r["problem_id"] for r in rows}


def grant_problem(user: str, problem_id: str, reason: str = "skipped") -> None:
    db.execute(
        "INSERT INTO problem_unlocks (user_id, problem_id, unlocked_at, reason) "
        "VALUES (?,?,?,?) ON CONFLICT(user_id, problem_id) DO NOTHING",
        (user, problem_id, time.time(), reason))


# ------------------------------------------------------------- preferences

#: What a client is allowed to set, and how each value is checked. A preference
#: that is not here is rejected -- otherwise the table becomes a place for the
#: browser to store arbitrary strings against a user id.
def _valid_language(value: str) -> bool:
    from . import languages
    lang = languages.get(value)
    return lang is not None and lang.implemented


PREFERENCE_KEYS = {
    "language": _valid_language,
}

#: Sent to a signed-out client and used when an account has never chosen.
PREFERENCE_DEFAULTS = {
    "language": "python",
}


def preferences(user: str) -> Dict[str, str]:
    """Every stored preference for this user, defaults filled in."""
    rows = db.query_all(
        "SELECT key, value FROM preferences WHERE user_id = ?", (user,))
    out = dict(PREFERENCE_DEFAULTS)
    for row in rows:
        if row["key"] in PREFERENCE_KEYS:
            out[row["key"]] = row["value"]
    return out


def set_preference(user: str, key: str, value: str) -> None:
    """
    Store one preference. The caller must have validated it.

    Upsert rather than delete-then-insert: two tabs saving at once would
    otherwise race to leave no row at all.
    """
    db.execute(
        "INSERT INTO preferences (user_id, key, value, updated_at) "
        "VALUES (?,?,?,?) ON CONFLICT(user_id, key) "
        "DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
        (user, key, value, time.time()))


def clear_preference(user: str, key: str) -> None:
    db.execute("DELETE FROM preferences WHERE user_id = ? AND key = ?",
               (user, key))


# ---------------------------------------------------------------- sessions

def create_session(token_hash: str, user_id: str, ttl_seconds: int,
                   user_agent: str = "") -> None:
    now = time.time()
    with db.transaction() as conn:
        conn.execute(
            # ON CONFLICT rather than INSERT OR REPLACE, which is SQLite-only.
            "INSERT INTO sessions (token_hash, user_id, created_at,"
            " touched_at, expires_at, user_agent) VALUES (?,?,?,?,?,?) "
            "ON CONFLICT (token_hash) DO UPDATE SET "
            "user_id = excluded.user_id, created_at = excluded.created_at, "
            "touched_at = excluded.touched_at, "
            "expires_at = excluded.expires_at, "
            "user_agent = excluded.user_agent",
            (token_hash, user_id, now, now, now + ttl_seconds, user_agent))
        # Opportunistic cleanup: expired rows are dead weight and this is the
        # one moment we are already holding a write connection.
        conn.execute("DELETE FROM sessions WHERE expires_at < ?", (now,))


def session_user(token_hash: str) -> Optional[Dict[str, Any]]:
    """The user for a live session, with the session's touched_at attached."""
    with db.reading() as conn:
        row = conn.execute(
            "SELECT u.*, s.touched_at AS session_touched "
            "FROM sessions s JOIN users u ON u.id = s.user_id "
            "WHERE s.token_hash = ? AND s.expires_at > ?",
            (token_hash, time.time())).fetchone()
    return dict(row) if row else None


def touch_session(token_hash: str, ttl_seconds: int) -> None:
    now = time.time()
    with db.transaction() as conn:
        conn.execute(
            "UPDATE sessions SET touched_at = ?, expires_at = ? "
            "WHERE token_hash = ?", (now, now + ttl_seconds, token_hash))


def delete_session(token_hash: str) -> None:
    with db.transaction() as conn:
        conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))


def delete_user_sessions(user_id: str, keep_token_hash: str = "") -> int:
    """Sign out everywhere. Used on password change, which must invalidate."""
    with db.transaction() as conn:
        cur = conn.execute(
            "DELETE FROM sessions WHERE user_id = ? AND token_hash != ?",
            (user_id, keep_token_hash))
        return cur.rowcount


def session_count(user_id: str) -> int:
    with db.reading() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM sessions "
            "WHERE user_id = ? AND expires_at > ?",
            (user_id, time.time())).fetchone()
        return int(row["n"])


# --------------------------------------------------------------- submissions

# Only these verdicts represent a real attempt worth keeping. A `stub` means
# the learner pressed Submit on untouched starter code, and recording those
# would make the history unreadable and the "attempted" count a lie.
KEEP_VERDICTS = {"accepted", "failed", "error", "missing"}


def record_submission(user: str, problem_id: str, language: str, source: str,
                      summary: Dict[str, Any],
                      elapsed_ms: float) -> Optional[int]:
    """Store one graded attempt. Returns the row id, or None if not kept."""
    verdict = summary.get("verdict", "")
    if verdict not in KEEP_VERDICTS:
        return None
    with db.transaction() as conn:
        # RETURNING rather than `cursor.lastrowid`, which is SQLite-only and has
        # no psycopg equivalent. Both engines support it (SQLite since 3.35).
        row = conn.execute(
            "INSERT INTO submissions (user_id, problem_id, language, source, "
            "verdict, passed, total, elapsed_ms, created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?) RETURNING id",
            (user, problem_id, language, source, verdict,
             int(summary.get("passed", 0)), int(summary.get("total", 0)),
             float(elapsed_ms), time.time()),
        ).fetchone()
        return int(row["id"]) if row else 0


def _row_to_submission(row: Any, with_source: bool) -> Dict[str, Any]:
    out = {
        "id": row["id"],
        "problemId": row["problem_id"],
        "language": row["language"],
        "verdict": row["verdict"],
        "passed": row["passed"],
        "total": row["total"],
        "elapsedMs": row["elapsed_ms"],
        "createdAt": row["created_at"],
    }
    if with_source:
        out["source"] = row["source"]
    return out


def submissions(user: str, problem_id: Optional[str] = None,
                limit: int = 50) -> List[Dict[str, Any]]:
    sql = "SELECT * FROM submissions WHERE user_id = ?"
    args: List[Any] = [user]
    if problem_id:
        sql += " AND problem_id = ?"
        args.append(problem_id)
    # created_at first: id order only matches time order as long as nothing
    # is ever backfilled, and a history that lies about "most recent" is worse
    # than a slightly slower sort.
    sql += " ORDER BY created_at DESC, id DESC LIMIT ?"
    args.append(max(1, min(limit, 500)))
    with db.reading() as conn:
        rows = conn.execute(sql, args).fetchall()
    return [_row_to_submission(r, with_source=False) for r in rows]


def submission(sub_id: int, user: str) -> Optional[Dict[str, Any]]:
    with db.reading() as conn:
        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ? AND user_id = ?",
            (sub_id, user)).fetchone()
    return _row_to_submission(row, with_source=True) if row else None


def statuses(user: str) -> Dict[str, str]:
    """
    problem_id -> "solved" | "attempted".

    One aggregate query rather than a per-problem lookup: the problem list needs
    a status for all 342 rows at once, and MAX over a grouped boolean is enough
    to say whether any attempt was ever accepted.
    """
    with db.reading() as conn:
        rows = conn.execute(
            # CASE rather than MAX(verdict = 'accepted'): that expression is a
            # SQLite-ism, because Postgres has no MAX() over booleans.
            "SELECT problem_id, MAX(CASE WHEN verdict = 'accepted' THEN 1 "
            "ELSE 0 END) AS ok "
            "FROM submissions WHERE user_id = ? GROUP BY problem_id",
            (user,)).fetchall()
    return {r["problem_id"]: ("solved" if r["ok"] else "attempted")
            for r in rows}


def attempt_counts(user: str) -> Dict[str, int]:
    with db.reading() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) AS n FROM submissions "
            "WHERE user_id = ? GROUP BY problem_id", (user,)).fetchall()
    return {r["problem_id"]: r["n"] for r in rows}


# ------------------------------------------------------------------ activity

def activity(user: str, days: int = 365) -> Dict[str, Any]:
    """
    Per-day submission and solve counts for the contribution heatmap.

    Days are bucketed in the server's local timezone. The server and the
    browser are the same machine in this setup, so local time is what the
    learner means by "today" -- UTC bucketing would roll the day over at the
    wrong moment for most of the world.
    """
    since = time.time() - days * 86400
    with db.reading() as conn:
        rows = conn.execute(
            "SELECT created_at, verdict, problem_id FROM submissions "
            "WHERE user_id = ? AND created_at >= ? ORDER BY created_at",
            (user, since)).fetchall()

    per_day: Dict[str, Dict[str, int]] = {}
    first_solve: Dict[str, str] = {}     # problem -> day of its first accept
    for r in rows:
        day = datetime.fromtimestamp(r["created_at"]).strftime("%Y-%m-%d")
        bucket = per_day.setdefault(day, {"submissions": 0, "solved": 0})
        bucket["submissions"] += 1
        if r["verdict"] == "accepted" and r["problem_id"] not in first_solve:
            first_solve[r["problem_id"]] = day
            bucket["solved"] += 1

    return {
        "days": [{"date": d, **v} for d, v in sorted(per_day.items())],
        "streak": _streak(set(per_day)),
        "longestStreak": _longest_streak(set(per_day)),
        "activeDays": len(per_day),
        "totalSubmissions": len(rows),
    }


def _streak(active: set) -> int:
    """
    Consecutive active days ending today.

    Yesterday counts as the anchor too: at 9am, a streak built yesterday has
    not been broken yet, and zeroing it before the day is over would punish
    the learner for not having practised at breakfast.
    """
    today = date.today()
    if today.isoformat() not in active:
        if (today - timedelta(days=1)).isoformat() not in active:
            return 0
        today -= timedelta(days=1)
    n = 0
    while today.isoformat() in active:
        n += 1
        today -= timedelta(days=1)
    return n


def _longest_streak(active: set) -> int:
    if not active:
        return 0
    days = sorted(date.fromisoformat(d) for d in active)
    best = run = 1
    for prev, cur in zip(days, days[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        best = max(best, run)
    return best


# ----------------------------------------------------------------- bookmarks

def bookmarks(user: str) -> List[str]:
    with db.reading() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM bookmarks WHERE user_id = ? "
            "ORDER BY created_at DESC", (user,)).fetchall()
    return [r["problem_id"] for r in rows]


def toggle_bookmark(problem_id: str, user: str) -> bool:
    """Returns the new state: True if now bookmarked."""
    with db.transaction() as conn:
        existing = conn.execute(
            "SELECT 1 FROM bookmarks WHERE user_id = ? AND problem_id = ?",
            (user, problem_id)).fetchone()
        if existing:
            conn.execute(
                "DELETE FROM bookmarks WHERE user_id = ? AND problem_id = ?",
                (user, problem_id))
            return False
        conn.execute(
            "INSERT INTO bookmarks (user_id, problem_id, created_at) "
            "VALUES (?,?,?)", (user, problem_id, time.time()))
        return True


# --------------------------------------------------------------------- notes

def note(problem_id: str, user: str) -> Dict[str, Any]:
    with db.reading() as conn:
        row = conn.execute(
            "SELECT body, updated_at FROM notes "
            "WHERE user_id = ? AND problem_id = ?",
            (user, problem_id)).fetchone()
    if not row:
        return {"problemId": problem_id, "body": "", "updatedAt": None}
    return {"problemId": problem_id, "body": row["body"],
            "updatedAt": row["updated_at"]}


def save_note(problem_id: str, body: str, user: str) -> Dict[str, Any]:
    now = time.time()
    with db.transaction() as conn:
        if body.strip():
            conn.execute(
                "INSERT INTO notes (user_id, problem_id, body, updated_at) "
                "VALUES (?,?,?,?) ON CONFLICT(user_id, problem_id) "
                "DO UPDATE SET body = excluded.body, "
                "updated_at = excluded.updated_at",
                (user, problem_id, body, now))
        else:
            # An emptied note is a deleted note, not a stored empty string --
            # otherwise the "has notes" badge would stay lit forever.
            conn.execute(
                "DELETE FROM notes WHERE user_id = ? AND problem_id = ?",
                (user, problem_id))
            return {"problemId": problem_id, "body": "", "updatedAt": None}
    return {"problemId": problem_id, "body": body, "updatedAt": now}


def noted_problems(user: str) -> List[str]:
    with db.reading() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM notes WHERE user_id = ?", (user,)).fetchall()
    return [r["problem_id"] for r in rows]


# ------------------------------------------------------- rate limiting

def record_attempt(bucket: str, client: str) -> None:
    """Log one failed attempt. Persisted, so a restart is not a way around it."""
    with db.transaction() as conn:
        conn.execute(
            "INSERT INTO auth_attempts (bucket, client, created_at) "
            "VALUES (?,?,?)", (bucket, client, time.time()))
        # Opportunistic pruning while we already hold the write lock. Ten
        # windows of history is plenty for any future forensics and keeps the
        # table from growing without bound.
        cutoff = time.time() - settings.rate_window_seconds * 10
        conn.execute("DELETE FROM auth_attempts WHERE created_at < ?", (cutoff,))


def count_attempts(bucket: str, client: str) -> int:
    since = time.time() - settings.rate_window_seconds
    with db.reading() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM auth_attempts "
            "WHERE bucket = ? AND client = ? AND created_at >= ?",
            (bucket, client, since)).fetchone()
    return int(row["n"]) if row else 0


def oldest_attempt(bucket: str, client: str) -> Optional[float]:
    since = time.time() - settings.rate_window_seconds
    with db.reading() as conn:
        row = conn.execute(
            "SELECT MIN(created_at) AS oldest FROM auth_attempts "
            "WHERE bucket = ? AND client = ? AND created_at >= ?",
            (bucket, client, since)).fetchone()
    return row["oldest"] if row and row["oldest"] is not None else None


def clear_attempts(bucket: str, client: str) -> None:
    with db.transaction() as conn:
        conn.execute("DELETE FROM auth_attempts WHERE bucket = ? AND client = ?",
                     (bucket, client))


def delete_user(user_id: str) -> bool:
    """Remove an account and everything it owns (via ON DELETE CASCADE)."""
    with db.transaction() as conn:
        cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return cur.rowcount > 0


def purge_expired_sessions() -> int:
    with db.transaction() as conn:
        cur = conn.execute("DELETE FROM sessions WHERE expires_at < ?",
                           (time.time(),))
        return cur.rowcount
