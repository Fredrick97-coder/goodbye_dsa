"""
FastAPI backend for the DSA practice platform.

Serves the 342 problems and 377 reference specs that live under
`python/_harness`, grades submissions against them in an isolated executor, and
keeps each account's progress in SQLite.

Three tiers of access, deliberately:

* **Public** -- metadata, the problem list, a problem's statement and starter
  code, and `mode="run"`. You can read and experiment without an account, which
  is what makes the editor useful before signing up.
* **Signed in** -- grading (`mode="test"`), submission history, progress,
  bookmarks and notes. Anything that reads or writes an account's data.
* **Nobody** -- another user's data. Every query is scoped by the session's user
  id, never by a parameter the client can set.

Startup order matters and is enforced in `lifespan`: configure logging, open and
migrate the database, resolve which executor is in use, and refuse to serve at
all if that executor is unsafe for the environment. A server that came up
healthy while silently unable to isolate submissions would be the worst possible
outcome, so it is fatal rather than a warning.
"""

from __future__ import annotations

import logging
import random
import uuid
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import (Depends, FastAPI, HTTPException, Request, Response,
                     status)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import (auth, content, courses_api, db, executors, languages,
               progress, progression, repo, settings as config, store)
from .execute import run_submission
from .observability import (BodyLimitMiddleware, RequestContextMiddleware,
                            SecurityHeadersMiddleware, configure_logging,
                            install_exception_handlers)
from .settings import settings

log = logging.getLogger("forge.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    db.init()
    version = db.current_version()

    resolved = config.resolve_executor()
    object.__setattr__(settings, "resolved_executor", resolved)
    config.check_safety(resolved)          # fatal in prod on an unsafe runner

    reasons = executors.availability()
    log.info("forge starting: env=%s schema=v%d executor=%s (safe=%s)",
             settings.env, version, resolved, executors.is_safe(resolved))
    for name in ("docker", "seatbelt", "local"):
        log.debug("  executor %-8s %-11s %s", name,
                  "available" if reasons[name] else "unavailable",
                  reasons[f"{name}_reason"])
    for problem in config.warnings_for(resolved):
        log.warning("configuration: %s", problem)

    purged = store.purge_expired_sessions()
    if purged:
        log.info("purged %d expired session(s)", purged)

    try:
        yield
    finally:
        db.close_all()
        log.info("forge stopped")


app = FastAPI(
    title="DSA Practice Platform",
    description="Serves the repo's own problems and reference tests.",
    version="0.4.0",
    lifespan=lifespan,
    # Interactive docs are useful locally and are attack surface in production.
    docs_url=None if settings.is_prod else "/docs",
    redoc_url=None,
    openapi_url=None if settings.is_prod else "/openapi.json",
)

install_exception_handlers(app)

# Order matters: middleware added last runs first, so the request id is assigned
# before anything else can log, and the body limit is enforced before a handler
# reads the body.
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(BodyLimitMiddleware)
app.add_middleware(RequestContextMiddleware)

# `allow_credentials` is what lets the session cookie travel, and it is why the
# origin list has to stay narrow -- browsers refuse a wildcard origin with
# credentials, and it would be the wrong thing here anyway. Both this and
# auth.check_origin read the same settings, so they cannot drift apart.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=settings.allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
    max_age=600,
)


# ------------------------------------------------------------------- models

class SubmitRequest(BaseModel):
    problemId: str
    language: str = "python"
    source: str
    mode: str = Field(default="test", pattern="^(test|run)$")


class NoteRequest(BaseModel):
    body: str = ""


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class PasswordChangeRequest(BaseModel):
    currentPassword: str
    newPassword: str


class NameChangeRequest(BaseModel):
    name: str


# --------------------------------------------------------------------- auth

@app.post("/api/auth/register")
def register(req: RegisterRequest, request: Request,
             response: Response) -> Dict[str, Any]:
    auth.check_origin(request)
    auth.rate_limit(request, "register")

    email = auth.clean_email(req.email)
    password = auth.check_password(req.password)
    name = auth.clean_name(req.name, email)

    try:
        user = store.create_user(uuid.uuid4().hex, email, name,
                                 auth.hash_password(password))
    except store.EmailTaken:
        # Registration cannot hide that an email is taken -- the account has to
        # be unique -- so it says so plainly instead of pretending to succeed.
        auth.record_failure(request, "register")
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "an account with that email already exists")

    store.mark_login(user["id"])
    auth.set_session_cookie(response, auth.new_session(user["id"], request),
                            request)
    return {"user": auth.public_user(user),
            "preferences": store.preferences(user["id"])}


