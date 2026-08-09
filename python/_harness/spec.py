"""
Test-spec vocabulary for the exercise harness.

A spec describes HOW to check one problem, not what the answer is. Two
styles are supported, and the second is usually stronger:

  cases=[...]   fixed (args -> expected) pairs. Good for edge cases and
                for problems where a reference is awkward.

  ref=f, gen=g  compare the learner's function against a REFERENCE
                implementation over randomly generated inputs. Far better
                coverage than a handful of hand-written cases, and the
                reference is normally the stdlib (math.comb, itertools,
                sorted) rather than something I wrote.

Both may be given; both run.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Tuple

# A case is (args_tuple, expected). kwargs are not needed anywhere so far.
Case = Tuple[tuple, Any]


@dataclass
class Spec:
    """One problem's check."""

    num: int                                  # problem number in exercise.py
    target: str                               # "func_name" or "Class.method"
    cases: List[Case] = field(default_factory=list)
    ref: Optional[Callable] = None             # reference implementation
    gen: Optional[Callable] = None             # () -> args tuple
    trials: int = 150                          # randomized trials
    norm: Optional[Callable] = None            # normalise before comparing
    inplace: bool = False                      # mutates args[0], returns None
    tol: Optional[float] = None                # float comparison tolerance
    script: Optional[Callable] = None          # for classes: (cls) -> result
    ref_script: Optional[Callable] = None      # reference for `script`
    note: str = ""                             # shown on failure

    @property
    def is_class(self) -> bool:
        return self.script is not None


def spec(num: int, target: str, **kw) -> Spec:
    return Spec(num=num, target=target, **kw)


# ---------------------------------------------------------------- normalisers

def as_sorted(x):
    """Order-insensitive comparison for a flat sequence."""
    return sorted(x) if x is not None else None


def as_set_of_tuples(x):
    """Order-insensitive for a list of lists (subsets, permutations, ...)."""
    if x is None:
        return None
    return sorted(tuple(item) for item in x)


def as_sorted_inner(x):
    """Sort each inner sequence AND the outer one. For unordered groupings."""
    if x is None:
        return None
    return sorted(tuple(sorted(item)) for item in x)


def as_len(x):
    """Only the count matters (e.g. 'how many solutions')."""
    return None if x is None else len(x)


def lists_to_tuples(x):
    if x is None:
        return None
    return tuple(tuple(row) for row in x)


# ------------------------------------------------------------------- outcomes

PASS = "PASS"
FAIL = "FAIL"
STUB = "STUB"          # not implemented yet
ERROR = "ERROR"        # raised an exception
MISSING = "MISSING"    # the function/class is not defined at all


@dataclass
class Result:
    num: int
    target: str
    status: str
    detail: str = ""
    checked: int = 0
