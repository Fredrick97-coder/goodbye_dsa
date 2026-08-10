"""
FastAPI backend for the DSA practice platform.

Serves the 342 problems and ~300 reference specs that already live under
`python/_harness`, and grades submissions against them.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import repo
from .execute import run_submission

app = FastAPI(
    title="DSA Practice Platform",
    description="Serves the repo's own problems and reference tests.",
    version="0.1.0",
)

# The Vite dev server runs on 5173/5174; the API on 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmitRequest(BaseModel):
    problemId: str
    language: str = "python"
    source: str
    mode: str = Field(default="test", pattern="^(test|run)$")


@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "pythonRoot": str(repo.PYTHON_ROOT)}


@app.get("/api/meta")
def meta() -> Dict[str, Any]:
    """Everything the UI needs to boot: languages, topics, and totals."""
    return {
        "languages": repo.LANGUAGES,
        "topics": repo.topics(),
        "stats": repo.stats(),
        "difficulties": ["Easy", "Medium", "Hard", "Challenge"],
    }


@app.get("/api/problems")
def problems(topic: Optional[int] = None,
             difficulty: Optional[str] = None,
             tested: Optional[bool] = None,
             q: Optional[str] = None) -> List[Dict[str, Any]]:
    items = repo.list_problems()
    if topic is not None:
        items = [p for p in items if p["topic"] == topic]
    if difficulty:
        want = difficulty.strip().capitalize()
        items = [p for p in items if p["difficulty"] == want]
    if tested is not None:
        items = [p for p in items if p["tested"] is tested]
    if q:
        needle = q.lower()
        items = [p for p in items
                 if needle in p["title"].lower()
                 or needle in p["topicName"].lower()
                 or any(needle in t.lower() for t in p["targets"])]
    return items


@app.get("/api/problems/{problem_id}")
def problem(problem_id: str) -> Dict[str, Any]:
    detail = repo.problem_detail(problem_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"no problem {problem_id}")
    return detail


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
    return report
