"""Specs for Topic 02 -- Arrays & Lists."""

from collections import Counter, deque

from ..spec import spec


def _second_max(arr):
    u = sorted(set(arr), reverse=True)
    return u[1] if len(u) > 1 else None


def _dedupe_keep_order(arr):
    seen = set()
    out = []
    for v in arr:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _two_sum(arr, target):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None


def _rotate(arr, k):
    if not arr:
        return []
    k %= len(arr)
    return arr[-k:] + arr[:-k] if k else list(arr)


def _kadane(arr):
    if not arr:
        return 0
    best = cur = arr[0]
    for v in arr[1:]:
        cur = max(v, cur + v)
        best = max(best, cur)
    return best


def _dup_within_k(arr, k):
    for i in range(len(arr)):
        for j in range(i + 1, min(i + k + 1, len(arr))):
            if arr[i] == arr[j]:
                return True
    return False


def _trap(height):
    n = len(height)
    if n < 3:
        return 0
    total = 0
    for i in range(n):
        left = max(height[:i + 1])
        right = max(height[i:])
        total += min(left, right) - height[i]
    return total


def _product_except_self(arr):
    n = len(arr)
    out = []
    for i in range(n):
        p = 1
        for j in range(n):
            if j != i:
                p *= arr[j]
        out.append(p)
    return out


def _window_max(arr, k):
    dq = deque()
    out = []
    for i, v in enumerate(arr):
        while dq and arr[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(arr[dq[0]])
    return out


def _longest_consecutive(arr):
    s = set(arr)
    best = 0
    for v in s:
        if v - 1 not in s:
            n = v
            while n + 1 in s:
                n += 1
            best = max(best, n - v + 1)
    return best


def g_arr(rng, lo=-30, hi=30, nmin=1, nmax=18):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_arr_k(rng):
    arr = [rng.randint(-20, 20) for _ in range(rng.randint(1, 15))]
    return (arr, rng.randint(0, 20))


def g_window(rng):
    n = rng.randint(1, 18)
    return ([rng.randint(-25, 25) for _ in range(n)], rng.randint(1, n))


def g_heights(rng):
    return ([rng.randint(0, 8) for _ in range(rng.randint(0, 15))],)


SPECS = [
    spec(1, "find_second_max", ref=_second_max,
         gen=lambda r: g_arr(r, 0, 12, 1, 12),
         cases=[(([1, 5, 3, 9, 7],), 7), (([2, 2],), None)]),
    spec(2, "remove_duplicates", ref=_dedupe_keep_order, gen=g_arr,
         cases=[(([1, 2, 2, 3, 1],), [1, 2, 3]), (([],), [])]),
    spec(3, "count_elements", ref=lambda a: dict(Counter(a)), gen=g_arr,
         cases=[(([1, 1, 2],), {1: 2, 2: 1}), (([],), {})]),
    spec(4, "reverse_array", ref=lambda a: a[::-1], gen=g_arr,
         cases=[(([1, 2, 3],), [3, 2, 1]), (([],), [])]),
    spec(5, "two_sum", ref=_two_sum, gen=g_arr_k,
         norm=lambda x: tuple(x) if x is not None else None,
         cases=[(([2, 7, 11, 15], 9), (0, 1))]),
    spec(6, "rotate_array", ref=_rotate, gen=g_arr_k,
         cases=[(([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
                (([1, 2, 3], 0), [1, 2, 3]),
                (([1, 2, 3], 3), [1, 2, 3])]),
    spec(7, "merge_sorted", ref=lambda a, b: sorted(a + b),
         gen=lambda r: (sorted(r.randint(0, 30) for _ in range(r.randint(0, 8))),
                        sorted(r.randint(0, 30) for _ in range(r.randint(0, 8)))),
         cases=[(([1, 3], [2, 4]), [1, 2, 3, 4])]),
    spec(8, "max_subarray_sum", ref=_kadane, gen=g_arr,
         cases=[(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([-1],), -1)]),
    spec(9, "contains_duplicate_k", ref=_dup_within_k,
         gen=lambda r: ([r.randint(0, 6) for _ in range(r.randint(0, 12))],
                        r.randint(0, 5)),
         cases=[(([1, 2, 3, 1], 3), True), (([1, 2, 3, 1], 2), False)]),
    spec(10, "trap_rain_water", ref=_trap, gen=g_heights,
         cases=[(([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6), (([],), 0)]),
    spec(11, "product_except_self", ref=_product_except_self,
         gen=lambda r: ([r.randint(-4, 4) for _ in range(r.randint(1, 8))],),
         cases=[(([1, 2, 3, 4],), [24, 12, 8, 6])]),
    spec(12, "sliding_window_max", ref=_window_max, gen=g_window,
         cases=[(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])]),
    spec(13, "longest_consecutive", ref=_longest_consecutive,
         gen=lambda r: g_arr(r, 0, 25, 0, 15),
         cases=[(([100, 4, 200, 1, 3, 2],), 4), (([],), 0)]),
]
