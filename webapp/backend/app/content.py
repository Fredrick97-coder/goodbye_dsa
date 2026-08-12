"""
Courses, modules and lessons, loaded from the filesystem.

The platform is not only DSA, so "course" is the top-level unit and everything
below it is generic. A course is a directory containing a `course.json` manifest;
the DSA curriculum is course #1 and needed no re-authoring, because its 22 topic
directories already had the right shape.

    <courses root>/
      python/                     <- course "dsa"
        course.json               title, level per module, file names
        19_heaps_priority_queues/
          theory.md               -> 14 lessons
          examples.py             -> runnable
          exercise.py             -> graded problems (see repo.py)
          project.py
      system-design/              <- a future course, same shape
        course.json

**Content stays in files and the database stores only user state.** That is the
same rule the problem catalogue follows: authored material belongs in git where
it can be reviewed in a diff, and a `lesson_progress` row is the only thing a
learner's reading adds. Nothing here writes.

Lessons are the `##` sections of `theory.md`. That convention was already
consistent across all 22 modules -- 9 to 14 sections each, 258 in total -- so it
is the natural boundary rather than an imposed one. A lesson is identified by the
**slug of its title**, not its position: inserting a section in the middle must
not shift every id and silently reset a learner's progress. Renaming a section
does lose that one checkmark, which is the cheaper failure.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from .settings import settings

MANIFEST = "course.json"

#: Reading-time model. Prose and code are counted separately because they are
#: not read at the same speed: an early version counted prose only and put
#: "1 min" on a heap lesson with three implementations in it, which is the kind
#: of number that makes a learner distrust every other number on the page.
WORDS_PER_MINUTE = 190
CODE_LINES_PER_MINUTE = 11


# ------------------------------------------------------------------- models

@dataclass(frozen=True)
class Lesson:
    slug: str
    title: str
    ordinal: int                # 1-based position, for display only
    body: str                   # raw markdown, rendered by the client
    words: int
    code_blocks: int
    code_lines: int

    @property
    def minutes(self) -> int:
        return max(1, round(self.words / WORDS_PER_MINUTE
                            + self.code_lines / CODE_LINES_PER_MINUTE))

    def as_dict(self, with_body: bool = False) -> Dict[str, Any]:
        data = {
            "slug": self.slug, "title": self.title, "ordinal": self.ordinal,
            "minutes": self.minutes, "words": self.words,
            "codeBlocks": self.code_blocks, "codeLines": self.code_lines,
        }
        if with_body:
            data["body"] = self.body
        return data


@dataclass(frozen=True)
class Module:
    id: str                     # "19"
    dir: str
    title: str
    level: str
    intro: str                  # the prose above the first ## section
    lessons: List[Lesson] = field(default_factory=list)
    has_examples: bool = False
    has_project: bool = False

    def as_dict(self, with_lessons: bool = True) -> Dict[str, Any]:
        data = {
            "id": self.id, "title": self.title, "level": self.level,
            "intro": self.intro, "lessonCount": len(self.lessons),
            "minutes": sum(l.minutes for l in self.lessons),
            "hasExamples": self.has_examples, "hasProject": self.has_project,
        }
        if with_lessons:
            data["lessons"] = [l.as_dict() for l in self.lessons]
        return data


@dataclass(frozen=True)
class Course:
    id: str
    title: str
    subtitle: str
    language: str
    root: Path
    levels: List[str]
    modules: List[Module]
    practice_languages: List[str] = field(default_factory=list)

    def as_dict(self, with_modules: bool = True) -> Dict[str, Any]:
        data = {
            "id": self.id, "title": self.title, "subtitle": self.subtitle,
            "language": self.language, "levels": self.levels,
            "moduleCount": len(self.modules),
            "lessonCount": sum(len(m.lessons) for m in self.modules),
            "minutes": sum(l.minutes for m in self.modules for l in m.lessons),
            "practiceLanguages": self.practice_languages,
        }
        if with_modules:
            data["modules"] = [m.as_dict(with_lessons=False)
                               for m in self.modules]
        return data

    def module(self, module_id: str) -> Optional[Module]:
        return next((m for m in self.modules if m.id == module_id), None)


# ------------------------------------------------------------------ parsing

def slugify(text: str) -> str:
    """
    A stable, readable id for a lesson title.

    The leading "3. " of "## 3. The Two Core Operations" is dropped: it is
    positional, and keeping it would make the id change when a section is
    inserted above -- exactly the fragility slugs are meant to avoid.
    """
    text = re.sub(r"^\s*\d+[.)]\s*", "", text.strip())
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"`([^`]*)`", r"\1", text)          # drop inline code marks
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def _strip_number(title: str) -> str:
    return re.sub(r"^\s*\d+[.)]\s*", "", title.strip())


def parse_theory(markdown: str) -> tuple:
    """
    (intro, lessons) from a theory file.

    Fence-aware, which is not optional here: the files contain 315 code blocks
    full of Python comments, and a naive scan for `#` at the start of a line
    reads those as headings -- one module appeared to have 21 top-level titles.
    """
    lines = markdown.splitlines()
    fence = False
    intro: List[str] = []
    lessons: List[Lesson] = []
    current_title: Optional[str] = None
    current: List[str] = []

    def flush() -> None:
        if current_title is None:
            return
        body = "\n".join(current).strip("\n")
        prose_words, code_lines = _measure(body)
        lessons.append(Lesson(
            slug=slugify(current_title),
            title=_strip_number(current_title),
            ordinal=len(lessons) + 1,
            body=body,
            words=prose_words,
            code_blocks=body.count("```") // 2,
            code_lines=code_lines,
        ))

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            fence = not fence
            (current if current_title else intro).append(line)
            continue
        if not fence and line.startswith("## "):
            flush()
            current_title = line[3:].strip()
            current = []
            continue
        if not fence and line.startswith("# ") and current_title is None:
            continue                                  # the module title itself
        (current if current_title else intro).append(line)

    flush()

    # The intro is the pitch above the first section: keep the prose, drop the
    # horizontal rule that separates it from lesson one.
    intro_text = "\n".join(intro).strip()
    intro_text = re.sub(r"\n-{3,}\s*$", "", intro_text).strip()
    return intro_text, lessons


def _measure(text: str) -> tuple:
    """(prose words, code lines). Blank and comment-only code lines are skipped."""
    prose: List[str] = []
    code = 0
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            bare = line.strip()
            if bare and not bare.startswith(("#", "//")):
                code += 1
        else:
            prose.append(line)
    return len(re.findall(r"\b[\w'-]+\b", " ".join(prose))), code


# ------------------------------------------------------------------ loading

def courses_root() -> Path:
    return settings.courses_root


@lru_cache(maxsize=1)
def _load_all() -> Dict[str, Course]:
    """
    Every course under the root, keyed by id.

    Cached for the process lifetime: parsing 22 theory files is ~30 ms, and the
    files do not change under a running server. `reload()` exists for tests and
    for an operator who has just edited content.
    """
    found: Dict[str, Course] = {}
    root = courses_root()
    if not root.exists():
        return found

    for manifest_path in sorted(root.glob(f"*/{MANIFEST}")):
        try:
            course = _load_course(manifest_path)
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            # A malformed course must not take down the whole shelf.
            continue
        if course.modules:
            found[course.id] = course
    return found


def _load_course(manifest_path: Path) -> Course:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base = manifest_path.parent
    theory_name = manifest.get("theoryFile", "theory.md")
    examples_name = manifest.get("examplesFile", "examples.py")
    project_name = manifest.get("projectFile", "project.py")

    modules: List[Module] = []
    for entry in manifest.get("modules", []):
        directory = base / entry["dir"]
        theory = directory / theory_name
        if not theory.exists():
            continue
        intro, lessons = parse_theory(theory.read_text(encoding="utf-8"))
        modules.append(Module(
            id=str(entry["id"]),
            dir=entry["dir"],
            title=entry.get("title") or entry["dir"],
            level=entry.get("level", ""),
            intro=intro,
            lessons=lessons,
            has_examples=(directory / examples_name).exists(),
            has_project=(directory / project_name).exists(),
        ))

    return Course(
        id=manifest["id"],
        title=manifest.get("title", manifest["id"]),
        subtitle=manifest.get("subtitle", ""),
        language=manifest.get("language", ""),
        root=base,
        levels=manifest.get("levels", []),
        modules=modules,
        practice_languages=manifest.get("practiceLanguages", []),
    )


def reload() -> None:
    _load_all.cache_clear()


def all_courses() -> List[Course]:
    return list(_load_all().values())


def get(course_id: str) -> Optional[Course]:
    return _load_all().get(course_id)


def lesson(course_id: str, module_id: str, slug: str) -> Optional[Lesson]:
    course = get(course_id)
    module = course.module(module_id) if course else None
    if module is None:
        return None
    return next((l for l in module.lessons if l.slug == slug), None)


def neighbours(course_id: str, module_id: str, slug: str) -> Dict[str, Any]:
    """
    Previous and next lesson, crossing module boundaries.

    A reader that stops at the end of a module makes the course feel like 22
    disconnected documents, so "next" walks into the following module.
    """
    course = get(course_id)
    if course is None:
        return {"prev": None, "next": None}
    flat = [(m.id, l) for m in course.modules for l in m.lessons]
    for i, (mid, les) in enumerate(flat):
        if mid == module_id and les.slug == slug:
            before = flat[i - 1] if i > 0 else None
            after = flat[i + 1] if i + 1 < len(flat) else None
            return {
                "prev": {"moduleId": before[0], "slug": before[1].slug,
                         "title": before[1].title} if before else None,
                "next": {"moduleId": after[0], "slug": after[1].slug,
                         "title": after[1].title} if after else None,
            }
    return {"prev": None, "next": None}


def lesson_ids(course_id: str) -> List[str]:
    """`"<module>/<slug>"` for every lesson, which is how progress is keyed."""
    course = get(course_id)
    if course is None:
        return []
    return [f"{m.id}/{l.slug}" for m in course.modules for l in m.lessons]


def module_path(course_id: str, module_id: str) -> Optional[Path]:
    course = get(course_id)
    module = course.module(module_id) if course else None
    return (course.root / module.dir) if course and module else None


def stats() -> Dict[str, Any]:
    """For /api/health, so a content problem is visible without a page load."""
    return {
        "root": str(courses_root()),
        "courses": [{"id": c.id, "modules": len(c.modules),
                     "lessons": sum(len(m.lessons) for m in c.modules)}
                    for c in all_courses()],
    }
