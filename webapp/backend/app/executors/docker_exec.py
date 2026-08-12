"""
Container backend: the one that is actually safe to expose.

Every submission gets a fresh container with:

  --network none            no DNS, no sockets, no metadata endpoint
  --read-only               the image filesystem cannot be modified
  --tmpfs /tmp:noexec       a small scratch area, from which nothing can execute
  --user 65534:65534        nobody; no write access to the mounted sources
  --cap-drop ALL            no capabilities at all
  --security-opt no-new-privileges
  --pids-limit N            fork bombs hit a wall instead of the host
  --memory / --memory-swap  equal, so it cannot swap its way past the cap
  --cpus                    a CPU ceiling on top of the in-child rlimit
  --rm                      nothing accumulates

The curriculum and the runner script are bind-mounted read-only, so the image
does not need rebuilding when a problem or a spec changes -- which matters,
because the whole design has the repo as the source of truth.

Wall-clock is enforced by the parent: `docker run` is killed, then the container
is removed by name so a hung daemon cannot leak containers.
"""

from __future__ import annotations

import shutil
import subprocess
import time
import uuid
from pathlib import Path
from typing import List

from .. import languages
from ..settings import settings
from .base import Job, RawResult, now_ms, staged

RUNNERS = Path(__file__).resolve().parents[1] / "runners"
CONTAINER_REPO = "/repo"
CONTAINER_RUNNERS = "/runner"
CONTAINER_WORK = "/work"


def build_argv(name: str, lang=None, workdir: str = "") -> List[str]:
    """
    The exact `docker run` argv, separated out so tests can assert on it.

    A sandbox whose flags are only verified by running it is a sandbox whose
    flags silently regress; this way the important ones are unit-tested.
    """
    lang = lang or languages.get("python")
    memory = f"{settings.exec_memory_mb}m"
    mounts: List[str] = [
        "--volume", f"{settings.python_root.resolve()}:{CONTAINER_REPO}:ro",
        "--volume", f"{RUNNERS.resolve()}:{CONTAINER_RUNNERS}:ro",
    ]
    if workdir:
        # The staged source, read-only: the container must import it, never
        # modify it, and never see anything else from the host.
        mounts += ["--volume", f"{workdir}:{CONTAINER_WORK}:ro"]

    inner = languages.resolve_command(
        lang,
        driver=f"{CONTAINER_RUNNERS}/{lang.driver}",
        python_root=CONTAINER_REPO,
        workdir=CONTAINER_WORK,
        python="python",
    )
    return [
        settings.docker_binary, "run",
        "--rm", "--interactive",
        "--name", name,
        "--network", "none",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=32m",
        "--user", "65534:65534",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", str(settings.docker_pids_limit),
        "--memory", memory,
        "--memory-swap", memory,        # equal to --memory disables swap
        "--cpus", "1",
        "--workdir", "/tmp",
        "--env", "PYTHONDONTWRITEBYTECODE=1",
        "--env", "PYTHONUNBUFFERED=1",
        "--env", "NODE_OPTIONS=--no-warnings",
        "--env", "HOME=/tmp",
        *mounts,
        languages.image_for(lang),
        *inner,
    ]


class DockerExecutor:
    name = "docker"
    safe_for_untrusted = True

    def run(self, job: Job) -> RawResult:
        # Hex only: docker rejects names outside [a-zA-Z0-9][a-zA-Z0-9_.-]*,
        # and a name built from anything caller-supplied would be an injection
        # point into the argv.
        lang = languages.get(job.language)
        if lang is None or not lang.implemented:
            return RawResult("", f"no driver for {job.language}", 1, 0.0)

        name = f"forge-run-{uuid.uuid4().hex[:16]}"
        started = time.perf_counter()
        with staged(job) as (workdir, source_path):
          container_source = f"{CONTAINER_WORK}/{job.filename}"
          try:
            proc = subprocess.run(
                build_argv(name, lang, workdir),
                input=job.payload(container_source),
                capture_output=True,
                text=True,
                # A little grace over the in-container limits: the container
                # should stop itself, and this is the backstop for a wedged
                # daemon rather than the primary limit.
                timeout=settings.exec_wall_seconds + 10,
            )
          except subprocess.TimeoutExpired:
            self._force_remove(name)
            return RawResult("", "", None,
                             (settings.exec_wall_seconds + 10) * 1000,
                             timed_out=True)

        # Deliberately no OOM guess here: exit 137 is SIGKILL and, measured on
        # this stack, that is the CPU hard limit rather than the cgroup OOM
        # killer (a real memory bomb trips the child's RLIMIT_AS and reports a
        # clean MemoryError instead). `to_report` names both causes.
          return RawResult(proc.stdout, proc.stderr, proc.returncode,
                           now_ms(started))

    def _force_remove(self, name: str) -> None:
        try:
            subprocess.run([settings.docker_binary, "rm", "-f", name],
                           capture_output=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            pass


def availability() -> tuple:
    binary = shutil.which(settings.docker_binary)
    if not binary:
        return False, f"{settings.docker_binary} not on PATH"
    try:
        info = subprocess.run([settings.docker_binary, "info", "--format",
                               "{{.ServerVersion}}"],
                              capture_output=True, text=True, timeout=25)
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"daemon unreachable: {exc}"
    if info.returncode != 0:
        return False, "daemon unreachable (is Docker running?)"

    # The images have to exist locally: pulling on the first submission would
    # turn one learner's Submit into a multi-minute wait.
    missing = []
    for lang in languages.LANGUAGES:
        if not lang.implemented:
            continue
        image = languages.image_for(lang)
        try:
            found = subprocess.run(
                [settings.docker_binary, "image", "inspect", image],
                capture_output=True, text=True, timeout=25)
        except (OSError, subprocess.SubprocessError) as exc:
            return False, f"image check failed: {exc}"
        if found.returncode != 0:
            missing.append(f"{image} ({lang.id})")
    if missing:
        return False, (f"image(s) not built: {', '.join(missing)} -- run "
                       f"backend/docker/build.sh")
    return True, f"docker {info.stdout.strip()}"
