"""
Persistence for submissions, bookmarks and notes.

SQLite, one file under `backend/data/`. This is what turns the tool from an
editor into a platform: solved-state, submission history and streaks all come
from real rows rather than the browser's localStorage, so they survive a cache
clear and can be queried across problems.

Every table carries a `user_id`. There is exactly one user today -- the constant
`LOCAL_USER` -- but having the column from the start means adding accounts later
is a change to how `user_id` is resolved, not a migration of every table.
"""

from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "forge.db"
LOCAL_USER = "local"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT    NOT NULL DEFAULT 'local',
    problem_id  TEXT    NOT NULL,
    language    TEXT    NOT NULL,
    source      TEXT    NOT NULL,
    verdict     TEXT    NOT NULL,
    passed      INTEGER NOT NULL,
    total       INTEGER NOT NULL,
    elapsed_ms  REAL    NOT NULL,
    created_at  REAL    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_sub_user_problem
    ON submissions (user_id, problem_id, id DESC);
CREATE INDEX IF NOT EXISTS ix_sub_user_time
    ON submissions (user_id, created_at);

CREATE TABLE IF NOT EXISTS bookmarks (
    user_id    TEXT NOT NULL DEFAULT 'local',
    problem_id TEXT NOT NULL,
    created_at REAL NOT NULL,
    PRIMARY KEY (user_id, problem_id)
);

CREATE TABLE IF NOT EXISTS notes (
    user_id    TEXT NOT NULL DEFAULT 'local',
    problem_id TEXT NOT NULL,
    body       TEXT NOT NULL,
    updated_at REAL NOT NULL,
    PRIMARY KEY (user_id, problem_id)
);
"""


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    """
    A fresh connection per call.

    FastAPI runs sync endpoints in a threadpool, so a shared connection would
    need `check_same_thread=False` plus a lock. Per-call connections to a local
    file are cheap and sidestep that entirely. WAL keeps a write from blocking
    the reads that the dashboard fires alongside it.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    finally:
        conn.close()


def init() -> None:
    with _conn() as conn:
        conn.executescript(_SCHEMA)


# --------------------------------------------------------------- submissions

# Only these verdicts represent a real attempt worth keeping. A `stub` means
# the learner pressed Submit on untouched starter code, and recording those
# would make the history unreadable and the "attempted" count a lie.
KEEP_VERDICTS = {"accepted", "failed", "error", "missing"}


def record_submission(problem_id: str, language: str, source: str,
                      summary: Dict[str, Any], elapsed_ms: float,
                      user: str = LOCAL_USER) -> Optional[int]:
    """Store one graded attempt. Returns the row id, or None if not kept."""
    verdict = summary.get("verdict", "")
    if verdict not in KEEP_VERDICTS:
        return None
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO submissions (user_id, problem_id, language, source, "
            "verdict, passed, total, elapsed_ms, created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (user, problem_id, language, source, verdict,
             int(summary.get("passed", 0)), int(summary.get("total", 0)),
             float(elapsed_ms), time.time()),
        )
        return int(cur.lastrowid or 0)


def _row_to_submission(row: sqlite3.Row, with_source: bool) -> Dict[str, Any]:
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


def submissions(problem_id: Optional[str] = None, limit: int = 50,
                user: str = LOCAL_USER) -> List[Dict[str, Any]]:
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
    with _conn() as conn:
        rows = conn.execute(sql, args).fetchall()
    return [_row_to_submission(r, with_source=False) for r in rows]


def submission(sub_id: int, user: str = LOCAL_USER) -> Optional[Dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ? AND user_id = ?",
            (sub_id, user)).fetchone()
    return _row_to_submission(row, with_source=True) if row else None


def statuses(user: str = LOCAL_USER) -> Dict[str, str]:
    """
    problem_id -> "solved" | "attempted".

    One aggregate query rather than a per-problem lookup: the problem list needs
    a status for all 342 rows at once, and MAX over a grouped boolean is enough
    to say whether any attempt was ever accepted.
    """
    with _conn() as conn:
        rows = conn.execute(
            "SELECT problem_id, MAX(verdict = 'accepted') AS ok "
            "FROM submissions WHERE user_id = ? GROUP BY problem_id",
            (user,)).fetchall()
    return {r["problem_id"]: ("solved" if r["ok"] else "attempted")
            for r in rows}


def attempt_counts(user: str = LOCAL_USER) -> Dict[str, int]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT problem_id, COUNT(*) AS n FROM submissions "
            "WHERE user_id = ? GROUP BY problem_id", (user,)).fetchall()
    return {r["problem_id"]: r["n"] for r in rows}


# ------------------------------------------------------------------ activity

def activity(days: int = 365, user: str = LOCAL_USER) -> Dict[str, Any]:
    """
    Per-day submission and solve counts for the contribution heatmap.

    Days are bucketed in the server's local timezone. The server and the
    browser are the same machine in this setup, so local time is what the
    learner means by "today" -- UTC bucketing would roll the day over at the
    wrong moment for most of the world.
    """
    since = time.time() - days * 86400
    with _conn() as conn:
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

def bookmarks(user: str = LOCAL_USER) -> List[str]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM bookmarks WHERE user_id = ? "
            "ORDER BY created_at DESC", (user,)).fetchall()
    return [r["problem_id"] for r in rows]


def toggle_bookmark(problem_id: str, user: str = LOCAL_USER) -> bool:
    """Returns the new state: True if now bookmarked."""
    with _conn() as conn:
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

def note(problem_id: str, user: str = LOCAL_USER) -> Dict[str, Any]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT body, updated_at FROM notes "
            "WHERE user_id = ? AND problem_id = ?",
            (user, problem_id)).fetchone()
    if not row:
        return {"problemId": problem_id, "body": "", "updatedAt": None}
    return {"problemId": problem_id, "body": row["body"],
            "updatedAt": row["updated_at"]}


def save_note(problem_id: str, body: str, user: str = LOCAL_USER) -> Dict[str, Any]:
    now = time.time()
    with _conn() as conn:
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


def noted_problems(user: str = LOCAL_USER) -> List[str]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT problem_id FROM notes WHERE user_id = ?", (user,)).fetchall()
    return [r["problem_id"] for r in rows]
