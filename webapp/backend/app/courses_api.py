"""
Routes for the learning side: courses, modules, lessons.

Kept in its own router rather than piled into main.py, because the learning
surface and the practice surface are separate concerns that happen to share a
user. The only place they meet is `module_practice()`, which is what turns a
module page from a document into something you can act on.

Reading a lesson does not require an account. Marking it complete does -- the
same rule the Submit button follows, and for the same reason: browsing is what
makes someone want an account.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from . import auth, content, progress, repo, store
from .execute import run_submission
from .settings import settings

router = APIRouter(prefix="/api/courses", tags=["courses"])


class DoneRequest(BaseModel):
    done: bool = True


def _progress(user: Optional[Dict[str, Any]], course_id: str) -> Dict[str, float]:
    if user is None:
        return {}
    return store.completed_lessons(user["id"], course_id)


def _module_practice(course: content.Course, module_id: str,
                     user: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    The problems belonging to a module, with the learner's status attached.

    Only the DSA course has graded problems today. The link is the module id
    doubling as the topic number, which holds because that course's directories
    *are* the topics; a course without exercises simply reports none rather than
    the page having to know which kind of course it is.

    The problems must go through `progress.decorate` -- `repo.list_problems()`
    returns them without per-user state, so reading `p["status"]` off a raw list
    raises. Signed out, decorate fills in "todo" for everything, which is the
    right answer rather than a special case here.
    """
    if course.language != "python" or not module_id.isdigit():
        return {"problems": [], "solved": 0, "total": 0}
    number = int(module_id)
    problems = progress.decorate(
        [p for p in repo.list_problems() if p["topic"] == number],
        user["id"] if user else None)
    return {
        "problems": problems,
        "total": len(problems),
        "solved": sum(1 for p in problems if p["status"] == "solved"),
    }


# ------------------------------------------------------------------- routes

@router.get("")
def list_courses(user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
                 ) -> List[Dict[str, Any]]:
    """The shelf. Public; progress fields are zero when signed out."""
    out = []
    for course in content.all_courses():
        done = _progress(user, course.id)
        total = sum(len(m.lessons) for m in course.modules)
        data = course.as_dict(with_modules=False)
        data["lessonsRead"] = len(done)
        data["lessonTotal"] = total
        if course.language == "python":
            # The practice half of the course, so a card can say "342 problems,
            # 12 solved" without the client stitching two endpoints together.
            data["problemTotal"] = repo.stats()["problems"]
            solved = 0
            if user:
                states = store.statuses(user["id"])
                solved = sum(1 for state in states.values() if state == "solved")
            data["problemsSolved"] = solved
        out.append(data)
    return out


@router.get("/{course_id}")
def get_course(course_id: str,
               user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
               ) -> Dict[str, Any]:
    course = content.get(course_id)
    if course is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no course {course_id}")

    done = _progress(user, course_id)
    data = course.as_dict(with_modules=False)
    modules = []
    for module in course.modules:
        entry = module.as_dict(with_lessons=False)
        read = sum(1 for lesson in module.lessons
                   if f"{module.id}/{lesson.slug}" in done)
        entry["lessonsRead"] = read
        practice = _module_practice(course, module.id, user)
        entry["problemTotal"] = practice["total"]
        entry["problemsSolved"] = practice["solved"]
        modules.append(entry)
    data["modules"] = modules
    data["lessonsRead"] = len(done)
    data["resume"] = _resume(course, done)
    return data


def _resume(course: content.Course, done: Dict[str, float]) -> Optional[Dict[str, Any]]:
    """
    The next unread lesson in course order.

    Deliberately "next unread" rather than "last read": the useful action is
    the one you have not done, and pointing at a lesson already marked complete
    would be a dead end.
    """
    for module in course.modules:
        for lesson in module.lessons:
            if f"{module.id}/{lesson.slug}" not in done:
                return {"moduleId": module.id, "moduleTitle": module.title,
                        "slug": lesson.slug, "title": lesson.title,
                        "ordinal": lesson.ordinal, "minutes": lesson.minutes}
    return None


