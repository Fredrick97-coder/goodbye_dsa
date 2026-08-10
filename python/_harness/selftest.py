"""
Self-consistency check for the spec suite.

    python -m _harness.selftest

Two independent checks:

  1. REF INJECTION -- for every spec that has a `ref`, install that ref as
     if it were the learner's solution. It must PASS. A spec that fails its
     own reference is a broken spec, and this has already caught eight real
     bugs (wrong expected values, ragged generated matrices, references with
     the wrong mutation contract).

     Specs combining `prop` with `ref` are skipped here: `prop` transforms
     only the ACTUAL value, so those refs already return the transformed
     form and re-transforming it is meaningless. They are covered by check 2.

  2. RAW SOLUTIONS -- a handful of genuine implementations for the
     prop-based specs that check 1 cannot reach.

This file tests the TESTS. Without it, a subtly wrong expected value would
silently mark a correct solution as failing, which is worse than no test.
"""

from __future__ import annotations


from .loader import load_exercise
from .runner import _run_one
from .specs import load_all


def _longest_pal_raw(s):
    if not s:
        return ""
    best = s[0]
    for i in range(len(s)):
        for j in range(i + len(best), len(s) + 1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best


def _min_window_raw(s, t):
    from collections import Counter
    if not t or not s:
        return ""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= n for c, n in need.items()):
                cand = s[i:j + 1]
                if not best or len(cand) < len(best):
                    best = cand
                break
    return best


def _activity_raw(activities):
    """Return an actual maximal selection, sorted by end time."""
    out = []
    last = None
    for s, e in sorted(activities, key=lambda x: x[1]):
        if last is None or s >= last:
            out.append((s, e))
            last = e
    return out


def _subset_sum_raw(nums, target):
    import itertools
    for r in range(len(nums) + 1):
        for combo in itertools.combinations(nums, r):
            if sum(combo) == target:
                return True, list(combo)
    return False, None


def _reverse_ll_raw(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def _merge_ll_raw(a, b):
    """Merge two sorted chains, reusing whichever Node class they came from."""
    vals = []
    for h in (a, b):
        while h:
            vals.append(h.data if hasattr(h, "data") else h.value)
            h = h.next
    vals.sort()
    node_cls = None
    for h in (a, b):
        if h is not None:
            node_cls = type(h)
            break
    if node_cls is None:
        return None
    head = None
    for v in reversed(vals):
        n = node_cls(v)
        n.next = head
        head = n
    return head


def _inorder_raw(root):
    return (_inorder_raw(root.left) + [root.value] + _inorder_raw(root.right)
            if root else [])


def _invert_raw(root):
    if root:
        root.left, root.right = _invert_raw(root.right), _invert_raw(root.left)
    return root


def _depth_raw(root):
    return 1 + max(_depth_raw(root.left), _depth_raw(root.right)) if root else 0


# (topic, target) -> a genuine raw implementation
RAW = {
    (3, "longest_palindrome"): _longest_pal_raw,
    (3, "min_window_substring"): _min_window_raw,
    (15, "activity_selection"): _activity_raw,
    (15, "interval_schedule"): _activity_raw,
    (20, "subset_sum"): _subset_sum_raw,
    # Node-based specs: ref injection cannot reach these, because the ref
    # returns a plain list while `prop` expects a Node chain to walk.
    (7, "reverse_linked_list"): _reverse_ll_raw,
    (7, "merge_sorted_lists"): _merge_ll_raw,
    (8, "inorder_traversal"): _inorder_raw,
    (8, "invert_tree"): _invert_raw,
    (8, "max_depth"): _depth_raw,
}


def main() -> int:
    all_specs = load_all()
    ref_bad, raw_bad = [], []
    ref_n = raw_n = skipped = 0

    for topic, specs in sorted(all_specs.items()):
        module, err = load_exercise(topic)
        if err:
            print(f"  topic {topic:02d}: IMPORT FAILED -- {err}")
            ref_bad.append((topic, 0, "<import>", "ERROR", err))
            continue

        for sp in specs:
            root = sp.target.split(".")[0]

            raw = RAW.get((topic, root))
            if raw is not None:
                raw_n += 1
                setattr(module, root, raw)
                r = _run_one(sp, module)
                if r.status != "PASS":
                    raw_bad.append((topic, sp.num, sp.target, r.status, r.detail))
                continue

            if sp.ref is None:
                continue
            if sp.prop is not None:
                skipped += 1
                continue

            ref_n += 1
            setattr(module, root, sp.ref)
            r = _run_one(sp, module)
            if r.status != "PASS":
                ref_bad.append((topic, sp.num, sp.target, r.status, r.detail))

    total_specs = sum(len(v) for v in all_specs.values())
    print("=" * 66)
    print("SPEC SELF-CONSISTENCY")
    print("=" * 66)
    print(f"  topics with specs      : {len(all_specs)}")
    print(f"  total specs            : {total_specs}")
    print(f"  ref-injection checked  : {ref_n}")
    print(f"  raw-solution checked   : {raw_n}")
    print(f"  skipped (prop + ref)   : {skipped}")

    bad = ref_bad + raw_bad
    if not bad:
        print(f"\n  All {ref_n + raw_n} verifiable specs are self-consistent.")
        print("  Every reference passes its own test, so a correct solution")
        print("  will not be marked wrong by a bad expected value.")
        return 0

    print(f"\n  {len(bad)} SELF-INCONSISTENT SPEC(S) -- fix the spec, not the solution:")
    for t, num, tgt, st, detail in bad:
        print(f"    t{t:02d} #{num} {tgt}: {st}")
        print(f"        {detail[:80]}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
