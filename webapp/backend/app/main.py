"""
FastAPI backend for the DSA practice platform.

Serves the 342 problems and ~300 reference specs that already live under
`python/_harness`, grades submissions against them, and keeps per-user
progress in SQLite (see store.py).
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import progress, repo, store
from .execute import run_submission

app = FastAPI(
    title="DSA Practice Platform",
    description="Serves the repo's own problems and reference tests.",
    version="0.2.0",
)

# The Vite dev server runs on 5173/5174; the API on 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    store.init()


# ------------------------------------------------------------------- models

class SubmitRequest(BaseModel):
    problemId: str
    language: str = "python"
    source: str
    mode: str = Field(default="test", pattern="^(test|run)$")


class NoteRequest(BaseModel):
    body: str = ""


# -------------------------------------------------------------------- meta

@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "pythonRoot": str(repo.PYTHON_ROOT),
            "db": str(store.DB_PATH)}


@app.get("/api/meta")
def meta() -> Dict[str, Any]:
    """Everything the UI needs to boot: languages, topics, and totals."""
    return {
        "languages": repo.LANGUAGES,
        "topics": repo.topics(),
        "stats": repo.stats(),
        "difficulties": ["Easy", "Medium", "Hard", "Challenge"],
    }


# ----------------------------------------------------------------- problems

@app.get("/api/problems")
def problems(topic: Optional[int] = None,
             difficulty: Optional[str] = None,
             tested: Optional[bool] = None,
             status: Optional[str] = None,
             bookmarked: Optional[bool] = None,
             q: Optional[str] = None) -> List[Dict[str, Any]]:
    items = progress.decorate(repo.list_problems())
    if topic is not None:
        items = [p for p in items if p["topic"] == topic]
    if difficulty:
        want = difficulty.strip().capitalize()
        items = [p for p in items if p["difficulty"] == want]
    if tested is not None:
        items = [p for p in items if p["tested"] is tested]
    if status:
        items = [p for p in items if p["status"] == status]
    if bookmarked:
        items = [p for p in items if p["bookmarked"]]
    if q:
        needle = q.lower()
        items = [p for p in items
                 if needle in p["title"].lower()
                 or needle in p["topicName"].lower()
                 or any(needle in t.lower() for t in p["targets"])]
    return items


@app.get("/api/problems/random")
def random_problem(difficulty: Optional[str] = None,
                   unsolved: bool = True) -> Dict[str, Any]:
    """
    A random pick, honouring the filters the UI has applied.

    Declared before `/api/problems/{problem_id}` because FastAPI matches routes
    in order -- otherwise "random" would be read as a problem id and 404.
    """
    pool = progress.decorate(repo.list_problems())
    pool = [p for p in pool if p["tested"]]
    if difficulty:
        pool = [p for p in pool if p["difficulty"] == difficulty.capitalize()]
    if unsolved:
        unsolved_pool = [p for p in pool if p["status"] != "solved"]
        # Falling back to the full pool means "random" still works once
        # everything matching is solved, instead of returning a 404.
        pool = unsolved_pool or pool
    if not pool:
        raise HTTPException(status_code=404, detail="no problems match")
    return {"id": random.choice(pool)["id"]}


@app.get("/api/problems/{problem_id}")
def problem(problem_id: str) -> Dict[str, Any]:
    detail = repo.problem_detail(problem_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"no problem {problem_id}")
    detail.update(repo.neighbors(problem_id))
    progress.decorate([detail])
    detail["submissionCount"] = len(store.submissions(problem_id, limit=500))
    return detail


# ---------------------------------------------------------------- execution

@app.post("/api/submit")
def submit(req: SubmitRequest) -> Dict[str, Any]:
    if req.language != "python":
        raise HTTPException(
            status_code=400,
            detail=(f"{req.language} is not executable yet -- only Python "
                    f"runs today. The repo's reference tests are Python "
                    f"functions, so other languages need a separate "
                    f"stdin/stdout test format."),
        )
    target = repo.find_problem(req.problemId)
    if target is None:
        raise HTTPException(status_code=404,
                            detail=f"no problem {req.problemId}")
    report = run_submission(req.source, target.topic, target.num, req.mode)
    report["problemId"] = req.problemId

    # Only graded runs go in the history. "Run" is a scratchpad and recording
    # it would fill the timeline with attempts that were never judged.
    report["submissionId"] = (
        store.record_submission(req.problemId, req.language, req.source,
                                report.get("summary", {}),
                                report.get("elapsedMs", 0.0))
        if req.mode == "test" else None
    )
    return report


# -------------------------------------------------------------- submissions

@app.get("/api/submissions")
def submissions(problemId: Optional[str] = None,
                limit: int = 50) -> List[Dict[str, Any]]:
    return store.submissions(problemId, limit)


@app.get("/api/submissions/{sub_id}")
def submission(sub_id: int) -> Dict[str, Any]:
    row = store.submission(sub_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"no submission {sub_id}")
    return row


# ----------------------------------------------------------------- progress

@app.get("/api/progress")
def progress_overview() -> Dict[str, Any]:
    return progress.overview()


@app.get("/api/activity")
def activity(days: int = 365) -> Dict[str, Any]:
    return store.activity(days=max(7, min(days, 730)))


# ---------------------------------------------------- bookmarks and notes

@app.get("/api/bookmarks")
def bookmarks() -> List[str]:
    return store.bookmarks()


@app.post("/api/bookmarks/{problem_id}")
def toggle_bookmark(problem_id: str) -> Dict[str, Any]:
    if repo.find_problem(problem_id) is None:
        raise HTTPException(status_code=404, detail=f"no problem {problem_id}")
    return {"problemId": problem_id,
            "bookmarked": store.toggle_bookmark(problem_id)}


@app.get("/api/notes/{problem_id}")
def get_note(problem_id: str) -> Dict[str, Any]:
    return store.note(problem_id)


@app.put("/api/notes/{problem_id}")
def put_note(problem_id: str, req: NoteRequest) -> Dict[str, Any]:
    if repo.find_problem(problem_id) is None:
        raise HTTPException(status_code=404, detail=f"no problem {problem_id}")
    return store.save_note(problem_id, req.body)
