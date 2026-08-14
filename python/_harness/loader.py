"""
Import the learner's exercise.py files safely.

Two obstacles:

  1. Topic directories start with digits ("19_heaps_priority_queues"), so they
     are not importable as normal packages. We load by file path instead.

  2. Every exercise.py prints its full problem list on import. We swallow that
     output -- otherwise running the checker would dump thousands of lines.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent

TOPIC_RE = re.compile(r"^(\d{2})_")


def course_roots() -> List[Path]:
    """
    Every directory that is a course: one holding a `course.json`.

    The harness started life scanning only `python/`, but the platform hosts
    more than one course now. A manifest is the marker rather than a hardcoded
    list, so adding a course stays a directory rather than a code change --
    the same rule the web app's content loader follows.
    """
    roots = [ROOT] if ROOT.is_dir() else []
    for sibling in sorted(REPO_ROOT.iterdir()):
        if sibling == ROOT or not sibling.is_dir():
            continue
        if (sibling / "course.json").exists():
            roots.append(sibling)
    return roots


def topic_dirs() -> Dict[int, Path]:
    """
    {topic_number: directory} for every NN_* folder that has an exercise.py.

    Numbers are global across courses, because a problem id (`NN-MM`) is stored
    on every submission and appears in every URL. Courses claim disjoint ranges
    -- DSA holds 01-22 -- so a second course does not disturb the first.
    """
    out: Dict[int, Path] = {}
    for root in course_roots():
        for p in sorted(root.iterdir()):
            if not p.is_dir():
                continue
            m = TOPIC_RE.match(p.name)
            if m and (p / "exercise.py").exists():
                number = int(m.group(1))
                if number in out:
                    raise RuntimeError(
                        f"topic number {number:02d} is claimed twice: "
                        f"{out[number]} and {p}. Courses must use disjoint "
                        f"ranges, because problem ids are global.")
                out[number] = p
    return out


_ACRONYMS = {"Dsa": "DSA", "Bst": "BST", "Avl": "AVL", "Dp": "DP"}


def topic_title(d: Path) -> str:
    """Human-readable topic name from the directory name."""
    words = d.name.split("_", 1)[1].replace("_", " ").title().split()
    return " ".join(_ACRONYMS.get(w, w) for w in words)


def load_exercise(topic: int):
    """
    Import <topic>/exercise.py and return the module.

    Returns (module, error_string). On success error_string is None.
    """
    dirs = topic_dirs()
    if topic not in dirs:
        return None, f"no topic {topic:02d} found"

    path = dirs[topic] / "exercise.py"
    mod_name = f"_exercise_{topic:02d}"

    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        return None, f"could not load {path}"

    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module

    buf = io.StringIO()
    try:
        # exercise.py prints its whole problem list at import time; hide it.
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            spec.loader.exec_module(module)
    except Exception as exc:                                # noqa: BLE001
        return None, f"{type(exc).__name__} while importing: {exc}"

    return module, None


def resolve(module, target: str):
    """
    Look up "func" or "Class.method" on the module.

    Returns (obj, owner_class_or_None). obj is None when not found.
    """
    if "." in target:
        cls_name, attr = target.split(".", 1)
        cls = getattr(module, cls_name, None)
        if cls is None:
            return None, None
        return getattr(cls, attr, None), cls
    return getattr(module, target, None), None
