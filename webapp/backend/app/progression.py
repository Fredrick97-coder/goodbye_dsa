"""
Progressive unlocking: which modules, lessons and problems are open yet.

The curriculum has always been ordered -- backtracking assumes recursion, segment
trees assume trees -- but nothing enforced it, so it was possible to open module
20 first and bounce off it. This makes the order real.

**It is deliberately not strict, and that is the whole design.** Gating every
module behind 100% of the previous one's problems would put 315 problems in front
of module 22, which is a cage rather than a curriculum. Three things keep it
humane:

* **Reading is the cheap gate, solving is the honest one.** A module opens when
  the previous one's lessons are read *and* a fraction of its problems are
  solved -- 40% by default, so five problems out of twelve, not twelve.
* **There is always a way through.** "Unlock anyway" opens any module and is
  recorded. Someone who already knows arrays should not have to prove it, and a
  learner stuck on one Hard problem must never be walled out of everything after
  it.
* **Existing work is grandfathered.** Turning this on cannot lock you out of a
  module you have already read or solved in.

Thresholds live in the course manifest, because how strict a course should be is
a property of the course, not of the platform. `FORGE_PROGRESSION` turns the
whole thing off.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from . import content, store
from .settings import settings

#: Used when a manifest says nothing. All lessons read, 40% of problems solved.
DEFAULT_RULE = {"requireLessons": 1.0, "requireProblems": 0.4}


@dataclass
class ModuleState:
    id: str
    unlocked: bool
    #: Why it is open: "first", "earned", "granted", "in-progress", "disabled".
    reason: str
    lessons_read: int
    lesson_count: int
    problems_solved: int
    problem_total: int
    #: What is still missing, when locked.
    needs_lessons: int = 0
    needs_problems: int = 0
    blocked_by: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "unlocked": self.unlocked,
            "reason": self.reason,
            "lessonsRead": self.lessons_read,
            "lessonCount": self.lesson_count,
            "problemsSolved": self.problems_solved,
            "problemTotal": self.problem_total,
            "needsLessons": self.needs_lessons,
            "needsProblems": self.needs_problems,
            "blockedBy": self.blocked_by,
        }


def rule_for(course: content.Course) -> Dict[str, float]:
    raw = getattr(course, "progression", None) or {}
    rule = dict(DEFAULT_RULE)
    for key in ("requireLessons", "requireProblems"):
        if key in raw:
            try:
                rule[key] = max(0.0, min(1.0, float(raw[key])))
            except (TypeError, ValueError):
                pass
    return rule


def enabled(course: content.Course) -> bool:
    if not settings.progression:
        return False
    raw = getattr(course, "progression", None)
    if isinstance(raw, dict) and raw.get("enabled") is False:
        return False
    return True


def _required(fraction: float, total: int) -> int:
    """
    How many of `total` are needed.

    Ceiling, so a 40% rule on a 12-problem module asks for 5 rather than 4.8 --
    and a module with no problems requires none rather than one.
    """
    if total <= 0:
        return 0
    return min(total, math.ceil(fraction * total))


def compute(course: content.Course, user_id: Optional[str]) -> Dict[str, ModuleState]:
    """
    Lock state for every module in a course.

    One pass, three queries. The problem statuses and lesson completions are
    fetched once rather than per module: this runs on the course page, the module
    page, the problem list and every submission.
    """
    from . import repo

    lessons_done = store.completed_lessons(user_id, course.id) if user_id else {}
    statuses = store.statuses(user_id) if user_id else {}
    granted = (store.granted_modules(user_id, course.id) if user_id else set())

    rule = rule_for(course)
    active = enabled(course)
    states: Dict[str, ModuleState] = {}
    previous_complete = True          # the first module has nothing before it

    for index, module in enumerate(course.modules):
        problems = repo.problems_in_topic(module.id)
        solved = sum(1 for p in problems
                     if statuses.get(f"{p.topic:02d}-{p.num:02d}") == "solved")
        read = sum(1 for lesson in module.lessons
                   if f"{module.id}/{lesson.slug}" in lessons_done)

        need_lessons = _required(rule["requireLessons"], len(module.lessons))
        need_problems = _required(rule["requireProblems"], len(problems))
        complete = read >= need_lessons and solved >= need_problems

        if not active:
            state = ModuleState(module.id, True, "disabled", read,
                                len(module.lessons), solved, len(problems))
        elif index == 0:
            state = ModuleState(module.id, True, "first", read,
                                len(module.lessons), solved, len(problems))
        elif module.id in granted:
            state = ModuleState(module.id, True, "granted", read,
                                len(module.lessons), solved, len(problems))
        elif read > 0 or solved > 0:
            # Grandfathering: work already done here keeps it open. Enabling
            # progression must never take away a module someone has started.
            state = ModuleState(module.id, True, "in-progress", read,
                                len(module.lessons), solved, len(problems))
        elif previous_complete:
            state = ModuleState(module.id, True, "earned", read,
                                len(module.lessons), solved, len(problems))
        else:
            before = course.modules[index - 1]
            before_state = states[before.id]
            state = ModuleState(
                module.id, False, "locked", read, len(module.lessons),
                solved, len(problems),
                needs_lessons=max(0, _required(rule["requireLessons"],
                                               len(before.lessons))
                                  - before_state.lessons_read),
                needs_problems=max(0, _required(rule["requireProblems"],
                                                before_state.problem_total)
                                   - before_state.problems_solved),
                blocked_by=before.id,
            )

        states[module.id] = state
        previous_complete = complete

    return states


def module_unlocked(course_id: str, module_id: str,
                    user_id: Optional[str]) -> bool:
    course = content.get(course_id)
    if course is None:
        return True
    state = compute(course, user_id).get(module_id)
    return state.unlocked if state else True


def locked_reason(course: content.Course, module_id: str,
                  user_id: Optional[str]) -> Optional[str]:
    """
    Why this module is locked, phrased as something the learner can act on.

    Two things an earlier version got wrong. It told you to finish module 04
    while module 04 was itself locked behind 03 -- so the instruction was
    impossible. And it gave a signed-out visitor a lesson count to complete,
    which they have nowhere to record. Both now point at the nearest thing that
    is actually open.
    """
    states = compute(course, user_id)
    state = states.get(module_id)
    if state is None or state.unlocked:
        return None

    if user_id is None:
        return ("sign in to track your progress and unlock the rest of the "
                "course")

    # Walk back to the last module that is open: that is where work can happen.
    ids = [m.id for m in course.modules]
    frontier = None
    for candidate in ids[:ids.index(module_id)][::-1]:
        if states[candidate].unlocked:
            frontier = states[candidate]
            break
    if frontier is None:
        return "finish the earlier modules first"

    parts: List[str] = []
    rule = rule_for(course)
    need_lessons = _required(rule["requireLessons"], frontier.lesson_count)
    need_problems = _required(rule["requireProblems"], frontier.problem_total)
    missing_lessons = max(0, need_lessons - frontier.lessons_read)
    missing_problems = max(0, need_problems - frontier.problems_solved)
    if missing_lessons:
        parts.append(f"{missing_lessons} more lesson"
                     f"{'s' if missing_lessons != 1 else ''}")
    if missing_problems:
        parts.append(f"{missing_problems} more problem"
                     f"{'s' if missing_problems != 1 else ''}")
    detail = " and ".join(parts) if parts else "finishing it"

    if frontier.id == ids[ids.index(module_id) - 1]:
        return f"module {module_id} opens after {detail} in module {frontier.id}"
    return (f"continue from module {frontier.id} -- {detail} there, then keep "
            f"going to reach module {module_id}")


def problem_locked(problem_id: str, user_id: Optional[str]) -> Optional[str]:
    """
    Why this problem is locked, or None.

    Problems inherit their module's state. Returning the reason rather than a
    bool means the API can explain the wall instead of just refusing.
    """
    if not settings.progression:
        return None
    try:
        module_id = str(problem_id).split("-")[0]
    except (AttributeError, IndexError):
        return None

    for course in content.all_courses():
        if course.language != "python":
            continue
        if module_id not in {m.id for m in course.modules}:
            continue
        return locked_reason(course, module_id, user_id)
    return None


def summary(course: content.Course, user_id: Optional[str]) -> Dict[str, Any]:
    states = compute(course, user_id)
    unlocked = [s for s in states.values() if s.unlocked]
    return {
        "enabled": enabled(course),
        "rule": rule_for(course),
        "modulesUnlocked": len(unlocked),
        "moduleCount": len(states),
        "modules": {mid: s.as_dict() for mid, s in states.items()},
    }
