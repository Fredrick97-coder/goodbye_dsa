"""Specs for Topic 19 -- Heaps & Priority Queues."""

import heapq
from collections import Counter, deque

from ..spec import as_sorted, spec

# ------------------------------------------------------------- references


def _ref_heap_sort(arr):
    return sorted(arr)


def _ref_is_min_heap(arr):
    return all(arr[i] <= arr[c]
               for i in range(len(arr))
               for c in (2 * i + 1, 2 * i + 2) if c < len(arr))


def _ref_kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]


def _ref_top_k_frequent(nums, k):
    return [v for v, _ in Counter(nums).most_common(k)]


def _ref_k_closest(points, k):
    return sorted(points, key=lambda p: (p[0] ** 2 + p[1] ** 2))[:k]


def _ref_merge_k_sorted(lists):
    out = []
    for l in lists:
        out.extend(l)
    return sorted(out)


def _ref_last_stone(stones):
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        a = -heapq.heappop(h)
        b = -heapq.heappop(h)
        if a != b:
            heapq.heappush(h, -(a - b))
    return -h[0] if h else 0


def _ref_min_rooms(intervals):
    """Sweep line, half-open."""
    ev = []
    for s, e in intervals:
        ev.append((s, 1))
        ev.append((e, -1))
    ev.sort()
    cur = best = 0
    for _, d in ev:
        cur += d
        best = max(best, cur)
    return best


def _ref_least_interval(tasks, n):
    """Closed form: (maxcount-1)*(n+1) + how many share the max count."""
    if not tasks:
        return 0
    counts = Counter(tasks)
    top = max(counts.values())
    ties = sum(1 for v in counts.values() if v == top)
    return max(len(tasks), (top - 1) * (n + 1) + ties)


def _ref_window_max(nums, k):
    dq = deque()
    out = []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def _ref_connect_sticks(sticks):
    if len(sticks) < 2:
        return 0
    h = list(sticks)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def _ref_smallest_range(lists):
    ptrs = [0] * len(lists)
    h = [(l[0], i) for i, l in enumerate(lists)]
    heapq.heapify(h)
    hi = max(l[0] for l in lists)
    best = (h[0][0], hi)
    while True:
        lo, i = heapq.heappop(h)
        if hi - lo < best[1] - best[0]:
            best = (lo, hi)
        ptrs[i] += 1
        if ptrs[i] >= len(lists[i]):
            return best
        nxt = lists[i][ptrs[i]]
        hi = max(hi, nxt)
        heapq.heappush(h, (nxt, i))


def _ref_reorganize(s):
    """Returns '' when impossible, else any valid arrangement."""
    counts = Counter(s)
    if max(counts.values()) > (len(s) + 1) // 2:
        return ""
    h = [(-c, ch) for ch, c in counts.items()]
    heapq.heapify(h)
    out = []
    while len(h) > 1:
        c1, a = heapq.heappop(h)
        c2, b = heapq.heappop(h)
        out += [a, b]
        if c1 + 1:
            heapq.heappush(h, (c1 + 1, a))
        if c2 + 1:
            heapq.heappush(h, (c2 + 1, b))
    if h:
        out.append(h[0][1])
    return "".join(out)


def _ref_ipo(k, w, capital, profits):
    locked = sorted(zip(capital, profits))
    avail = []
    i = 0
    for _ in range(k):
        while i < len(locked) and locked[i][0] <= w:
            heapq.heappush(avail, -locked[i][1])
            i += 1
        if not avail:
            break
        w += -heapq.heappop(avail)
    return w


