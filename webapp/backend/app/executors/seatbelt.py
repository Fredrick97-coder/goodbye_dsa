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

from .. import languages
from ..settings import settings
from .base import Job, RawResult, now_ms, staged

RUNNERS = Path(__file__).resolve().parents[1] / "runners"
SANDBOX_EXEC = "/usr/bin/sandbox-exec"

#: Places a submission has no business reading. The curriculum is carved back
#: out below, and so is the interpreter, which may itself live under $HOME in a
#: virtualenv.
DENY_READ_PREFIXES = (
    "/Users", "/etc", "/private/etc", "/var", "/private/var/root",
    "/Volumes", "/opt", "/Applications", "/Library/Keychains",
)


def _profile(extra_read: tuple = (), extra_exec: tuple = (),
             extra_meta: tuple = ()) -> str:
    """
    The policy. `extra_read`/`extra_exec` admit a non-Python runtime.

    A second language means a second interpreter binary, and both its own tree
    and the staged source directory have to be readable -- otherwise the sandbox
    denies the very thing it was asked to launch.
    """
    prefix = Path(sys.prefix).resolve()
    base_prefix = Path(sys.base_prefix).resolve()
    repo = settings.python_root.resolve()
    runner = RUNNERS.resolve()

    deny_reads = "\n".join(f'(deny file-read* (subpath "{p}"))'
                           for p in DENY_READ_PREFIXES)
    allow_reads = "\n".join(f'(allow file-read* (subpath "{p}"))' for p in (
        (prefix, base_prefix, repo, runner) + tuple(extra_read)))
    allow_exec = "\n".join(f'(allow process-exec (subpath "{p}"))' for p in (
        (prefix, base_prefix) + tuple(extra_exec)))
    # Metadata only. Node's ESM loader realpath()s the module it is given, which
    # lstat()s every ancestor directory -- and a macOS temp dir sits under
    # /var/folders, which is denied. Granting lstat on the ancestors keeps the
    # ban on actually reading their contents.
    allow_meta = "\n".join(f'(allow file-read-metadata (subpath "{p}"))'
                           for p in tuple(extra_meta))

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
{allow_meta}

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
        lang = languages.get(job.language)
        if lang is None or not lang.implemented:
            return RawResult("", f"no driver for {job.language}", 1, 0.0)

        found = _runtime_binary(lang)
        if found is None:
            return RawResult("", f"{lang.runtime} runtime not found", 1, 0.0)
        link, real = found

        started = time.perf_counter()
        with staged(job) as (workdir, source_path):
            # The staged directory must be readable (the driver imports the file
            # from it) but never writable -- the deny on writes stays absolute.
            #
            # Both the PATH entry and its target are admitted: Homebrew's `node`
            # is a symlink in /opt/homebrew/bin pointing into ../Cellar, and /opt
            # is on the deny list. Allowing only the resolved path left
            # sandbox-exec unable to read the symlink it was told to run, which
            # surfaced as "execvp() of 'node' failed: Operation not permitted".
            roots = {link.parent, link.parent.parent, real.parent,
                     real.parent.parent}
            ancestors = tuple(Path(workdir).parents)
            profile = _profile(extra_read=(workdir, *roots),
                               extra_exec=tuple(roots),
                               extra_meta=ancestors)
            argv = [SANDBOX_EXEC, "-p", profile] + languages.resolve_command(
                lang, driver=str(RUNNERS / lang.driver),
                python_root=str(settings.python_root),
                workdir=workdir, python=sys.executable)
            # An absolute argv[0]: sandbox-exec resolves a bare name through
            # PATH, and the policy is expressed in paths.
            argv[3] = str(real)
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


def _runtime_binary(lang):
    """
    (path_on_PATH, fully_resolved_path) for this language's interpreter.

    Both matter: the policy must admit the symlink the shell would find *and*
    the file it points at.
    """
    import shutil
    if lang.runtime == "python":
        exe = Path(sys.executable)
        return exe, exe.resolve()
    found = shutil.which(lang.command[0]) if lang.command else None
    if not found:
        return None
    link = Path(found)
    return link, link.resolve()


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
