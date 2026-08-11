"""
Executor registry: which isolation backends exist, and which one is in use.

`availability()` answers "could this host use each backend, and if not why", so
startup can log a real reason rather than silently degrading. `get()` returns the
resolved backend, built once.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

from . import docker_exec, local, seatbelt
from .base import Job, RawResult, fatal, summarise, to_report   # noqa: F401

log = logging.getLogger("forge.exec")

_BACKENDS = {
    "local": (local.LocalExecutor, local.availability),
    "seatbelt": (seatbelt.SeatbeltExecutor, seatbelt.availability),
    "docker": (docker_exec.DockerExecutor, docker_exec.availability),
}

_cache: Dict[str, object] = {}
_availability: Optional[Dict[str, object]] = None


def availability(refresh: bool = False) -> Dict[str, object]:
    """
    {name: bool, name_reason: str} for every backend.

    Cached: probing Docker costs a subprocess and a daemon round trip, and this
    is consulted on startup and by /api/health.
    """
    global _availability
    if _availability is not None and not refresh:
        return _availability
    out: Dict[str, object] = {}
    for name, (_cls, probe) in _BACKENDS.items():
        try:
            ok, reason = probe()
        except Exception as exc:                            # noqa: BLE001
            ok, reason = False, f"probe raised {type(exc).__name__}: {exc}"
        out[name] = ok
        out[f"{name}_reason"] = reason
    _availability = out
    return out


def get(name: str):
    if name not in _BACKENDS:
        raise ValueError(f"unknown executor {name!r}")
    if name not in _cache:
        _cache[name] = _BACKENDS[name][0]()
    return _cache[name]


def is_safe(name: str) -> bool:
    cls = _BACKENDS[name][0]
    return bool(getattr(cls, "safe_for_untrusted", False))
