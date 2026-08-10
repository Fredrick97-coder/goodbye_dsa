"""Specs for Topic 13 -- Advanced Sorting."""

from ..spec import spec


def g_arr(rng, lo=-40, hi=40, nmin=0, nmax=30):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_nonneg(rng):
    return ([rng.randint(0, 60) for _ in range(rng.randint(0, 25))],)


def g_counting(rng):
    arr = [rng.randint(0, 30) for _ in range(rng.randint(0, 20))]
    return (arr, max(arr) if arr else 0)


def g_floats(rng):
    return ([round(rng.random(), 4) for _ in range(rng.randint(0, 20))],)


def g_lists(rng):
    return ([sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 8)))
             for _ in range(rng.randint(0, 6))],)


def g_arr_k(rng):
    arr = [rng.randint(-30, 30) for _ in range(rng.randint(1, 18))]
    return (arr, rng.randint(1, len(arr)))


def g_nearly_sorted(rng):
    k = rng.randint(0, 4)
    n = rng.randint(0, 18)
    arr = sorted(rng.randint(0, 50) for _ in range(n))
    # perturb each element by at most k positions
    for i in range(n):
        j = min(n - 1, max(0, i + rng.randint(-k, k)))
        arr[i], arr[j] = arr[j], arr[i]
    return (arr, k)


def g_tuples(rng):
    return ([tuple(rng.randint(0, 9) for _ in range(3))
             for _ in range(rng.randint(0, 10))],)


def _count_inversions(arr):
    return sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr))
               if arr[i] > arr[j])


def _quick_select(arr, k):
    """kth SMALLEST, 1-indexed."""
    return sorted(arr)[k - 1]


def _merge_k(arrays):
    out = []
    for a in arrays:
        out.extend(a)
    return sorted(out)


def _multikey(items, keys):
    return sorted(items, key=lambda t: tuple(t[i] for i in keys))


SPECS = [
    spec(1, "merge_sort", ref=sorted, gen=g_arr,
         cases=[(([5, 2, 9, 1],), [1, 2, 5, 9]), (([],), []), (([1],), [1])]),
    spec(2, "quick_sort", ref=sorted, gen=g_arr,
         cases=[(([5, 2, 9, 1],), [1, 2, 5, 9]), (([],), []),
                (([3, 3, 3],), [3, 3, 3])]),
    spec(3, "heap_sort", ref=sorted, gen=g_arr,
         cases=[(([5, 2, 9, 1],), [1, 2, 5, 9]), (([],), [])]),
    spec(4, "counting_sort", ref=lambda a, m: sorted(a), gen=g_counting,
         cases=[(([4, 2, 2, 8, 3], 8), [2, 2, 3, 4, 8]), (([], 0), [])]),
    spec(5, "radix_sort", ref=sorted, gen=g_nonneg,
         cases=[(([170, 45, 75, 90, 2, 802, 24, 66],),
                 [2, 24, 45, 66, 75, 90, 170, 802]), (([],), [])],
         note="non-negative integers only"),
    spec(6, "bucket_sort", ref=sorted, gen=g_floats, tol=1e-9,
         cases=[(([0.42, 0.32, 0.75, 0.11],), [0.11, 0.32, 0.42, 0.75]),
                (([],), [])]),
    spec(7, "custom_sort", ref=sorted, gen=g_tuples,
         cases=[(([(3, 1, 2), (1, 2, 3)],), [(1, 2, 3), (3, 1, 2)])]),
    spec(8, "merge_k_arrays", ref=_merge_k, gen=g_lists,
         cases=[(([[1, 4], [2, 5], [3, 6]],), [1, 2, 3, 4, 5, 6]),
                (([],), [])]),
    spec(9, "quick_select", ref=_quick_select, gen=g_arr_k,
         cases=[(([7, 10, 4, 3, 20, 15], 3), 7), (([1], 1), 1)],
         note="kth SMALLEST, 1-indexed"),
    spec(10, "count_inversions", ref=_count_inversions,
         gen=lambda r: g_arr(r, 0, 20, 0, 16),
         cases=[(([5, 4, 3, 2, 1],), 10), (([1, 2, 3],), 0), (([],), 0)]),
    spec(11, "sort_nearly_sorted", ref=lambda a, k: sorted(a),
         gen=g_nearly_sorted,
         cases=[(([6, 5, 3, 2, 8, 10, 9], 3), [2, 3, 5, 6, 8, 9, 10]),
                (([], 0), [])]),
    spec(12, "multikey_sort", ref=_multikey,
         gen=lambda r: (g_tuples(r)[0], r.sample([0, 1, 2], r.randint(1, 3))),
         cases=[(([(1, 5), (1, 2), (0, 9)], [0, 1]),
                 [(0, 9), (1, 2), (1, 5)])]),
]
