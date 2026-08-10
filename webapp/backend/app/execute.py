"""
Run a submission in a child process and collect the report.

SECURITY NOTE, stated plainly: this executes arbitrary Python on the machine
running the server. The child gets a wall-clock timeout, a CPU-time limit and
an address-space limit, which stops runaway loops and memory bombs -- but it
is NOT a sandbox. Nothing prevents a submission from reading your files or
opening a socket.

That is acceptable for a single-user tool bound to 127.0.0.1, which is what
this is. Before this is ever exposed to other people, the child must move
into a real isolation boundary (a container with no network and a read-only
filesystem, gVisor, Firecracker, or a hosted service such as Judge0/Piston).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict

from .repo import PYTHON_ROOT

CHILD = Path(__file__).resolve().parent / "child_runner.py"

DEFAULT_TIMEOUT = 10.0      # wall clock, seconds
DEFAULT_CPU = 5             # CPU seconds inside the child
DEFAULT_MEMORY_MB = 512
MAX_SOURCE_BYTES = 200_000


def run_submission(source: str, topic: int, num: int,
                   mode: str = "test",
                   timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return _fatal("SubmissionTooLarge",
                      f"source exceeds {MAX_SOURCE_BYTES} bytes")

    job = json.dumps({
        "source": source,
        "topic": topic,
        "num": num,
        "mode": mode,
        "cpuSeconds": DEFAULT_CPU,
        "memoryMb": DEFAULT_MEMORY_MB,
    })

    started = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, "-I", str(CHILD), str(PYTHON_ROOT)],
            input=job,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return _fatal(
            "Timeout",
            f"execution exceeded {timeout:.0f}s -- most likely an infinite "
            f"loop, or a solution far slower than the problem allows",
            elapsed_ms=timeout * 1000,
        )

    elapsed_ms = (time.perf_counter() - started) * 1000

    if not proc.stdout.strip():
        detail = (proc.stderr or "").strip()[-1500:]
        rc = proc.returncode

        # A negative return code means the OS killed the child with a signal.
        # SIGXCPU/SIGKILL is what the CPU rlimit produces, and it fires before
        # the wall-clock timeout -- so without this branch a plain infinite
        # loop was reported as "CrashedSilently", which explains nothing.
        if rc is not None and rc < 0:
            signame = {-9: "SIGKILL", -24: "SIGXCPU", -11: "SIGSEGV",
                       -6: "SIGABRT"}.get(rc, f"signal {-rc}")
            if rc in (-9, -24):
                return _fatal(
                    "TimeLimit",
                    f"killed after {DEFAULT_CPU}s of CPU time ({signame}) -- "
                    f"an infinite loop, or a solution too slow for this "
                    f"problem's input sizes",
                    elapsed_ms=elapsed_ms)
            return _fatal("Crashed",
                          f"the process died from {signame}",
                          elapsed_ms=elapsed_ms)

        if "MemoryError" in detail or "Cannot allocate" in detail:
            return _fatal("MemoryLimit",
                          "the process ran out of memory (512 MB cap)",
                          elapsed_ms=elapsed_ms)
        return _fatal("CrashedSilently",
                      detail or "the child process produced no output",
                      elapsed_ms=elapsed_ms)

    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return _fatal("BadReport", proc.stdout[-1500:], elapsed_ms=elapsed_ms)

    report["elapsedMs"] = round(elapsed_ms, 1)
    report["summary"] = _summarise(report)
    return report


def _summarise(report: Dict[str, Any]) -> Dict[str, Any]:
    targets = report.get("targets", [])
    passed = sum(t.get("passed", 0) for t in targets)
    total = sum(t.get("total", 0) for t in targets)
    statuses = [t.get("status") for t in targets]

    if report.get("compileError"):
        verdict = "error"
    elif report.get("untested"):
        verdict = "untested"
    elif not targets:
        verdict = "untested"
    elif all(s == "RAN" for s in statuses):
        verdict = "ran"
    elif any(s == "ERROR" for s in statuses):
        verdict = "error"
    elif any(s == "MISSING" for s in statuses):
        verdict = "missing"
    elif all(s == "PASS" for s in statuses):
        verdict = "accepted"
    elif all(s == "STUB" for s in statuses):
        verdict = "stub"
    else:
        verdict = "failed"

    return {"verdict": verdict, "passed": passed, "total": total,
            "targetCount": len(targets)}


def _fatal(kind: str, message: str, elapsed_ms: float = 0.0) -> Dict[str, Any]:
    return {
        "ok": False,
        "compileError": {"type": kind, "message": message,
                         "line": None, "offset": None, "text": ""},
        "stdout": "",
        "targets": [],
        "elapsedMs": round(elapsed_ms, 1),
        "summary": {"verdict": "error", "passed": 0, "total": 0,
                    "targetCount": 0},
    }