@app.post("/api/auth/login")
def login(req: LoginRequest, request: Request,
          response: Response) -> Dict[str, Any]:
    auth.check_origin(request)
    auth.rate_limit(request, "login")

    email = (req.email or "").strip().lower()
    user, _reason = auth.authenticate(email, req.password or "")
    if user is None:
        auth.record_failure(request, "login")
        # Same message and the same cost whether the email is unknown or the
        # password is wrong, so this cannot be used to enumerate accounts.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "email or password is incorrect")

    auth.clear_failures(request, "login")
    store.mark_login(user["id"])
    auth.set_session_cookie(response, auth.new_session(user["id"], request),
                            request)
    return {"user": auth.public_user(user),
            "preferences": store.preferences(user["id"])}


@app.post("/api/auth/logout")
def logout(request: Request, response: Response) -> Dict[str, Any]:
    auth.check_origin(request)
    token = request.cookies.get(auth.COOKIE_NAME)
    if token:
        store.delete_session(auth.token_hash(token))
    auth.clear_session_cookie(response, request)
    return {"ok": True}


@app.get("/api/auth/me")
def me(user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
       ) -> Dict[str, Any]:
    """Always 200, with `user: null` when signed out -- this is how the app boots."""
    if user is None:
        # Defaults, so a signed-out client renders the same shape rather than
        # branching on whether preferences exist.
        return {"user": None, "preferences": dict(store.PREFERENCE_DEFAULTS)}
    return {"user": auth.public_user(user),
            "preferences": store.preferences(user["id"]),
            "sessions": store.session_count(user["id"])}


@app.post("/api/auth/password")
def change_password(req: PasswordChangeRequest, request: Request,
                    response: Response,
                    user: Dict[str, Any] = Depends(auth.current_user),
                    ) -> Dict[str, Any]:
    auth.check_origin(request)
    auth.rate_limit(request, "password")

    if not auth.verify_password(req.currentPassword or "",
                                user["password_hash"]):
        auth.record_failure(request, "password")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "current password is incorrect")

    new_password = auth.check_password(req.newPassword)
    store.set_password(user["id"], auth.hash_password(new_password))

    # A password change must end every other session -- otherwise changing it
    # after losing a laptop accomplishes nothing. The current device gets a
    # fresh token rather than being signed out of the tab doing the change.
    old_token = request.cookies.get(auth.COOKIE_NAME) or ""
    ended = store.delete_user_sessions(user["id"])
    auth.set_session_cookie(response, auth.new_session(user["id"], request),
                            request)
    return {"ok": True, "otherSessionsEnded": max(0, ended - (1 if old_token else 0))}


@app.post("/api/auth/name")
def change_name(req: NameChangeRequest, request: Request,
                user: Dict[str, Any] = Depends(auth.current_user),
                ) -> Dict[str, Any]:
    auth.check_origin(request)
    name = auth.clean_name(req.name, user["email"])
    store.set_name(user["id"], name)
    return {"user": {**auth.public_user(user), "name": name}}


@app.post("/api/auth/logout-everywhere")
def logout_everywhere(request: Request,
                      user: Dict[str, Any] = Depends(auth.current_user),
                      ) -> Dict[str, Any]:
    auth.check_origin(request)
    token = request.cookies.get(auth.COOKIE_NAME) or ""
    ended = store.delete_user_sessions(user["id"], auth.token_hash(token))
    return {"ok": True, "otherSessionsEnded": ended}


class PreferencesRequest(BaseModel):
    """A partial update: only the keys present are changed."""
    language: Optional[str] = None


@app.get("/api/preferences")
def get_preferences(user: Dict[str, Any] = Depends(auth.current_user),
                    ) -> Dict[str, Any]:
    return store.preferences(user["id"])


@app.patch("/api/preferences")
def patch_preferences(req: PreferencesRequest, request: Request,
                      user: Dict[str, Any] = Depends(auth.current_user),
                      ) -> Dict[str, Any]:
    """
    Update the preferences named in the body.

    Every value is checked against the whitelist in store.PREFERENCE_KEYS, so
    this endpoint cannot be used to stash arbitrary strings against a user id --
    and a language that has no driver is refused rather than saved and then
    silently ignored at submit time.
    """
    auth.check_origin(request)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "no preferences given")
    for key, value in updates.items():
        check = store.PREFERENCE_KEYS.get(key)
        if check is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"unknown preference {key!r}")
        if not isinstance(value, str) or not check(value):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"{value!r} is not a valid {key}")
        store.set_preference(user["id"], key, value)
    return store.preferences(user["id"])


