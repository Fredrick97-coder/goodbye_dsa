"""
The submission entry point: pick the isolation backend and run one job.

This module used to *be* the subprocess runner. It is now a dispatcher, because
"how isolated is the code we run" became a deployment decision rather than a
fixed property of the code -- see `app/executors/`.

Two things live here that belong to neither the caller nor a backend:

* the source-size check, which should reject a 10 MB paste before any process
  is started
* a concurrency cap, so N simultaneous submissions cannot start N containers and
  take the host down with them
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Dict

from . import executors
from .executors.base import Job, fatal, summarise, to_report      # noqa: F401
from .settings import settings

log = logging.getLogger("forge.exec")

# A submission holds one slot for its whole run. This bounds concurrent memory
# and CPU use to something the host can survive: without it, twenty learners
# pressing Submit at once means twenty containers each allowed 512 MB.
_slots = threading.BoundedSemaphore(settings.exec_max_concurrent)
_ACQUIRE_TIMEOUT = 20.0


def run_submission(source: str, topic: int, num: int,
                   mode: str = "test") -> Dict[str, Any]:
    if len(source.encode("utf-8")) > settings.exec_max_source_bytes:
        return fatal("SubmissionTooLarge",
                     f"source exceeds {settings.exec_max_source_bytes} bytes")

    name = settings.resolved_executor or "local"
    backend = executors.get(name)
    job = Job(source=source, topic=topic, num=num, mode=mode)

    if not _slots.acquire(timeout=_ACQUIRE_TIMEOUT):
        # Shedding load with a clear message beats queueing behind a timeout
        # the learner cannot see.
        log.warning("execution queue full, shedding a submission")
        return fatal("Busy",
                     "the grader is at capacity right now -- try again in a "
                     "few seconds")
    try:
        result = backend.run(job)
    except Exception as exc:                                # noqa: BLE001
        log.exception("executor %s failed", name)
        return fatal("ExecutorError",
                     f"the {name} runner failed: {type(exc).__name__}: {exc}")
    finally:
        _slots.release()

    return to_report(result, name)
