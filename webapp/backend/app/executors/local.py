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

from .. import languages
from ..settings import settings
from .base import Job, RawResult, now_ms, staged

RUNNERS = Path(__file__).resolve().parents[1] / "runners"


class LocalExecutor:
    name = "local"
    safe_for_untrusted = False

    def run(self, job: Job) -> RawResult:
        lang = languages.get(job.language)
        if lang is None or not lang.implemented:
            return RawResult("", f"no driver for {job.language}", 1, 0.0)

        started = time.perf_counter()
        with staged(job) as (workdir, source_path):
            argv = languages.resolve_command(
                lang,
                driver=str(RUNNERS / lang.driver),
                python_root=str(settings.python_root),
                workdir=workdir,
                # -I (isolated) is in the Python row's template: it ignores
                # PYTHONPATH and the user site directory, so a submission cannot
                # be influenced by whatever is installed for the server user.
                python=sys.executable,
            )
            try:
                proc = subprocess.run(
                    argv, input=job.payload(source_path),
                    capture_output=True, text=True,
                    timeout=settings.exec_wall_seconds,
                )
            except subprocess.TimeoutExpired:
                return RawResult("", "", None,
                                 settings.exec_wall_seconds * 1000,
                                 timed_out=True)
            return RawResult(proc.stdout, proc.stderr, proc.returncode,
                             now_ms(started))


def availability() -> tuple:
    """Always usable -- it is the fallback everything else degrades to."""
    return True, "subprocess with rlimits (not a sandbox)"
