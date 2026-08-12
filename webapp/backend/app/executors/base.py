"""
The contract every execution backend implements, and the shared report shaping.

An executor takes a job (source, which problem, run-or-grade) and returns the
report JSON that `child_runner.py` emits. Everything that differs between
backends -- how the child is isolated -- lives in the backend; everything that
must not differ -- limits, verdict derivation, error shaping -- lives here.

That split matters because the verdict rules are load-bearing for the whole
platform: "Not Attempted" versus "Wrong Answer" is decided from this data, and
having two backends disagree about it would be a silent grading bug.
"""

from __future__ import annotations

import json
import time
import contextlib
import os
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, Protocol

from ..settings import settings


@dataclass(frozen=True)
class Job:
    source: str
    topic: int
    num: int
    mode: str = "test"
    language: str = "python"
    #: The language-neutral test plan. Required by drivers that cannot run the
    #: Python specs themselves; the Python driver ignores it and loads them.
    plan: Optional[Dict[str, Any]] = None
    #: Filename the source is staged as, e.g. solution.mts. The extension is
    #: load-bearing for some runtimes -- Node reads .mts as ES-module
    #: TypeScript and a bare .ts as CommonJS, which fails on the first export.
    filename: str = "solution.py"

    def payload(self, source_path: str) -> str:
        """
        What the driver reads on stdin.

        `sourceFile` is a path the driver can import directly. The PARENT writes
        it, not the driver: under the Seatbelt profile nothing may write to disk
        at all, so a driver that had to create its own temp file could not run
        sandboxed.
        """
        return json.dumps({
            "source": self.source,
            "sourceFile": source_path,
            "topic": self.topic,
            "num": self.num,
            "mode": self.mode,
            "language": self.language,
            "plan": self.plan,
            "cpuSeconds": settings.exec_cpu_seconds,
            "memoryMb": settings.exec_memory_mb,
            "maxStdoutBytes": settings.exec_max_stdout_bytes,
        })


@dataclass
class RawResult:
    """What a backend produces, before it becomes a report."""
    stdout: str
    stderr: str
    returncode: Optional[int]
    elapsed_ms: float
    timed_out: bool = False
    oom_killed: bool = False


class Executor(Protocol):
    name: str

    def run(self, job: Job) -> RawResult: ...


@contextlib.contextmanager
def staged(job: Job) -> Iterator[tuple]:
    """
    Write the submission to a throwaway directory. Yields (dir, file).

    Mode 0o755 on the directory and 0o644 on the file because the container runs
    as uid 65534, which is not the uid that created them -- default 0o700 would
    make the mount unreadable and every submission would fail to import.
    """
    tmp = tempfile.mkdtemp(prefix="forge-src-")
    try:
        os.chmod(tmp, 0o755)
        path = os.path.join(tmp, job.filename)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(job.source)
        os.chmod(path, 0o644)
        yield tmp, path
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ shaping

SIGNALS = {-9: "SIGKILL", -24: "SIGXCPU", -11: "SIGSEGV", -6: "SIGABRT",
           -15: "SIGTERM", -4: "SIGILL", -8: "SIGFPE"}


def to_report(result: RawResult, executor: str) -> Dict[str, Any]:
    """Turn a backend's raw output into the report the API returns."""
    if result.timed_out:
        return fatal(
            "Timeout",
            f"execution exceeded {settings.exec_wall_seconds:.0f}s -- most "
            f"likely an infinite loop, or a solution far slower than the "
            f"problem allows",
            elapsed_ms=result.elapsed_ms, executor=executor)

    if result.oom_killed:
        return fatal(
            "MemoryLimit",
            f"the process exceeded its {settings.exec_memory_mb} MB memory cap",
            elapsed_ms=result.elapsed_ms, executor=executor)

    if not result.stdout.strip():
        detail = (result.stderr or "").strip()[-1500:]
        rc = result.returncode

        # A negative return code means a signal killed the child. SIGXCPU or
        # SIGKILL is what the CPU rlimit produces, and it fires before the
        # wall-clock timeout -- without this branch a plain infinite loop was
        # reported as "CrashedSilently", which explains nothing.
        if rc is not None and rc < 0:
            signame = SIGNALS.get(rc, f"signal {-rc}")
            if rc in (-9, -24):
                return fatal(
                    "TimeLimit",
                    f"killed after {settings.exec_cpu_seconds}s of CPU time "
                    f"({signame}) -- an infinite loop, or a solution too slow "
                    f"for this problem's input sizes",
                    elapsed_ms=result.elapsed_ms, executor=executor)
            return fatal("Crashed", f"the process died from {signame}",
                         elapsed_ms=result.elapsed_ms, executor=executor)

        # Containers report the same conditions through the exit code, because
        # the kill happens inside the container rather than to the child the
        # parent spawned.
        #
        # 137 is SIGKILL. Measured on this stack, a pure CPU loop in the
        # container exits 137 with `OOMKilled=false`, while an actual memory
        # bomb exits 0 -- the child's own RLIMIT_AS raises MemoryError first and
        # the harness reports it per-case. So 137 means the CPU hard limit far
        # more often than it means memory, and an earlier version of this branch
        # labelled every infinite loop a "MemoryLimit". Distinguishing them for
        # certain needs `docker inspect .State.OOMKilled`, which costs two extra
        # daemon round trips on every submission -- not worth it to refine a
        # message that already names both causes.
        if rc == 137:
            return fatal(
                "TimeLimit",
                f"killed (exit 137) after exceeding its limits -- "
                f"{settings.exec_cpu_seconds}s of CPU time, or the "
                f"{settings.exec_memory_mb} MB memory cap",
                elapsed_ms=result.elapsed_ms, executor=executor)
        if rc == 152:
            return fatal(
                "TimeLimit",
                f"killed (exit 152 / SIGXCPU) after "
                f"{settings.exec_cpu_seconds}s of CPU time",
                elapsed_ms=result.elapsed_ms, executor=executor)

        if "MemoryError" in detail or "Cannot allocate" in detail:
            return fatal("MemoryLimit",
                         f"the process ran out of memory "
                         f"({settings.exec_memory_mb} MB cap)",
                         elapsed_ms=result.elapsed_ms, executor=executor)
        return fatal("CrashedSilently",
                     detail or "the child process produced no output",
                     elapsed_ms=result.elapsed_ms, executor=executor)

    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        return fatal("BadReport", result.stdout[-1500:],
                     elapsed_ms=result.elapsed_ms, executor=executor)

    report["elapsedMs"] = round(result.elapsed_ms, 1)
    report["summary"] = summarise(report)
    report["executor"] = executor
    return report


def summarise(report: Dict[str, Any]) -> Dict[str, Any]:
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


def fatal(kind: str, message: str, elapsed_ms: float = 0.0,
          executor: str = "") -> Dict[str, Any]:
    return {
        "ok": False,
        "compileError": {"type": kind, "message": message,
                         "line": None, "offset": None, "text": ""},
        "stdout": "",
        "targets": [],
        "elapsedMs": round(elapsed_ms, 1),
        "executor": executor,
        "summary": {"verdict": "error", "passed": 0, "total": 0,
                    "targetCount": 0},
    }


def now_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000
