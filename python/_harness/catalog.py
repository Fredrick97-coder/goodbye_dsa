"""
Extract problem metadata from the exercise.py files themselves.

The exercise files already state, in a consistent shape:

    print("\\n[MEDIUM PROBLEMS]")
    print("\\n7. SUBSETS WITH DUPLICATES")
    print("Input: A list that may contain repeats")
    print("Output: All UNIQUE subsets")
    print("Example: [1,2,2] -> ...")
    def subsets_with_dup(nums): ...

So the exercise files stay the single source of truth. Parsing them means the
drill can never drift out of sync with the problems, which a hand-maintained
catalogue would do immediately.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .loader import topic_dirs, topic_title

_SECTION = re.compile(r'print\(\s*"\\n*\[([A-Z /]+?)\s*PROBLEMS?\]"')
_SECTION_ALT = re.compile(r'print\(\s*"\\n*\[([A-Z /-]+?)\]"')
_HEADING = re.compile(r'print\(\s*"\\n(\d+)\.\s+(.+?)"\s*\)')
_FIELD = re.compile(r'print\(\s*"(Input|Output|Example):\s*(.*?)"\s*\)')
_DEF = re.compile(r'^(?:def|class)\s+(\w+)', re.M)


@dataclass
class Problem:
    topic: int
    topic_name: str
    num: int
    title: str
    difficulty: str
    input_desc: str = ""
    output_desc: str = ""
    example: str = ""
    targets: List[str] = None      # function/class names that follow

    def __post_init__(self):
        if self.targets is None:
            self.targets = []

    @property
    def label(self) -> str:
        return f"{self.topic:02d}.{self.num:02d}"


def _difficulty_from(raw: str) -> str:
    r = raw.strip().upper()
    for key in ("EASY", "MEDIUM", "HARD", "CHALLENGE"):
        if key in r:
            return key.capitalize()
    return "Unknown"


def parse_topic(topic: int) -> List[Problem]:
    dirs = topic_dirs()
    if topic not in dirs:
        return []
    path: Path = dirs[topic] / "exercise.py"
    src = path.read_text(encoding="utf-8")
    name = topic_title(dirs[topic])

    # Walk the source line by line so ordering is preserved.
    problems: List[Problem] = []
    difficulty = "Unknown"
    current: Optional[Problem] = None

    for line in src.splitlines():
        sec = _SECTION.search(line) or _SECTION_ALT.search(line)
        if sec:
            d = _difficulty_from(sec.group(1))
            if d != "Unknown":
                difficulty = d
            continue

        head = _HEADING.search(line)
        if head:
            current = Problem(
                topic=topic, topic_name=name,
                num=int(head.group(1)),
                title=head.group(2).strip(),
                difficulty=difficulty,
            )
            problems.append(current)
            continue

        if current is not None:
            f = _FIELD.search(line)
            if f:
                key, val = f.group(1).lower(), f.group(2).strip()
                if key == "input":
                    current.input_desc = val
                elif key == "output":
                    current.output_desc = val
                else:
                    current.example = val
                continue
            d = _DEF.match(line)
            if d:
                current.targets.append(d.group(1))

    return problems


def parse_all() -> Dict[int, List[Problem]]:
    return {t: parse_topic(t) for t in sorted(topic_dirs())}


def flat_all() -> List[Problem]:
    out: List[Problem] = []
    for _, probs in sorted(parse_all().items()):
        out.extend(probs)
    return out