# -------------------------------------------------------------------- meta

app.include_router(courses_api.router)


@app.get("/api/health")
def health() -> Dict[str, Any]:
    """
    Liveness plus enough detail to diagnose a bad deployment.

    Returns 503 when the database is unreachable or its schema is not the one
    this code expects -- a health check that answers "ok" while the schema is a
    version behind is how a broken rollout stays up.
    """
    ok, detail = db.healthy()
    body: Dict[str, Any] = {
        "status": "ok" if ok else "degraded",
        "detail": detail,
        "config": config.summary(),
        "db": db.stats(),
        "content": content.stats(),
        "executorSafe": executors.is_safe(settings.resolved_executor or "local"),
        "warnings": config.warnings_for(settings.resolved_executor or "local"),
        "pythonRoot": str(repo.PYTHON_ROOT),
    }
    if not ok:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail)
    return body


@app.get("/api/ready")
def ready() -> Dict[str, Any]:
    """Cheap readiness probe: no row counts, no file size, just a query."""
    ok, detail = db.healthy()
    if not ok:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail)
    return {"status": "ready"}


@app.get("/api/meta")
def meta() -> Dict[str, Any]:
    """Everything the UI needs to boot: languages, topics, and totals."""
    return {
        "languages": repo.language_status(),
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
             q: Optional[str] = None,
             user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
             ) -> List[Dict[str, Any]]:
    """
    Public. Signed out, every problem simply reads as "todo".

    Browsing without an account has to work -- the whole point of prompting at
    Submit is that nothing prompts you for merely looking.
    """
    items = progress.decorate(repo.list_problems(),
                              user["id"] if user else None)
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


@app.post("/api/problems/{problem_id}/unlock")
def unlock_problem(problem_id: str, request: Request,
                   user: Dict[str, Any] = Depends(auth.current_user),
                   ) -> Dict[str, Any]:
    """
    Skip one problem and move the chain on.

    The chain is strictly linear, so without this being stuck on a single
    problem would wall off every problem after it. Recorded, and never refused.
    """
    auth.check_origin(request)
    if repo.find_problem(problem_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no problem {problem_id}")
    store.grant_problem(user["id"], problem_id, reason="skipped")
    chain = progression.problem_chain(user["id"])
    return {"unlocked": True, "problemId": problem_id,
            "next": chain.frontier, "solved": chain.position,
            "total": chain.total}


@app.get("/api/problems/chain")
def problem_chain(user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
                  ) -> Dict[str, Any]:
    """Where the learner is in the run: what is next, and how far along."""
    chain = progression.problem_chain(user["id"] if user else None)
    nxt = repo.problem_detail(chain.frontier) if chain.frontier else None
    return {
        "next": ({"id": chain.frontier, "title": nxt["title"],
                  "difficulty": nxt["difficulty"], "topicName": nxt["topicName"]}
                 if nxt else None),
        "solved": chain.position,
        "total": chain.total,
        "enabled": bool(settings.progression),
    }


@app.get("/api/problems/random")
def random_problem(difficulty: Optional[str] = None,
                   unsolved: bool = True,
                   user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
                   ) -> Dict[str, Any]:
    """
    A random pick, honouring the filters the UI has applied.

    Declared before `/api/problems/{problem_id}` because FastAPI matches routes
    in order -- otherwise "random" would be read as a problem id and 404.
    """
    pool = progress.decorate(repo.list_problems(),
                             user["id"] if user else None)
    pool = [p for p in pool if p["tested"]]
    if difficulty:
        pool = [p for p in pool if p["difficulty"] == difficulty.capitalize()]
    if unsolved:
        unsolved_pool = [p for p in pool if p["status"] != "solved"]
        # Falling back to the full pool means "random" still works once
        # everything matching is solved, instead of returning a 404.
        pool = unsolved_pool or pool
    if not pool:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no problems match")
    return {"id": random.choice(pool)["id"]}


@app.get("/api/problems/{problem_id}")
def problem(problem_id: str,
            user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
            ) -> Dict[str, Any]:
    detail = repo.problem_detail(problem_id)
    if detail is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no problem {problem_id}")
    detail.update(repo.neighbors(problem_id))
    detail["lockedReason"] = progression.problem_locked(
        problem_id, user["id"] if user else None)
    detail["locked"] = detail["lockedReason"] is not None
    uid = user["id"] if user else None
    progress.decorate([detail], uid)
    detail["submissionCount"] = (
        len(store.submissions(uid, problem_id, limit=500)) if uid else 0)
    return detail


# ---------------------------------------------------------------- execution

@app.post("/api/submit")
def submit(req: SubmitRequest, request: Request,
           user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
           ) -> Dict[str, Any]:
    """
    Run or grade a submission.

    `mode="run"` is open to anyone: it records nothing, and it is what makes the
    editor usable before signing in. `mode="test"` is graded and stored against
    an account, so it needs one -- the UI turns that 401 into the sign-in modal
    and replays the submission afterwards.
    """
    auth.check_origin(request)

    if req.mode == "test" and user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "sign in to submit and track your progress")

    lang = languages.get(req.language)
    if lang is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"unknown language {req.language!r}")
    if not lang.implemented:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"{lang.label} is not runnable yet -- {lang.todo}")
    usable, detail = languages.runtime_available(lang.runtime)
    if not usable:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            f"{lang.label} is unavailable on this server: {detail}")

    target = repo.find_problem(req.problemId)
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no problem {req.problemId}")

    # Enforced here, not just hidden in the UI. A lock that only exists in the
    # client is decoration -- anyone can POST.
    locked = progression.problem_locked(req.problemId,
                                        user["id"] if user else None)
    if locked and req.mode == "test":
        raise HTTPException(status.HTTP_423_LOCKED,
                            f"this problem is locked -- {locked}")

    # Non-Python drivers cannot run the Python specs, so they are handed the
    # serialised plan instead. Python loads the specs itself and ignores it.
    plan = None
    if req.language != "python" and req.mode == "test":
        plan = repo.plan(target.topic, target.num)
        if not plan["targets"] or plan["excluded"]:
            reasons = "; ".join(f"{e['name']}: {e['reason']}"
                                for e in plan["excluded"]) or "no portable tests"
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"this problem can only be graded in Python -- {reasons}")

    report = run_submission(req.source, target.topic, target.num, req.mode,
                            language=req.language, plan=plan)
    report["problemId"] = req.problemId

    # Only graded runs go in the history. "Run" is a scratchpad and recording
    # it would fill the timeline with attempts that were never judged.
    report["submissionId"] = (
        store.record_submission(user["id"], req.problemId, req.language,
                                req.source, report.get("summary", {}),
                                report.get("elapsedMs", 0.0))
        if req.mode == "test" and user else None
    )
    return report