@router.get("/{course_id}/modules/{module_id}")
def get_module(course_id: str, module_id: str,
               user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
               ) -> Dict[str, Any]:
    course = content.get(course_id)
    module = course.module(module_id) if course else None
    if course is None or module is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no module {module_id} in {course_id}")

    done = _progress(user, course_id)
    data = module.as_dict(with_lessons=True)
    for lesson in data["lessons"]:
        lesson["completed"] = f"{module_id}/{lesson['slug']}" in done
    data["lessonsRead"] = sum(1 for l in data["lessons"] if l["completed"])
    data["courseId"] = course_id
    data["courseTitle"] = course.title

    practice = _module_practice(course, module_id, user)
    data["practice"] = practice["problems"]
    data["problemTotal"] = practice["total"]
    data["problemsSolved"] = practice["solved"]

    index = [m.id for m in course.modules].index(module_id)
    data["prevModule"] = course.modules[index - 1].id if index > 0 else None
    data["nextModule"] = (course.modules[index + 1].id
                          if index + 1 < len(course.modules) else None)
    return data


@router.get("/{course_id}/modules/{module_id}/lessons/{slug}")
def get_lesson(course_id: str, module_id: str, slug: str,
               user: Optional[Dict[str, Any]] = Depends(auth.current_user_optional),
               ) -> Dict[str, Any]:
    lesson = content.lesson(course_id, module_id, slug)
    if lesson is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no lesson {slug}")

    course = content.get(course_id)
    module = course.module(module_id)
    done = _progress(user, course_id)

    data = lesson.as_dict(with_body=True)
    data.update(content.neighbours(course_id, module_id, slug))
    data["completed"] = f"{module_id}/{slug}" in done
    data["courseId"] = course_id
    data["courseTitle"] = course.title
    data["moduleId"] = module_id
    data["moduleTitle"] = module.title
    data["moduleLessonCount"] = len(module.lessons)
    return data


@router.post("/{course_id}/modules/{module_id}/lessons/{slug}/done")
def mark_lesson(course_id: str, module_id: str, slug: str, req: DoneRequest,
                request: Request,
                user: Dict[str, Any] = Depends(auth.current_user),
                ) -> Dict[str, Any]:
    auth.check_origin(request)
    if content.lesson(course_id, module_id, slug) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"no lesson {slug}")
    store.set_lesson_done(user["id"], course_id, f"{module_id}/{slug}", req.done)
    done = store.completed_lessons(user["id"], course_id)
    course = content.get(course_id)
    module = course.module(module_id)
    return {
        "completed": req.done,
        "moduleLessonsRead": sum(1 for l in module.lessons
                                 if f"{module_id}/{l.slug}" in done),
        "courseLessonsRead": len(done),
    }


@router.post("/{course_id}/modules/{module_id}/examples")
def run_examples(course_id: str, module_id: str, request: Request,
                 user: Dict[str, Any] = Depends(auth.current_user),
                 ) -> Dict[str, Any]:
    """
    Run the module's `examples.py` in the sandbox and return what it printed.

    The demos are already written to narrate themselves, and they go through the
    exact same isolated runner a submission does -- so "run the examples" costs
    no new execution path, and a demo that hangs is contained by the same limits.

    Signed in only: it is an execution request, and attributing it to an account
    is what keeps the concurrency cap meaningful.
    """
    auth.check_origin(request)
    directory = content.module_path(course_id, module_id)
    if directory is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"no module {module_id} in {course_id}")

    path = directory / "examples.py"
    if not path.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            "this module has no examples file")
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            f"could not read the examples: {exc}")

    if len(source.encode("utf-8")) > settings.exec_max_source_bytes:
        # The demos are long; say so rather than failing with a size error the
        # learner cannot act on.
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"this module's examples are larger than the "
            f"{settings.exec_max_source_bytes} byte execution limit -- run it "
            f"locally with: python {directory.name}/examples.py")

    report = run_submission(source, 0, 0, mode="run", language="python")
    return {
        "stdout": report.get("stdout", ""),
        "elapsedMs": report.get("elapsedMs", 0),
        "executor": report.get("executor", ""),
        "error": (report.get("compileError") or {}).get("message") or None,
    }
