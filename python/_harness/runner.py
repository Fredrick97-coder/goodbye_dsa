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
import inspect
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
    if sp.accept_inplace and out is None:
        # Some problems read naturally either way -- "reverse a queue" can
        # hand back a new queue or rearrange the one it was given. Grading one
        # contract would fail correct code on a coin flip, so fall back to the
        # mutated argument when nothing was returned.
        return safe[0]
    return out


def _matches(got: Any, want: Any, sp: Spec) -> bool:
    """
    Compare one result against one expectation.

    `prop` is applied to the ACTUAL value only, so `want` can describe a
    property of the output ("is this a valid min-heap?") rather than the
    output itself. `norm` is applied to BOTH, for order-insensitive checks.
    """
    if sp.prop is not None:
        try:
            got = sp.prop(got)
        except Exception:                                   # noqa: BLE001
            return False
    elif sp.norm is not None:
        try:
            got, want = sp.norm(got), sp.norm(want)
        except Exception:                                   # noqa: BLE001
            # An unwritten stub returns None, which most normalisers cannot
            # transform. That is a non-match, not a crash in the harness --
            # `sorted(None)` used to take down the whole run.
            return False
    return _same(got, want, sp.tol)


def _ref_value(sp: Spec, args: tuple):
    """
    What the reference says the answer is.

    For in-place problems the answer is the MUTATED first argument, not the
    return value -- an in-place reference returns None by design.
    """
    safe = copy.deepcopy(args)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = sp.ref(*safe)
    return safe[0] if sp.inplace else out


def _body_is_empty(fn) -> Optional[bool]:
    """
    Is this function still an unwritten stub, judged from its SOURCE?

    Output alone cannot always tell. A transpose that loops over the full row
    range swaps every pair twice and is a perfect no-op -- identical output to
    an empty stub, but the learner did write code and deserves a FAIL with an
    explanation rather than a misleading "not implemented".

    Returns None when the source cannot be read.
    """
    try:
        src = inspect.getsource(fn)
    except (OSError, TypeError):
        return None
    lines = src.splitlines()
    # drop the signature (which may span lines) up to the first colon-ended line
    body: List[str] = []
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if stripped.endswith(":") and (stripped.startswith("def ")
                                           or ")" in stripped):
                started = True
            continue
        if not stripped or stripped.startswith("#"):
            continue
        body.append(stripped)
    if not body:
        return True
    # strip a leading docstring
    if body[0][:3] in ('"""', "'''"):
        quote = body[0][:3]
        if body[0].count(quote) >= 2:
            body = body[1:]
        else:
            for i in range(1, len(body)):
                if quote in body[i]:
                    body = body[i + 1:]
                    break
            else:
                body = []
    real = [b for b in body if b not in ("pass", "...") and
            not b.startswith("#")]
    return not real


def _unimplemented(got: Any, sp: Spec, args: tuple) -> bool:
    """
    Distinguish "not written yet" from "written and wrong".

    A plain `pass` body returns None. For in-place problems it instead leaves
    the argument untouched, so compare against the original input.

    For OBJECT inputs (a linked-list head, a tree root) `==` falls back to
    identity and would always report False -- making an untouched stub look
    like a wrong answer. Compare through whichever transform the spec gave for
    exactly that purpose: `prop` or `norm`. Consulting only `prop` was a bug --
    a spec that used `norm` to read one field off a mutated node reported every
    unwritten stub as a wrong answer instead.
    """
    written = _body_is_empty(_CURRENT_FN[0]) if _CURRENT_FN[0] else None
    if written is False:
        # The learner wrote real code, so nothing here is an unwritten stub.
        return False
    if not (sp.inplace or sp.accept_inplace):
        return got is None
    comparable = sp.prop or sp.norm
    if comparable is not None:
        try:
            return comparable(got) == comparable(args[0])
        except Exception:                                   # noqa: BLE001
            return False
    return got == args[0]


_CURRENT_FN: List[Any] = [None]


def _run_one(sp: Spec, module) -> Result:
    fn, owner = resolve(module, sp.target)
    _CURRENT_FN[0] = fn
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
    stub_hits = 0
    real_progress = 0     # a case that passed AND could not be a stub artefact

    cases = list(sp.cases)
    if sp.build_cases is not None:
        # Cases whose inputs must be constructed from the learner's own
        # classes (a Node chain, a TreeNode tree) rather than written inline.
        try:
            cases += list(sp.build_cases(module))
        except Exception as exc:                            # noqa: BLE001
            return Result(sp.num, sp.target, ERROR,
                          f"could not build inputs: {type(exc).__name__}: "
                          f"{_short(str(exc))}")

    for args, want in cases:
        try:
            got = _call(fn, args, sp)
        except Exception as exc:                            # noqa: BLE001
            return Result(sp.num, sp.target, ERROR,
                          f"{type(exc).__name__} on {_short(args)}: "
                          f"{_short(str(exc))}")
        looks_stubbed = _unimplemented(got, sp, args)
        if _matches(got, want, sp):
            checked += 1
            # A no-op case (input already satisfies the postcondition) is
            # indistinguishable from a stub, so it is not evidence of work.
            if not looks_stubbed:
                real_progress += 1
            continue
        if looks_stubbed:
            stub_hits += 1
            continue
        return Result(sp.num, sp.target, FAIL,
                      f"{sp.target}{_short(args)} -> {_short(got)}, "
                      f"expected {_short(want)}")

    # Nothing proved the function does real work -> it is still a stub.
    if stub_hits and real_progress == 0:
        return Result(sp.num, sp.target, STUB, "not implemented")

    # Some inputs work and others produce nothing: genuinely broken.
    if stub_hits:
        return Result(sp.num, sp.target, FAIL,
                      f"{stub_hits} of {len(cases)} cases produced no "
                      f"result while others worked")

    # ---- randomized comparison against a reference ------------------------
    maker = sp.gen
    if sp.build is not None:
        maker = lambda rng: sp.build(module, rng)   # noqa: E731
    if sp.ref and maker:
        rng = random.Random(sp.num * 7919 + 13)
        for _ in range(sp.trials):
            args = maker(rng)
            try:
                got = _call(fn, args, sp)
            except Exception as exc:                        # noqa: BLE001
                return Result(sp.num, sp.target, ERROR,
                              f"{type(exc).__name__} on {_short(args)}: "
                              f"{_short(str(exc))}")
            want = _ref_value(sp, args)
            if _matches(got, want, sp):
                checked += 1
                if not _unimplemented(got, sp, args):
                    real_progress += 1
                continue
            if _unimplemented(got, sp, args):
                return Result(sp.num, sp.target, STUB, "not implemented")
            return Result(sp.num, sp.target, FAIL,
                          f"{sp.target}{_short(args)} -> {_short(got)}, "
                          f"expected {_short(want)}")

    if checked == 0:
        return Result(sp.num, sp.target, STUB, "nothing verifiable ran")

    # Everything matched, but nothing matched in a way an empty stub could not
    # have faked. This happens when a spec's only expected answer is None --
    # `graph_colouring` on a graph that is not m-colourable, for instance.
    # Calling that PASS would tell the learner they had solved a problem they
    # had not opened.
    if real_progress == 0:
        return Result(sp.num, sp.target, STUB, "not implemented")

    return Result(sp.num, sp.target, PASS, checked=checked)


def run_topic(topic: int, specs: List[Spec]) -> Tuple[List[Result], Optional[str]]:
    """Run every spec for one topic. Returns (results, import_error)."""
    module, err = load_exercise(topic)
    if err:
        return [], err
    return [_run_one(sp, module) for sp in specs], None