# -------------------------------------------------------------- submissions

@app.get("/api/submissions")
def submissions(problemId: Optional[str] = None, limit: int = 50,
                user: Dict[str, Any] = Depends(auth.current_user),
                ) -> List[Dict[str, Any]]:
    return store.submissions(user["id"], problemId, limit)


@app.get("/api/submissions/{sub_id}")
def submission(sub_id: int,
               user: Dict[str, Any] = Depends(auth.current_user),
               ) -> Dict[str, Any]:
    # Scoped by user inside the query, so guessing an id that belongs to someone
    # else returns 404 rather than their source code.
    row = store.submission(sub_id, user["id"])
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no submission {sub_id}")
    return row


# ----------------------------------------------------------------- progress

@app.get("/api/progress")
def progress_overview(user: Dict[str, Any] = Depends(auth.current_user),
                      ) -> Dict[str, Any]:
    return progress.overview(user["id"])


@app.get("/api/activity")
def activity(days: int = 365,
             user: Dict[str, Any] = Depends(auth.current_user),
             ) -> Dict[str, Any]:
    return store.activity(user["id"], days=max(7, min(days, 730)))


# ---------------------------------------------------- bookmarks and notes

@app.get("/api/bookmarks")
def bookmarks(user: Dict[str, Any] = Depends(auth.current_user)) -> List[str]:
    return store.bookmarks(user["id"])


@app.post("/api/bookmarks/{problem_id}")
def toggle_bookmark(problem_id: str, request: Request,
                    user: Dict[str, Any] = Depends(auth.current_user),
                    ) -> Dict[str, Any]:
    auth.check_origin(request)
    if repo.find_problem(problem_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no problem {problem_id}")
    return {"problemId": problem_id,
            "bookmarked": store.toggle_bookmark(problem_id, user["id"])}


@app.get("/api/notes/{problem_id}")
def get_note(problem_id: str,
             user: Dict[str, Any] = Depends(auth.current_user),
             ) -> Dict[str, Any]:
    return store.note(problem_id, user["id"])


@app.put("/api/notes/{problem_id}")
def put_note(problem_id: str, req: NoteRequest, request: Request,
             user: Dict[str, Any] = Depends(auth.current_user),
             ) -> Dict[str, Any]:
    auth.check_origin(request)
    if repo.find_problem(problem_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no problem {problem_id}")
    return store.save_note(problem_id, req.body, user["id"])
