"""
Runs ONE submission, inside its own short-lived process.

Invoked as:  python child_runner.py <python_root>
with a JSON job on stdin and a JSON report on stdout.

It lives in a separate process for three reasons:
  1. an infinite loop in the submission cannot hang the API server
  2. a crash or a segfault takes down only the child
  3. CPU and memory limits can be applied to the child alone

It is NOT a security sandbox. See the note in execute.py.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import random
import sys
import traceback
from typing import Any, Dict, List

MAX_RANDOM_TRIALS = 40      # keep response times snappy; check.py uses 150
REPR_LIMIT = 220


def _short(value: Any, limit: int = REPR_LIMIT) -> str:
    try:
        text = repr(value)
    except Exception:                                       # noqa: BLE001
        text = f"<unreprable {type(value).__name__}>"
    return text if len(text) <= limit else text[: limit - 3] + "..."


def empty_bodies(source: str) -> Dict[str, bool]:
    """
    Which top-level defs are still unwritten, judged from the AST?

    `inspect.getsource` is useless here: the submission arrives as a string
    and is exec'd, so there is no file for inspect to read. Parsing the source
    tells us definitively whether a body is just `pass` / `...` / a docstring,
    which is what separates "not attempted" from "attempted and wrong".
    """
    import ast
    out: Dict[str, bool] = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = list(node.body)
        if body and isinstance(body[0], ast.Expr) and \
                isinstance(body[0].value, ast.Constant) and \
                isinstance(body[0].value.value, str):
            body = body[1:]              # drop the docstring
        out[node.name] = all(
            isinstance(stmt, ast.Pass)
            or (isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and stmt.value.value is Ellipsis)
            for stmt in body
        )
    return out


def _apply_limits(cpu_seconds: int = 5, address_space_mb: int = 512) -> None:
    try:
        import resource
    except ImportError:                                     # Windows
        return
    try:
        resource.setrlimit(resource.RLIMIT_CPU,
                           (cpu_seconds, cpu_seconds + 1))
        limit = address_space_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except (ValueError, OSError):
        pass


def main() -> int:
    python_root = sys.argv[1]
    if python_root not in sys.path:
        sys.path.insert(0, python_root)

    job = json.load(sys.stdin)
    source: str = job["source"]
    topic: int = job["topic"]
    num: int = job["num"]
    mode: str = job.get("mode", "test")        # "test" | "run"

    _apply_limits(job.get("cpuSeconds", 5), job.get("memoryMb", 512))

    from _harness.runner import _matches, _ref_value  # noqa
    from _harness.specs import load_topic

    report: Dict[str, Any] = {
        "ok": True,
        "compileError": None,
        "stdout": "",
        "targets": [],
    }

    # ---- 1. execute the submission ---------------------------------------
    namespace: Dict[str, Any] = {"__name__": "__submission__"}
    stdout_buffer = io.StringIO()
    try:
        compiled = compile(source, "<submission>", "exec")
    except SyntaxError as exc:
        report["ok"] = False
        report["compileError"] = {
            "type": "SyntaxError",
            "message": str(exc.msg),
            "line": exc.lineno,
            "offset": exc.offset,
            "text": (exc.text or "").rstrip(),
        }
        print(json.dumps(report))
        return 0

    try:
        with contextlib.redirect_stdout(stdout_buffer), \
                contextlib.redirect_stderr(stdout_buffer):
            exec(compiled, namespace)
    except Exception as exc:                                # noqa: BLE001
        report["ok"] = False
        report["compileError"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "line": None,
            "offset": None,
            "text": "",
            "traceback": traceback.format_exc(limit=3),
        }
        report["stdout"] = stdout_buffer.getvalue()[:8000]
        print(json.dumps(report))
        return 0

    report["stdout"] = stdout_buffer.getvalue()[:8000]

    if mode == "run":
        # "Run" just executes the file and shows output -- no grading.
        report["targets"] = [{
            "target": "(run)", "status": "RAN", "cases": [],
            "passed": 0, "total": 0, "note": "",
        }]
        print(json.dumps(report))
        return 0

    # ---- 2. grade against the repo's reference specs ---------------------
    specs = [sp for sp in load_topic(topic) if sp.num == num]
    if not specs:
        report["targets"] = []
        report["untested"] = True
        print(json.dumps(report))
        return 0

    stubs = empty_bodies(source)
    for sp in specs:
        report["targets"].append(_grade(sp, namespace, _matches,
                                        _ref_value, stubs))

    print(json.dumps(report))
    return 0


class _NamespaceView:
    """
    Attribute access over the submission's globals.

    Specs that construct inputs from the learner's own classes call
    `module.Node` / `module.TreeNode` -- attribute access, because in check.py
    they receive a real module. A submission is just a dict, so it needs this
    shim; without it those specs raised AttributeError and were silently
    skipped, reporting 0 cases run.
    """

    __slots__ = ("_ns",)

    def __init__(self, ns: Dict[str, Any]):
        self._ns = ns

    def __getattr__(self, name: str) -> Any:
        try:
            return self._ns[name]
        except KeyError:
            raise AttributeError(
                f"your code does not define {name!r}, which this problem's "
                f"tests need in order to build inputs") from None

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Writes land in the submission's globals.

        Some problems assume a helper exists that the exercise file never
        defines -- `first_bad_version` is handed an `is_bad_version(v)` oracle
        the way LeetCode hands you one. The spec injects it by setting an
        attribute on the module, so that has to reach the namespace the
        submission actually runs in.
        """
        if name == "_ns":
            object.__setattr__(self, name, value)
        else:
            self._ns[name] = value


