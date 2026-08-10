"""
Specs for Topic 07 -- Linked Lists.

These use `build` / `build_cases`, which receive the exercise MODULE so that
inputs are constructed from the learner's OWN Node class. Testing a linked
list against a Node defined here would not exercise their code at all.
"""

from ..spec import spec


# --------------------------------------------------------------- scaffolding

def _make(module, values):
    """Build a chain from `values` using the learner's Node class."""
    Node = module.Node
    head = None
    for v in reversed(values):
        n = Node(v)
        n.next = head
        head = n
    return head


def _to_list(head, limit=10_000):
    out = []
    seen = set()
    while head is not None and len(out) < limit:
        if id(head) in seen:            # cycle -- stop rather than hang
            break
        seen.add(id(head))
        out.append(head.value if hasattr(head, "value") else head.data)
        head = head.next
    return out


def _make_cyclic(module, values, loop_to):
    head = _node_at(_make(module, values), 0)
    if head is None:
        return None
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = _node_at(head, loop_to)
    return head


def _node_at(head, i):
    for _ in range(i):
        if head is None:
            return None
        head = head.next
    return head




# ----------------------------------------------------------------- builders

def b_list(module, rng):
    vals = [rng.randint(0, 40) for _ in range(rng.randint(0, 12))]
    return (_make(module, vals),)


def b_list_target(module, rng):
    vals = [rng.randint(0, 8) for _ in range(rng.randint(0, 12))]
    return (_make(module, vals), rng.randint(0, 8))


def b_two_sorted(module, rng):
    a = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8)))
    b = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8)))
    return (_make(module, a), _make(module, b))


def b_palindrome_maybe(module, rng):
    n = rng.randint(0, 8)
    vals = [rng.randint(0, 2) for _ in range(n)]
    if rng.random() < 0.4:                  # force a palindrome sometimes
        vals = vals + vals[::-1][(1 if rng.random() < 0.5 else 0):]
    return (_make(module, vals),)


# --------------------------------------------------------------- references

def _ref_search(head, target):
    return target in _to_list(head)


def _ref_length(head):
    return len(_to_list(head))


def _ref_tail_value(head):
    vals = _to_list(head)
    return vals[-1] if vals else None


def _ref_reverse(head):
    return _to_list(head)[::-1]


def _ref_middle(head):
    vals = _to_list(head)
    return vals[len(vals) // 2] if vals else None


def _ref_merge(a, b):
    return sorted(_to_list(a) + _to_list(b))


def _ref_remove(head, val):
    return [v for v in _to_list(head) if v != val]


def _ref_is_pal(head):
    vals = _to_list(head)
    return vals == vals[::-1]


def _ref_add_two(a, b):
    """Digits stored least-significant-first, the standard convention."""
    x = int("".join(str(d) for d in reversed(_to_list(a))) or 0)
    y = int("".join(str(d) for d in reversed(_to_list(b))) or 0)
    return [int(c) for c in str(x + y)][::-1]


def _ref_reorder(head):
    """L0, Ln, L1, Ln-1, ..."""
    vals = _to_list(head)
    out = []
    lo, hi = 0, len(vals) - 1
    while lo <= hi:
        out.append(vals[lo])
        if lo != hi:
            out.append(vals[hi])
        lo += 1
        hi -= 1
    return out


# ------------------------------------------------------------------- cases

def c_search(module):
    return [((_make(module, [1, 2, 3]), 2), True),
            ((_make(module, [1, 2, 3]), 9), False),
            ((None, 1), False)]


def c_length(module):
    return [((_make(module, [1, 2, 3]),), 3), ((None,), 0)]


def c_cycle(module):
    return [((_make(module, [1, 2, 3, 4]),), False),
            ((_make_cyclic(module, [1, 2, 3, 4], 1),), True),
            ((None,), False),
            ((_make_cyclic(module, [1], 0),), True)]


SPECS = [
    spec(2, "search_linked_list", ref=_ref_search, build=b_list_target,
         build_cases=c_search),
    spec(3, "get_length", ref=_ref_length, build=b_list,
         build_cases=c_length),
    spec(4, "find_tail",
         prop=lambda n: None if n is None else (
             n.value if hasattr(n, "value") else n.data),
         ref=_ref_tail_value, build=b_list,
         note="returns the tail NODE; its stored value is compared"),
    spec(5, "reverse_linked_list", prop=_to_list, ref=_ref_reverse,
         build=b_list),
    spec(6, "find_middle",
         prop=lambda n: None if n is None else (
             n.value if hasattr(n, "value") else n.data),
         ref=_ref_middle, build=b_list,
         note="for even length, the SECOND middle is the usual convention"),
    spec(7, "merge_sorted_lists", prop=_to_list, ref=_ref_merge,
         build=b_two_sorted),
    spec(8, "remove_element", prop=_to_list, ref=_ref_remove,
         build=b_list_target),
    spec(9, "has_cycle", build_cases=c_cycle),
    spec(10, "is_palindrome", ref=_ref_is_pal, build=b_palindrome_maybe),
    spec(11, "add_two_numbers", prop=_to_list, ref=_ref_add_two,
         build=lambda m, r: (
             _make(m, [r.randint(0, 9) for _ in range(r.randint(1, 5))]),
             _make(m, [r.randint(0, 9) for _ in range(r.randint(1, 5))])),
         note="digits least-significant-first"),
    spec(12, "reorder_list", inplace=True, prop=_to_list, ref=_ref_reorder,
         build=b_list,
         note="in-place: L0, Ln, L1, Ln-1, ..."),
]
