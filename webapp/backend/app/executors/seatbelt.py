"""
macOS Seatbelt backend: the same subprocess, wrapped in a kernel-enforced policy.

`sandbox-exec` applies a profile that the XNU kernel enforces on the process and
everything it spawns. This is real containment, not a convention -- the deny
rules cannot be lifted from inside the sandbox.

**The profile is allow-default with explicit denies, and that is deliberate.**
A deny-default profile is stronger in principle, and it was the first thing tried
here -- but CPython touches a long, version-dependent tail of paths and Mach
services during startup, and enumerating them produced a profile that aborted
the interpreter with no diagnostics and would have broken on the next patch
release. Denying the four things that actually matter is a policy that holds:

    no network            nothing can be exfiltrated
    no filesystem writes  nothing persists, including /tmp
    no reads of $HOME     except the curriculum itself
    no exec               except the interpreter's own prefix

Order matters: Seatbelt applies the LAST matching rule, so every `allow` that
carves an exception out of a `deny` has to come after it.

This is defence in depth for local development, not a substitute for a container
in production: the process still shares the host kernel, and a Seatbelt bug is a
full escape. `availability()` probes the profile before offering it, so a broken
profile makes this backend unavailable rather than breaking submissions.
"""

from __future__ import annotations

import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Tuple

from ..settings import settings
from .base import Job, RawResult, now_ms

CHILD = Path(__file__).resolve().parents[1] / "child_runner.py"
SANDBOX_EXEC = "/usr/bin/sandbox-exec"

#: Places a submission has no business reading. The curriculum is carved back
#: out below, and so is the interpreter, which may itself live under $HOME in a
#: virtualenv.
DENY_READ_PREFIXES = (
    "/Users", "/etc", "/private/etc", "/var", "/private/var/root",
    "/Volumes", "/opt", "/Applications", "/Library/Keychains",
)


def _profile() -> str:
    prefix = Path(sys.prefix).resolve()
    base_prefix = Path(sys.base_prefix).resolve()
    repo = settings.python_root.resolve()
    runner = CHILD.resolve().parent

    deny_reads = "\n".join(f'(deny file-read* (subpath "{p}"))'
                           for p in DENY_READ_PREFIXES)
    allow_reads = "\n".join(f'(allow file-read* (subpath "{p}"))' for p in (
        prefix, base_prefix, repo, runner))
    allow_exec = "\n".join(f'(allow process-exec (subpath "{p}"))' for p in (
        prefix, base_prefix))

    return f"""(version 1)
(allow default)

;; 1. Nothing leaves the machine.
(deny network*)

;; 2. Nothing is written anywhere, including /tmp. The bit bucket is the one
;;    exception, because some libraries expect it to be writable.
(deny file-write* (subpath "/"))
(allow file-write-data (literal "/dev/null"))

;; 3. No reading the host's private data. The interpreter and the curriculum are
;;    added back afterwards -- these allows MUST follow the denies.
{deny_reads}
{allow_reads}

;; 4. No running other programs. Only the interpreter's own prefix, which is
;;    what sandbox-exec is about to launch; a bare `(deny process-exec*)` also
;;    blocks that first exec and the sandbox fails to start at all.
(deny process-exec*)
{allow_exec}
"""


class SeatbeltExecutor:
    name = "seatbelt"
    safe_for_untrusted = True

    def run(self, job: Job) -> RawResult:
        started = time.perf_counter()
        argv = [
            SANDBOX_EXEC, "-p", _profile(),
            sys.executable, "-I", str(CHILD), str(settings.python_root),
        ]
        try:
            proc = subprocess.run(
                argv, input=job.payload(), capture_output=True, text=True,
                timeout=settings.exec_wall_seconds,
            )
        except subprocess.TimeoutExpired:
            return RawResult("", "", None,
                             settings.exec_wall_seconds * 1000, timed_out=True)
        return RawResult(proc.stdout, proc.stderr, proc.returncode,
                         now_ms(started))


def availability() -> Tuple[bool, str]:
    """
    Is this usable here, and does the profile still load?

    The probe is not ceremony: a malformed profile fails at exec time with no
    diagnostics, and discovering that on a learner's first submission would be
    indistinguishable from a broken platform.
    """
    if platform.system() != "Darwin":
        return False, "sandbox-exec is macOS-only"
    if not Path(SANDBOX_EXEC).exists():
        return False, f"{SANDBOX_EXEC} not found"
    try:
        probe = subprocess.run(
            [SANDBOX_EXEC, "-p", _profile(), sys.executable, "-I", "-c",
             "print(1)"],
            capture_output=True, text=True, timeout=25)
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"probe failed: {exc}"
    if probe.returncode != 0 or probe.stdout.strip() != "1":
        detail = (probe.stderr or "").strip()[:120] or f"rc={probe.returncode}"
        return False, f"probe failed: {detail}"
    return True, "macOS Seatbelt: no network, no writes, no $HOME reads, no exec"
