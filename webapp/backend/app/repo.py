"""
Bridge to the existing DSA repo.

The whole point of this platform is that it serves the problems and reference
tests that already exist under `python/`, rather than a separate copy that
would immediately drift. Nothing here duplicates problem data; it all comes
from `_harness.catalog` (parsed out of the exercise.py files) and
`_harness.specs` (the reference test suite).
"""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from .settings import REPO_ROOT as _REPO_ROOT
from .settings import settings

# The curriculum location is configuration (FORGE_PYTHON_ROOT), not a fact about
# this file's position on disk -- a container mounts it somewhere else entirely.
REPO_ROOT = _REPO_ROOT
PYTHON_ROOT = settings.python_root

if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from _harness.catalog import Problem, parse_all           # noqa: E402
from _harness.loader import topic_dirs, topic_title       # noqa: E402
from _harness.specs import load_all                       # noqa: E402

# Languages the repo has folders for. Only Python executes today; the rest are
# advertised as unavailable so the UI can show them honestly rather than
# pretending and then failing.
LANGUAGES = [
    {"id": "python", "label": "Python 3", "monaco": "python",
     "ext": "py", "available": True},
    {"id": "javascript", "label": "JavaScript", "monaco": "javascript",
     "ext": "js", "available": False},
    {"id": "typescript", "label": "TypeScript", "monaco": "typescript",
     "ext": "ts", "available": False},
    {"id": "java", "label": "Java", "monaco": "java",
     "ext": "java", "available": False},
    {"id": "cpp", "label": "C++", "monaco": "cpp",
     "ext": "cpp", "available": False},
    {"id": "csharp", "label": "C#", "monaco": "csharp",
     "ext": "cs", "available": False},
    {"id": "go", "label": "Go", "monaco": "go",
     "ext": "go", "available": False},
    {"id": "rust", "label": "Rust", "monaco": "rust",
     "ext": "rs", "available": False},
]

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2, "Challenge": 3}

# Exercise headings are SHOUTED, so they need title-casing for display -- but
# str.title() turns "AVL INSERT" into "Avl Insert" and "DUPLICATE II" into
# "Duplicate Ii". These tokens stay upper.
_KEEP_UPPER = {
    "AVL", "BST", "BFS", "DFS", "DP", "LRU", "LFU", "KMP", "BWT", "RSA",
    "LCS", "LIS", "GCD", "LCM", "XOR", "API", "JSON", "SQL", "URL", "ID",
    "CPU", "RAM", "IO", "LCA", "MST", "RMQ", "BIT", "NP", "FIFO", "LIFO",
    "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "K",
}


def pretty_title(raw: str) -> str:
    """Title-case a shouted heading while preserving acronyms and numerals."""
    letters = [c for c in raw if c.isalpha()]
    # `raw.isupper()` was too strict: "GRAPH COLOURING (m-COLOURABILITY)" has a
    # meaningful lowercase 'm' and was left shouting.
    if not letters or sum(c.isupper() for c in letters) < 0.7 * len(letters):
        return raw

    def fix(token: str) -> str:
        # Split on hyphens and slashes so "K-WAY" and "SERIALIZE/DESERIALIZE"
        # are handled piece by piece.
        for sep in ("-", "/"):
            if sep in token:
                return sep.join(fix(part) for part in token.split(sep))
        bare = token.strip("().,:;'\"")
        if bare in _KEEP_UPPER:
            return token
        if len(bare) == 1:
            # A lone letter is notation -- the 'm' of m-colourability, the 'k'
            # of k-way -- so its case is meaningful.
            return token
        # str.capitalize() uppercases the FIRST character, so "(STREAMING)"
        # came out as "(streaming)". Capitalise the first letter instead.
        low = token.lower()
        for i, ch in enumerate(low):
            if ch.isalpha():
                return low[:i] + ch.upper() + low[i + 1:]
        return low

    return " ".join(fix(t) for t in raw.split())


# --------------------------------------------------------------------- specs

@lru_cache(maxsize=1)
def _spec_index() -> Dict[str, List[Any]]:
    """(topic, problem_num) -> [Spec, ...]  keyed as 'topic:num'."""
    index: Dict[str, List[Any]] = {}
    for topic, specs in load_all().items():
        for sp in specs:
            index.setdefault(f"{topic}:{sp.num}", []).append(sp)
    return index


