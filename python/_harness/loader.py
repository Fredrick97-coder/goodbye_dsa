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

TOPIC_RE = re.compile(r"^(\d{2})_")


def topic_dirs() -> Dict[int, Path]:
    """{topic_number: directory} for every NN_* folder that has an exercise.py."""
    out: Dict[int, Path] = {}
    for p in sorted(ROOT.iterdir()):
        if not p.is_dir():
            continue
        m = TOPIC_RE.match(p.name)
        if m and (p / "exercise.py").exists():
            out[int(m.group(1))] = p
    return out


def topic_title(d: Path) -> str:
    """Human-readable topic name from the directory name."""
    return d.name.split("_", 1)[1].replace("_", " ").title()


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