def _resolve(namespace: Dict[str, Any], target: str):
    if "." in target:
        cls_name, attr = target.split(".", 1)
        cls = namespace.get(cls_name)
        return (getattr(cls, attr, None) if cls else None), cls
    return namespace.get(target), None


def _mutating(sp) -> bool:
    """Does an unwritten stub of this problem show up as an untouched input?"""
    return bool(sp.inplace or getattr(sp, "accept_inplace", False))


def _looks_stubbed(sp, got, args) -> bool:
    """
    Mirrors runner._unimplemented: did this call leave the input untouched?

    Objects compare by identity, so a mutated-in-place tree node has to be
    read through the spec's own `prop`/`norm` transform to be comparable at
    all -- otherwise every unwritten stub reads as a wrong answer.
    """
    if got is None:
        return True
    if not _mutating(sp):
        return False
    comparable = sp.prop or sp.norm
    if comparable is not None:
        try:
            return comparable(got) == comparable(args[0])
        except Exception:                                   # noqa: BLE001
            return False
    return got == args[0]


def _grade(sp, namespace, _matches, _ref_value, stubs) -> Dict[str, Any]:
    """Run one spec and return every case outcome, not just the first failure."""
    out: Dict[str, Any] = {
        "target": sp.target,
        "note": sp.note or "",
        "cases": [],
        "passed": 0,
        "total": 0,
        "status": "PASS",
    }

    # class-based specs (Stack, MinStack, Trie, MedianFinder, ...)
    if sp.is_class:
        cls = namespace.get(sp.target)
        if cls is None:
            out["status"] = "MISSING"
            out["cases"].append({
                "name": sp.target, "passed": False,
                "input": "", "expected": "", "got": "",
                "error": f"class {sp.target} is not defined",
            })
            out["total"] = 1
            return out
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                got = sp.script(cls)
        except Exception as exc:                            # noqa: BLE001
            message = str(exc)
            # Unimplemented methods return None, so the script blows up on the
            # first thing it does with the result. That is "not attempted", not
            # a wrong answer -- mirroring runner._run_one.
            if isinstance(exc, (TypeError, AttributeError)) and (
                    "NoneType" in message or "not subscriptable" in message
                    or "argument" in message):
                out["status"] = "STUB"
                out["cases"].append({
                    "name": "method sequence", "passed": False,
                    "input": sp.note or "scripted calls",
                    "expected": "", "got": "",
                    "error": "methods are not implemented yet",
                })
            else:
                out["status"] = "ERROR"
                out["cases"].append({
                    "name": "method sequence", "passed": False,
                    "input": sp.note or "scripted calls",
                    "expected": "", "got": "",
                    "error": f"{type(exc).__name__}: {exc}",
                })
            out["total"] = 1
            return out

        # A script whose every observed value is None means the methods still
        # return nothing. Reporting that as Wrong Answer told every learner
        # opening a class problem that their untouched starter was incorrect.
        if got is None or (isinstance(got, (list, tuple)) and len(got)
                           and all(v is None for v in got)):
            out["status"] = "STUB"
            out["total"] = 1
            out["cases"].append({
                "name": "method sequence", "passed": False,
                "input": sp.note or "scripted calls",
                "expected": _short(sp.ref_script() if sp.ref_script else None),
                "got": _short(got),
                "error": "every method returned None -- not implemented yet",
            })
            return out

        want = sp.ref_script() if sp.ref_script else None
        ok = want is None or got == want
        out["cases"].append({
            "name": "method sequence", "passed": bool(ok),
            "input": sp.note or "scripted calls",
            "expected": _short(want), "got": _short(got), "error": "",
        })
        out["total"] = 1
        out["passed"] = 1 if ok else 0
        out["status"] = "PASS" if ok else "FAIL"
        return out

    fn, _owner = _resolve(namespace, sp.target)
    if fn is None:
        out["status"] = "MISSING"
        out["cases"].append({
            "name": sp.target, "passed": False,
            "input": "", "expected": "", "got": "",
            "error": f"{sp.target} is not defined in your code",
        })
        out["total"] = 1
        return out

    body_empty = stubs.get(sp.target.split('.')[0], False)

    def invoke(args):
        safe = copy.deepcopy(args)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = fn(*safe)
        if sp.inplace:
            return safe[0]
        # accept_inplace: either contract passes -- see runner._call
        if getattr(sp, "accept_inplace", False) and result is None:
            return safe[0]
        return result

    # --- fixed cases ---
    cases = list(sp.cases)
    if sp.build_cases is not None:
        try:
            cases += list(sp.build_cases(_NamespaceView(namespace)))
        except Exception as exc:                            # noqa: BLE001
            out["cases"].append({
                "name": "test setup", "passed": False,
                "input": "", "expected": "", "got": "",
                "error": f"could not build inputs -- {exc}",
            })
            out["total"] += 1
            out["status"] = "ERROR"
            return out

    stub_like = 0
    real_progress = 0     # a pass that an empty stub could not have produced
    for idx, (args, want) in enumerate(cases, 1):
        entry = {
            "name": f"case {idx}",
            "input": _short(args[0] if len(args) == 1 else args),
            "expected": _short(want),
            "got": "", "passed": False, "error": "",
        }
        try:
            got = invoke(args)
        except Exception as exc:                            # noqa: BLE001
            entry["error"] = f"{type(exc).__name__}: {exc}"
            out["cases"].append(entry)
            out["total"] += 1
            out["status"] = "ERROR"
            continue

        entry["got"] = _short(got)
        if _matches(got, want, sp):
            entry["passed"] = True
            out["passed"] += 1
            if not _looks_stubbed(sp, got, args):
                real_progress += 1
        elif _looks_stubbed(sp, got, args):
            stub_like += 1
        out["total"] += 1
        out["cases"].append(entry)

    # --- randomized trials against the reference ---
    if sp.ref and (sp.gen or sp.build):
        rng = random.Random(sp.num * 7919 + 13)
        view = _NamespaceView(namespace)
        maker = sp.gen if sp.gen else (lambda r: sp.build(view, r))
        failures_shown = 0
        for trial in range(1, MAX_RANDOM_TRIALS + 1):
            try:
                args = maker(rng)
            except Exception as exc:                        # noqa: BLE001
                # Input construction failed -- almost always a helper class
                # the problem needs (Node, TreeNode) that the submission has
                # not defined. Say so instead of reporting a bare 0/0.
                if trial == 1:
                    out["cases"].append({
                        "name": "test setup", "passed": False,
                        "input": "", "expected": "", "got": "",
                        "error": f"could not build inputs -- {exc}",
                    })
                    out["total"] += 1
                    out["status"] = "ERROR"
                break
            try:
                got = invoke(args)
                want = _ref_value(sp, args)
            except Exception as exc:                        # noqa: BLE001
                out["total"] += 1
                out["status"] = "ERROR"
                if failures_shown < 3:
                    failures_shown += 1
                    out["cases"].append({
                        "name": f"random trial {trial}",
                        "input": _short(args[0] if len(args) == 1 else args),
                        "expected": "", "got": "",
                        "passed": False,
                        "error": f"{type(exc).__name__}: {exc}",
                    })
                continue

            out["total"] += 1
            if _matches(got, want, sp):
                out["passed"] += 1
                if not _looks_stubbed(sp, got, args):
                    real_progress += 1
            else:
                if _looks_stubbed(sp, got, args):
                    stub_like += 1
                if failures_shown < 3:
                    failures_shown += 1
                    out["cases"].append({
                        "name": f"random trial {trial}",
                        "input": _short(args[0] if len(args) == 1 else args),
                        "expected": _short(want),
                        "got": _short(got),
                        "passed": False, "error": "",
                    })

    # --- verdict ---
    if out["status"] != "ERROR":
        if out["passed"] == out["total"] and out["total"] > 0:
            # ...unless nothing that passed required an implementation. A spec
            # whose only expected answer is None is satisfied by untouched
            # starter code, and calling that Accepted would be a lie.
            out["status"] = "STUB" if (body_empty and real_progress == 0) \
                else "PASS"
        elif body_empty and stub_like:
            out["status"] = "STUB"
        else:
            out["status"] = "FAIL"
    return out


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:                                       # noqa: BLE001
        # Never emit anything but JSON on stdout -- the parent parses it.
        print(json.dumps({
            "ok": False,
            "compileError": {
                "type": "HarnessError",
                "message": traceback.format_exc(limit=4),
                "line": None, "offset": None, "text": "",
            },
            "stdout": "", "targets": [],
        }))