def specs_for(topic: int, num: int) -> List[Any]:
    return _spec_index().get(f"{topic}:{num}", [])


# ------------------------------------------------------------------ starters

_SIG_RE = re.compile(r"^\s*(def|class)\s+(\w+)\s*(\(.*?\))?\s*(->\s*[^:]+)?:",
                     re.S)


@lru_cache(maxsize=64)
def _exercise_source(topic: int) -> str:
    dirs = topic_dirs()
    if topic not in dirs:
        return ""
    return (dirs[topic] / "exercise.py").read_text(encoding="utf-8")


@lru_cache(maxsize=64)
def _scaffolding(topic: int) -> Any:
    """
    The parts of exercise.py a solution needs but does not write itself.

    Two kinds:

    * top-level imports -- without them a signature like
      `def avl_insert(node: Optional[AVLNode], ...)` raises NameError the
      moment the file is executed, because annotations are evaluated at
      definition time.
    * provided helper classes -- AVLNode, TreeNode and friends, which the
      exercise files hand the learner complete. A class counts as provided
      only when EVERY method has a real body. Accepting "at least one" leaked
      FenwickTree into other problems' starters: its `__init__` is written for
      you but `update` and `prefix_sum` are the exercise.

    Returns (import_block, {class_name: source}).
    """
    import ast
    src = _exercise_source(topic)
    if not src:
        return "", {}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return "", {}

    imports: List[str] = []
    classes: Dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            segment = ast.get_source_segment(src, node)
            if segment:
                imports.append(segment)
        elif isinstance(node, ast.ClassDef):
            methods = [item for item in node.body
                       if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if not methods:
                continue

            def _written(item) -> bool:
                body = [st for st in item.body
                        if not (isinstance(st, ast.Expr)
                                and isinstance(st.value, ast.Constant))]
                return bool(body) and any(not isinstance(st, ast.Pass)
                                          for st in body)

            if all(_written(item) for item in methods):
                segment = ast.get_source_segment(src, node)
                if segment:
                    classes[node.name] = segment
    return "\n".join(imports), classes


def starter_code(topic: int, targets: List[str],
                 needs_scaffold: bool = False) -> str:
    """
    Pull the real signature and TODO hints straight out of exercise.py.

    Learners get the exact stub they would see in the file -- same parameter
    names, same type hints, same guidance comments -- so the browser and the
    filesystem never disagree about what a solution should look like.

    `needs_scaffold` adds the provided helper classes, and is set when the
    problem's tests construct inputs from the learner's own module: those specs
    look up `module.AVLNode`, so a starter without it cannot be graded at all.
    """
    src = _exercise_source(topic)
    if not src:
        return "\n".join(f"def {t}():\n    pass\n" for t in targets)

    lines = src.splitlines()
    blocks: List[str] = []

    for target in targets:
        start = None
        for i, line in enumerate(lines):
            if re.match(rf"^(def|class)\s+{re.escape(target)}\b", line):
                start = i
                break
        if start is None:
            continue

        block = [lines[start]]
        for j in range(start + 1, len(lines)):
            nxt = lines[j]
            # stop at the next top-level statement
            if nxt and not nxt[0].isspace():
                break
            block.append(nxt)
        # trim trailing blank lines
        while block and not block[-1].strip():
            block.pop()
        blocks.append("\n".join(block))

    imports, provided = _scaffolding(topic)
    preamble: List[str] = []
    if imports:
        preamble.append(imports)
    if needs_scaffold:
        wanted = [name for name in provided if name not in targets]
        if wanted:
            preamble.append(
                "# --- provided by the exercise file; the tests build inputs "
                "from this ---")
            preamble.extend(provided[name] for name in wanted)

    header = (
        "# Solve the function(s) below.\n"
        "# The signature and hints come straight from the exercise file.\n"
        "# You may add helper functions or imports above.\n"
    )
    parts = [header] + preamble + blocks
    return "\n\n".join(p.rstrip() for p in parts) + "\n"


# ----------------------------------------------------------------- problems

def _problem_dict(p: Problem, with_detail: bool = False) -> Dict[str, Any]:
    specs = specs_for(p.topic, p.num)
    data: Dict[str, Any] = {
        "id": f"{p.topic:02d}-{p.num:02d}",
        "topic": p.topic,
        "topicName": p.topic_name,
        "num": p.num,
        "title": pretty_title(p.title),
        "rawTitle": p.title,
        "difficulty": p.difficulty,
        "targets": p.unique_targets,
        "tested": bool(specs),
        "testCount": len(specs),
        "drillable": p.drillable,
    }
    if with_detail:
        data.update({
            "inputDesc": p.input_desc,
            "outputDesc": p.output_desc,
            "example": p.example,
            "notes": [sp.note for sp in specs if sp.note],
            "starterCode": {"python": starter_code(
                p.topic, p.unique_targets,
                needs_scaffold=any(sp.build is not None
                                   or sp.build_cases is not None
                                   for sp in specs))},
            "conventions": _conventions(specs),
        })
    return data


def _conventions(specs: List[Any]) -> List[str]:
    """Surface what the reference tests assume, so it is never a guess."""
    out: List[str] = []
    for sp in specs:
        bits = []
        if sp.inplace:
            bits.append("mutates its first argument in place and returns None")
        if sp.prop is not None:
            bits.append("checked by a property, so several answers can be valid")
        if sp.norm is not None:
            bits.append("order-insensitive comparison")
        if sp.tol is not None:
            bits.append(f"floats compared to within {sp.tol}")
        if sp.ref is not None and sp.gen is not None:
            bits.append("also run against randomized inputs")
        if bits:
            out.append(f"{sp.target}: " + "; ".join(bits))
    return out


@lru_cache(maxsize=1)
def all_problems() -> List[Problem]:
    out: List[Problem] = []
    for _, probs in sorted(parse_all().items()):
        out.extend(probs)
    return out


def list_problems() -> List[Dict[str, Any]]:
    return [_problem_dict(p) for p in all_problems()]


def find_problem(problem_id: str) -> Optional[Problem]:
    try:
        topic_s, num_s = problem_id.split("-")
        topic, num = int(topic_s), int(num_s)
    except (ValueError, AttributeError):
        return None
    for p in all_problems():
        if p.topic == topic and p.num == num:
            return p
    return None


def problem_detail(problem_id: str) -> Optional[Dict[str, Any]]:
    p = find_problem(problem_id)
    return _problem_dict(p, with_detail=True) if p else None


def topics() -> List[Dict[str, Any]]:
    dirs = topic_dirs()
    cat = parse_all()
    out = []
    for t in sorted(cat):
        probs = cat[t]
        tested = sum(1 for p in probs if specs_for(t, p.num))
        out.append({
            "topic": t,
            "name": topic_title(dirs[t]) if t in dirs else f"Topic {t}",
            "slug": dirs[t].name if t in dirs else "",
            "problemCount": len(probs),
            "testedCount": tested,
            "level": _level_for(t),
        })
    return out


def _level_for(topic: int) -> str:
    if topic <= 6:
        return "Beginner"
    if topic <= 11:
        return "Intermediate"
    if topic <= 18:
        return "Advanced"
    return "Interview Prep"


def stats() -> Dict[str, Any]:
    probs = all_problems()
    by_diff: Dict[str, int] = {}
    for p in probs:
        by_diff[p.difficulty] = by_diff.get(p.difficulty, 0) + 1
    tested = sum(1 for p in probs if specs_for(p.topic, p.num))
    return {
        "problems": len(probs),
        "topics": len(parse_all()),
        "tested": tested,
        "byDifficulty": by_diff,
        "specCount": sum(len(v) for v in load_all().values()),
    }


def problem_ids() -> List[str]:
    return [f"{p.topic:02d}-{p.num:02d}" for p in all_problems()]


def neighbors(problem_id: str) -> Dict[str, Optional[str]]:
    """
    Previous/next in curriculum order, for the arrows in the solve view.

    Ordering follows the catalogue, so "next" means the next problem in the
    course rather than the next id numerically -- topics do not all have the
    same number of problems.
    """
    ids = problem_ids()
    try:
        i = ids.index(problem_id)
    except ValueError:
        return {"prevId": None, "nextId": None}
    return {"prevId": ids[i - 1] if i > 0 else None,
            "nextId": ids[i + 1] if i + 1 < len(ids) else None}
