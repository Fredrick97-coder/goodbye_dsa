"""
Turn a Python spec into a language-agnostic test plan.

This is what makes a second language possible without writing a second test
suite. The specs are Python -- they call `math.comb`, they use `itertools`, they
compare against brute-force references written as Python functions -- so they
cannot grade TypeScript directly. But for most problems the *data* is ordinary
JSON, and the Python reference can compute the expected answers ahead of time.

So: run the reference here, serialise `(args, expected)` pairs, and hand that to
a runner in any language. The Python reference stays the single source of truth,
and a TypeScript solution is graded against exactly the same expectations as a
Python one.

Not every spec survives the crossing, and the honest ones are excluded rather
than approximated:

* **class method sequences** -- the script is a Python lambda calling methods
* **inputs built from the learner's own classes** -- a `TreeNode` in their
  Python file is not a `TreeNode` in their TypeScript file
* **property checks** -- "is this a valid min-heap?" is a Python predicate
* **custom normalisers** -- a one-off lambda cannot be sent over the wire

`portability()` reports which of those applies, so the UI can say *why* a
problem is Python-only instead of just hiding the option.
"""

from __future__ import annotations

import json
import random
from typing import Any, Dict, List, Optional, Tuple

from . import spec as specmod
from .runner import _ref_value
from .spec import Spec

#: Comparison modes a runner in any language must implement. Deliberately tiny:
#: every mode here has an obvious implementation in any language, which is what
#: keeps two runners from disagreeing about whether an answer is correct.
COMPARE_MODES = ("exact", "sorted", "sorted_pairs", "sorted_inner")

_NAMED_NORMS = {
    id(specmod.as_sorted): "sorted",
    id(specmod.as_set_of_tuples): "sorted_pairs",
    id(specmod.as_sorted_inner): "sorted_inner",
}

#: How many randomised trials go into a plan. Fewer than check.py's 150: these
#: are generated per submission and shipped as JSON, so the size matters, and 40
#: seeded trials already catch what a handful of fixed cases miss.
TRIALS = 40

#: Fixed, so a plan is reproducible. A learner re-submitting the same code gets
#: the same cases, which makes "it passed a minute ago" a real statement.
SEED = 8_675_309


def _jsonable(value: Any) -> bool:
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False


def portability(sp: Spec) -> Tuple[Optional[str], Optional[str]]:
    """
    (compare_mode, reason_it_cannot_travel). Exactly one is None.
    """
    if sp.is_class:
        return None, "the test drives a class through a sequence of method calls"
    if sp.build is not None or sp.build_cases is not None:
        return None, "the test builds inputs from your own classes"
    if sp.prop is not None:
        return None, "the answer is checked by a Python property, not compared"

    mode = "exact"
    if sp.norm is not None:
        mode = _NAMED_NORMS.get(id(sp.norm))
        if mode is None:
            return None, "this problem uses a comparison written in Python"

    if sp.cases and not all(_jsonable(args) and _jsonable(want)
                            for args, want in sp.cases):
        return None, "the example data cannot be represented as JSON"

    if sp.gen is not None:
        try:
            if not _jsonable(sp.gen(random.Random(SEED))):
                return None, "the generated inputs cannot be represented as JSON"
        except Exception:                                   # noqa: BLE001
            return None, "the input generator failed"
    elif not sp.cases:
        return None, "there is nothing to serialise"

    return mode, None


def _tuples_to_lists(value: Any) -> Any:
    """
    JSON has one sequence type, so a tuple and a list must not be distinguished.

    Python references return tuples all over the place (`(0, 3)` for an index
    pair); JSON turns those into arrays, and a TypeScript solution can only ever
    produce arrays. Normalising here means the comparison is about the answer,
    not about which sequence type the reference happened to use.
    """
    if isinstance(value, tuple):
        return [_tuples_to_lists(v) for v in value]
    if isinstance(value, list):
        return [_tuples_to_lists(v) for v in value]
    if isinstance(value, dict):
        return {k: _tuples_to_lists(v) for k, v in value.items()}
    if isinstance(value, set):
        return sorted(_tuples_to_lists(v) for v in value)
    return value


def plan_for_spec(sp: Spec) -> Optional[Dict[str, Any]]:
    """One target's cases, with expected answers computed by the Python ref."""
    mode, reason = portability(sp)
    if mode is None:
        return None

    cases: List[Dict[str, Any]] = []

    for args, want in sp.cases:
        cases.append({"args": _tuples_to_lists(list(args)),
                      "expected": _tuples_to_lists(want)})

    if sp.ref is not None and sp.gen is not None:
        rng = random.Random(SEED)
        for _ in range(TRIALS):
            try:
                args = sp.gen(rng)
                want = _ref_value(sp, args)
            except Exception:                               # noqa: BLE001
                # A generator or reference that throws on an edge case is not a
                # reason to fail the learner; drop the trial and keep going.
                continue
            cases.append({"args": _tuples_to_lists(list(args)),
                          "expected": _tuples_to_lists(want)})

    if not cases:
        return None

    return {
        "name": sp.target,
        "compare": mode,
        "tol": sp.tol,
        "inplace": bool(sp.inplace),
        "note": sp.note or "",
        "cases": cases,
    }


def plan_for_problem(topic: int, num: int, specs: List[Spec]) -> Dict[str, Any]:
    """
    The full plan for one problem, plus what had to be left out.

    A problem with any excluded target is reported as partial rather than
    silently graded on half its requirements -- being told "8 of 8 passed" when
    two functions were never run would be worse than being told nothing.
    """
    targets: List[Dict[str, Any]] = []
    excluded: List[Dict[str, str]] = []

    for sp in specs:
        if sp.num != num:
            continue
        plan = plan_for_spec(sp)
        if plan is None:
            _, reason = portability(sp)
            excluded.append({"name": sp.target,
                             "reason": reason or "not portable"})
        else:
            targets.append(plan)

    return {
        "problemId": f"{topic:02d}-{num:02d}",
        "targets": targets,
        "excluded": excluded,
        "complete": bool(targets) and not excluded,
    }


def problem_support(topic: int, num: int, specs: List[Spec]) -> Dict[str, Any]:
    """
    Cheap check for "can this problem be solved in another language?".

    Deliberately does not compute expected answers -- the problem list asks this
    for all 342 problems at once, and running every reference forty times to
    render a dropdown would be absurd.
    """
    portable, blocked = [], []
    for sp in specs:
        if sp.num != num:
            continue
        mode, reason = portability(sp)
        (portable if mode else blocked).append(
            sp.target if mode else {"name": sp.target, "reason": reason})
    return {
        "portable": portable,
        "blocked": blocked,
        "complete": bool(portable) and not blocked,
    }
