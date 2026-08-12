"""
Aggregation for the dashboard and progress pages.

`repo` knows the curriculum, `store` knows what the learner did. Neither should
know about the other, so the joining happens here.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import content, repo, store

DIFFICULTIES = ["Easy", "Medium", "Hard", "Challenge"]


def _title_index() -> Dict[str, Dict[str, Any]]:
    return {f"{p.topic:02d}-{p.num:02d}": {
        "title": repo.pretty_title(p.title),
        "difficulty": p.difficulty,
        "topic": p.topic,
        "topicName": p.topic_name,
    } for p in repo.all_problems()}


def decorate(items: List[Dict[str, Any]],
             user_id: Optional[str]) -> List[Dict[str, Any]]:
    """
    Attach per-user state to problem summaries in one pass.

    `user_id` of None means signed out: every problem reads as "todo" with no
    bookmarks or notes, which is exactly what an anonymous visitor should see.
    Four queries become zero.
    """
    if user_id is None:
        for item in items:
            item["status"] = "todo"
            item["attempts"] = 0
            item["bookmarked"] = False
            item["hasNote"] = False
        return items

    status = store.statuses(user_id)
    attempts = store.attempt_counts(user_id)
    marked = set(store.bookmarks(user_id))
    noted = set(store.noted_problems(user_id))
    for item in items:
        pid = item["id"]
        item["status"] = status.get(pid, "todo")
        item["attempts"] = attempts.get(pid, 0)
        item["bookmarked"] = pid in marked
        item["hasNote"] = pid in noted
    return items


def overview(user_id: str) -> Dict[str, Any]:
    """Everything the dashboard needs, in one round trip."""
    problems = repo.all_problems()
    status = store.statuses(user_id)
    titles = _title_index()

    by_difficulty = {d: {"total": 0, "solved": 0, "attempted": 0}
                     for d in DIFFICULTIES}
    by_topic: Dict[int, Dict[str, Any]] = {}
    solved_total = attempted_total = 0

    for p in problems:
        pid = f"{p.topic:02d}-{p.num:02d}"
        state = status.get(pid, "todo")
        bucket = by_difficulty.setdefault(
            p.difficulty, {"total": 0, "solved": 0, "attempted": 0})
        bucket["total"] += 1

        topic = by_topic.setdefault(p.topic, {
            "topic": p.topic, "name": p.topic_name, "total": 0,
            "solved": 0, "attempted": 0, "tested": 0,
        })
        topic["total"] += 1
        if repo.specs_for(p.topic, p.num):
            topic["tested"] += 1

        if state == "solved":
            bucket["solved"] += 1
            topic["solved"] += 1
            solved_total += 1
        elif state == "attempted":
            bucket["attempted"] += 1
            topic["attempted"] += 1
            attempted_total += 1

    recent = store.submissions(user_id, limit=12)
    for sub in recent:
        sub.update(titles.get(sub["problemId"], {}))

    return {
        "totals": {
            "problems": len(problems),
            "solved": solved_total,
            "attempted": attempted_total,
            "tested": sum(1 for p in problems if repo.specs_for(p.topic, p.num)),
        },
        "byDifficulty": [
            {"difficulty": d, **by_difficulty[d]}
            for d in DIFFICULTIES if by_difficulty.get(d, {}).get("total")
        ],
        "byTopic": [
            {**by_topic[t], "level": repo._level_for(t)}
            for t in sorted(by_topic)
        ],
        "activity": store.activity(user_id),
        "recent": recent,
        "resume": _resume(user_id),
        "nextUp": _next_up(user_id, limit=5),
        "learning": _learning(user_id),
    }


def _learning(user_id: str) -> Dict[str, Any]:
    """
    Where the learner is in the reading, for the dashboard.

    The platform is a course as well as a judge now, so a dashboard that only
    counted solved problems would tell half the story -- and would make the
    theory feel optional.
    """
    out: Dict[str, Any] = {"courses": [], "next": None}
    for course in content.all_courses():
        done = store.completed_lessons(user_id, course.id)
        total = sum(len(m.lessons) for m in course.modules)
        out["courses"].append({
            "id": course.id, "title": course.title,
            "lessonsRead": len(done), "lessonCount": total,
        })
        if out["next"] is None:
            for module in course.modules:
                for lesson in module.lessons:
                    if f"{module.id}/{lesson.slug}" not in done:
                        out["next"] = {
                            "courseId": course.id, "courseTitle": course.title,
                            "moduleId": module.id, "moduleTitle": module.title,
                            "slug": lesson.slug, "title": lesson.title,
                            "minutes": lesson.minutes,
                        }
                        break
                if out["next"]:
                    break
    return out


def _resume(user_id: str) -> Optional[Dict[str, Any]]:
    """
    The most recent problem that was worked on but not solved.

    "Continue where you left off" is only useful if it points at unfinished
    work -- linking back to something already accepted would be a dead end.
    """
    status = store.statuses(user_id)
    titles = _title_index()
    for sub in store.submissions(user_id, limit=60):
        pid = sub["problemId"]
        if status.get(pid) != "solved" and pid in titles:
            return {"id": pid, **titles[pid], "verdict": sub["verdict"],
                    "at": sub["createdAt"]}
    return None


def _next_up(user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Suggested problems: untouched, auto-graded, in curriculum order.

    Graded ones come first because they are the only ones the platform can give
    feedback on -- recommending an ungraded problem would send the learner
    somewhere the Submit button cannot help them.
    """
    status = store.statuses(user_id)
    out: List[Dict[str, Any]] = []
    for p in repo.all_problems():
        pid = f"{p.topic:02d}-{p.num:02d}"
        if status.get(pid) or not repo.specs_for(p.topic, p.num):
            continue
        out.append({
            "id": pid,
            "title": repo.pretty_title(p.title),
            "difficulty": p.difficulty,
            "topic": p.topic,
            "topicName": p.topic_name,
        })
        if len(out) >= limit:
            break
    return out
