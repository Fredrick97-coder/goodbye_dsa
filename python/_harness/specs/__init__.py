"""
Spec registry.

Each t<NN>.py exposes SPECS: a list of Spec objects. Topics with no spec
module simply have no tests yet, and the checker says so rather than
pretending they passed.
"""

from __future__ import annotations

import importlib
from typing import Dict, List

from ..spec import Spec

#: Spec modules are numbered to match topic numbers, which are global across
#: courses. The range is generous so a new course's specs are picked up by
#: existing them, not by editing this line.
_MODULES = [f"t{n:02d}" for n in range(1, 60)]


def load_all() -> Dict[int, List[Spec]]:
    out: Dict[int, List[Spec]] = {}
    for name in _MODULES:
        try:
            mod = importlib.import_module(f".{name}", __name__)
        except ModuleNotFoundError:
            continue
        specs = getattr(mod, "SPECS", None)
        if specs:
            out[int(name[1:])] = specs
    return out


def load_topic(topic: int) -> List[Spec]:
    return load_all().get(topic, [])
