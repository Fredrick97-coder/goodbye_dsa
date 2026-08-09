"""
Run specs against a learner's exercise.py and classify each problem.

Statuses:
  PASS     every case and every randomized trial matched
  FAIL     produced a wrong answer -- the detail shows the smallest one
  STUB     not implemented yet (returns None / does not mutate)
  ERROR    raised an exception
  MISSING  the function or class is not defined in exercise.py

STUB matters for usability: with ~394 unimplemented stubs, reporting them all
as FAIL would bury the two problems you actually got wrong.
"""

from __future__ import annotations

import contextlib
import copy
import io
import random
from typing import Any, List, Optional, Tuple

from .loader import load_exercise, resolve
from .spec import ERROR, FAIL, MISSING, PASS, STUB, Result, Spec


class _Timeout(Exception):
    pass


def _same(a: Any, b: Any, tol: Optional[float]) -> bool:
    if tol is not None:
        try:
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                return len(a) == len(b) and all(
                    abs(x - y) <= tol for x, y in zip(a, b))
            return abs(a - b) <= tol
        except TypeError:
            return False
    return a == b


def _short(x: Any, limit: int = 60) -> str:
    s = repr(x)
    return s if len(s) <= limit else s[:limit - 3] + "..."


def _call(fn, args, sp: Spec):
    """Invoke the learner's function, isolating stdout and deep-copying args."""
    safe = copy.deepcopy(args)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = fn(*safe)
    if sp.inplace:
        # In-place problems mutate the first argument and return None.
        return safe[0]
    return out


def _run_one(sp: Spec, module) -> Result:
    fn, owner = resolve(module, sp.target)
    if fn is None:
        return Result(sp.num, sp.target, MISSING,
                      "not defined in exercise.py")

    # ---- class-based specs -------------------------------------------------
    if sp.is_class:
        cls = getattr(module, sp.target, None)
        if cls is None:
            return Result(sp.num, sp.target, MISSING, "class not defined")
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                got = sp.script(cls)
        except Exception as exc:                            # noqa: BLE001
            msg = str(exc)
            if isinstance(exc, (TypeError, AttributeError)) and (
                    "NoneType" in msg or "not subscriptable" in msg
                    or "argument" in msg):
                return Result(sp.num, sp.target, STUB, "methods not implemented")
            return Result(sp.num, sp.target, ERROR,
                          f"{type(exc).__name__}: {_short(msg)}")
        want = sp.ref_script() if sp.ref_script else None
        if got is None or (isinstance(got, (list, tuple)) and
                           len(got) and all(v is None for v in got)):
            return Result(sp.num, sp.target, STUB, "methods return None")
        if want is not None and not _same(got, want, sp.tol):
            return Result(sp.num, sp.target, FAIL,
                          f"got {_short(got)}, want {_short(want)}")
        return Result(sp.num, sp.target, PASS, checked=1)

    # ---- fixed cases ------------------------------------------------------
    checked = 0
    all_none = True
    saw_non_none_expected = False

    for args, want in sp.cases:
        try:
            got = _call(fn, args, sp)
        except Exception as exc:                            # noqa: BLE001
            return Result(sp.num, sp.target, ERROR,
                          f"{type(exc).__name__} on {_short(args)}: "
                          f"{_short(str(exc))}")
        if want is not None:
            saw_non_none_expected = True
        if got is not None:
            all_none = False
        norm = sp.norm or (lambda v: v)
        if not _same(norm(got), norm(want), sp.tol):
            if got is None:
                continue      # decide STUB vs FAIL after the loop
            return Result(sp.num, sp.target, FAIL,
                          f"{sp.target}{_short(args)} -> {_short(got)}, "
                          f"expected {_short(want)}")
        checked += 1

    if sp.cases and all_none and saw_non_none_expected:
        return Result(sp.num, sp.target, STUB, "returns None")

    # A case returned None but others did not: that is a real failure.
    if checked < len(sp.cases):
        for args, want in sp.cases:
            try:
                got = _call(fn, args, sp)
            except Exception:                               # noqa: BLE001
                break
            norm = sp.norm or (lambda v: v)
            if not _same(norm(got), norm(want), sp.tol):
                return Result(sp.num, sp.target, FAIL,
                              f"{sp.target}{_short(args)} -> {_short(got)}, "
                              f"expected {_short(want)}")

    # ---- randomized comparison against a reference ------------------------
    if sp.ref and sp.gen:
        rng = random.Random(sp.num * 7919 + 13)
        for _ in range(sp.trials):
            args = sp.gen(rng)
            try:
                got = _call(fn, args, sp)
            except Exception as exc:                        # noqa: BLE001
                return Result(sp.num, sp.target, ERROR,
                              f"{type(exc).__name__} on {_short(args)}: "
                              f"{_short(str(exc))}")
            want = sp.ref(*copy.deepcopy(args))
            if got is None and want is not None:
                return Result(sp.num, sp.target, STUB, "returns None")
            norm = sp.norm or (lambda v: v)
            if not _same(norm(got), norm(want), sp.tol):
                return Result(sp.num, sp.target, FAIL,
                              f"{sp.target}{_short(args)} -> {_short(got)}, "
                              f"expected {_short(want)}")
            checked += 1

    if checked == 0:
        return Result(sp.num, sp.target, STUB, "nothing verifiable ran")
    return Result(sp.num, sp.target, PASS, checked=checked)


def run_topic(topic: int, specs: List[Spec]) -> Tuple[List[Result], Optional[str]]:
    """Run every spec for one topic. Returns (results, import_error)."""
    module, err = load_exercise(topic)
    if err:
        return [], err
    return [_run_one(sp, module) for sp in specs], None
