"""
The plain subprocess backend: fast, portable, and NOT a sandbox.

It applies a wall-clock timeout, a CPU-time rlimit and an address-space rlimit,
so runaway loops and memory bombs are contained. Nothing stops the submitted
code from reading files or opening a socket -- it runs as the server user.

Fine for a single developer on 127.0.0.1, which is why it stays the default in
`dev`. `settings.check_safety` refuses to start `prod` on it.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from ..settings import settings
from .base import Job, RawResult, now_ms

CHILD = Path(__file__).resolve().parents[1] / "child_runner.py"


class LocalExecutor:
    name = "local"
    safe_for_untrusted = False

    def run(self, job: Job) -> RawResult:
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                # -I: isolated mode. Ignores PYTHONPATH and the user site
                # directory, so a submission cannot be influenced by whatever
                # happens to be installed for the server user.
                [sys.executable, "-I", str(CHILD), str(settings.python_root)],
                input=job.payload(),
                capture_output=True,
                text=True,
                timeout=settings.exec_wall_seconds,
            )
        except subprocess.TimeoutExpired:
            return RawResult("", "", None,
                             settings.exec_wall_seconds * 1000, timed_out=True)
        return RawResult(proc.stdout, proc.stderr, proc.returncode,
                         now_ms(started))


def availability() -> tuple:
    """Always usable -- it is the fallback everything else degrades to."""
    return True, "subprocess with rlimits (not a sandbox)"