def _ref_sliding_median(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        w = sorted(nums[i:i + k])
        out.append(w[k // 2] if k % 2 else (w[k // 2 - 1] + w[k // 2]) / 2)
    return out


# ------------------------------------------------------------- generators


def g_int_list(rng, lo=0, hi=40, nmin=1, nmax=25):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_list_and_k(rng):
    arr = [rng.randint(-50, 50) for _ in range(rng.randint(1, 20))]
    return (arr, rng.randint(1, len(arr)))


def g_intervals(rng):
    iv = []
    for _ in range(rng.randint(0, 12)):
        a = rng.randint(0, 30)
        iv.append((a, a + rng.randint(1, 12)))
    return (iv,)


def g_lists_of_sorted(rng):
    return ([sorted(rng.randint(0, 60) for _ in range(rng.randint(0, 8)))
             for _ in range(rng.randint(1, 6))],)


def g_nonempty_sorted_lists(rng):
    return ([sorted(rng.randint(0, 60) for _ in range(rng.randint(1, 8)))
             for _ in range(rng.randint(1, 5))],)


def g_points(rng):
    pts = [(rng.randint(-20, 20), rng.randint(-20, 20))
           for _ in range(rng.randint(1, 15))]
    return (pts, rng.randint(1, len(pts)))


def g_window(rng):
    n = rng.randint(1, 25)
    arr = [rng.randint(-30, 30) for _ in range(n)]
    return (arr, rng.randint(1, n))


SPECS = [
    spec(1, "parent_index", cases=[
        ((0,), -1), ((1,), 0), ((2,), 0), ((4,), 1), ((9,), 4),
    ]),
    spec(1, "child_indices", cases=[
        ((0,), (1, 2)), ((1,), (3, 4)), ((4,), (9, 10)),
    ]),
    spec(2, "sift_up", inplace=True, cases=[
        (([1, 3, 5, 7, 0], 4), [0, 1, 5, 7, 3]),
        (([1, 2], 1), [1, 2]),
    ]),
    spec(3, "sift_down", inplace=True, cases=[
        (([9, 1, 5, 7, 3], 0, 5), [1, 3, 5, 7, 9]),
        (([1, 2, 3], 0, 3), [1, 2, 3]),
    ]),
    spec(4, "heap_push", inplace=True, cases=[
        (([1, 3, 5], 0), [0, 1, 5, 3]),
        (([], 7), [7]),
    ]),
    spec(4, "heap_pop", cases=[
        (([1, 3, 5, 7],), 1), (([5],), 5),
    ]),
    spec(5, "heapify", inplace=True, norm=_ref_is_min_heap,
         cases=[(([9, 4, 7, 1, 8, 2],), True), (([1],), True)]),
    spec(6, "is_min_heap", ref=_ref_is_min_heap, gen=g_int_list, cases=[
        (([1, 3, 5, 7, 9],), True), (([1, 3, 5, 0],), False), (([],), True),
    ]),
    spec(7, "heap_sort", ref=_ref_heap_sort, gen=g_int_list, cases=[
        (([3, 1, 2],), [1, 2, 3]), (([],), []),
    ]),
    spec(8, "kth_largest", ref=_ref_kth_largest, gen=g_list_and_k, cases=[
        (([3, 2, 1, 5, 6, 4], 2), 5), (([1], 1), 1),
    ]),
    spec(9, "top_k_frequent", norm=as_sorted, cases=[
        (([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1]),
        (([4, 4, 4, 5, 5, 6], 2), [4, 5]),
    ]),
    spec(10, "k_closest", ref=_ref_k_closest, gen=g_points,
         norm=lambda x: sorted(map(tuple, x)) if x else x, cases=[
        (([(1, 3), (-2, 2)], 1), [(-2, 2)]),
    ]),
    spec(11, "merge_k_sorted", ref=_ref_merge_k_sorted,
         gen=g_lists_of_sorted, cases=[
        (([[1, 4], [2, 5], [3, 6]],), [1, 2, 3, 4, 5, 6]),
        (([[]],), []),
    ]),
    spec(12, "last_stone_weight", ref=_ref_last_stone,
         gen=lambda r: g_int_list(r, 1, 30, 1, 12), cases=[
        (([2, 7, 4, 1, 8, 1],), 1), (([1],), 1), (([2, 2],), 0),
    ]),
    spec(13, "min_meeting_rooms", ref=_ref_min_rooms, gen=g_intervals, cases=[
        (([(0, 30), (5, 10), (15, 20)],), 2),
        (([(7, 10), (2, 4)],), 1),
        (([],), 0),
    ]),
    spec(14, "least_interval", ref=_ref_least_interval,
         gen=lambda r: ([r.choice("ABCDE") for _ in range(r.randint(1, 20))],
                        r.randint(0, 4)), cases=[
        ((["A", "A", "A", "B", "B", "B"], 2), 8),
        ((["A", "A", "A", "B", "B", "B"], 0), 6),
    ]),
    spec(15, "MedianFinder",
         script=lambda cls: (lambda m: [
             (m.add_num(v), m.find_median())[1]
             for v in [5, 15, 1, 3]
         ])(cls()),
         ref_script=lambda: [5.0, 10.0, 5.0, 4.0]),
    spec(16, "sliding_window_median", ref=_ref_sliding_median, gen=g_window,
         tol=1e-9, cases=[
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), [1, -1, -1, 3, 5, 6]),
    ]),
    spec(17, "smallest_range", ref=_ref_smallest_range,
         gen=g_nonempty_sorted_lists,
         norm=lambda x: tuple(x) if x is not None else None, cases=[
        (([[4, 10, 15], [0, 9, 12], [5, 18, 22]],), (9, 12)),
    ]),
    spec(18, "reorganize_string",
         norm=lambda s: None if s is None else (
             "IMPOSSIBLE" if s == "" else
             ("OK" if all(s[i] != s[i + 1] for i in range(len(s) - 1))
              else "ADJACENT")),
         cases=[
        (("aab",), "OK"), (("aaab",), "IMPOSSIBLE"), (("vvvlo",), "OK"),
        (("a",), "OK"),
    ]),
    spec(19, "find_maximized_capital", ref=_ref_ipo,
         gen=lambda r: (lambda n: (
             r.randint(1, 3), r.randint(0, 5),
             [r.randint(0, 8) for _ in range(n)],
             [r.randint(1, 9) for _ in range(n)]))(r.randint(1, 6)),
         cases=[((2, 0, [0, 1, 1], [1, 2, 3]), 4)]),
    spec(23, "connect_sticks", ref=_ref_connect_sticks,
         gen=lambda r: g_int_list(r, 1, 30, 0, 12),
         cases=[(([2, 4, 3],), 14), (([1],), 0), (([],), 0)]),
    spec(24, "max_sliding_window_heap", ref=_ref_window_max, gen=g_window,
         cases=[(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])]),
    spec(24, "max_sliding_window_deque", ref=_ref_window_max, gen=g_window,
         cases=[(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7])]),
]
