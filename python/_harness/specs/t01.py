"""Specs for Topic 01 -- Introduction to DSA."""

import itertools

from ..spec import as_set_of_tuples, spec


def _pairs(arr, target):
    return [(i, j) for i in range(len(arr)) for j in range(i + 1, len(arr))
            if arr[i] + arr[j] == target]


def _subarrays(arr, target):
    out = []
    for i in range(len(arr)):
        run = 0
        for j in range(i, len(arr)):
            run += arr[j]
            if run == target:
                out.append((i, j))
    return out


def _closest_pair(arr):
    best = None
    bestd = None
    for a, b in itertools.combinations(sorted(arr), 2):
        d = abs(a - b)
        if bestd is None or d < bestd:
            bestd, best = d, (a, b)
    return best


def g_arr(rng, lo=-30, hi=30, nmin=1, nmax=20):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_arr_target(rng):
    arr = [rng.randint(-15, 15) for _ in range(rng.randint(1, 14))]
    return (arr, rng.randint(-20, 20))


def g_missing(rng):
    n = rng.randint(1, 20)
    full = list(range(n + 1))
    full.remove(rng.randrange(n + 1))
    rng.shuffle(full)
    return (full,)


def g_two_sorted(rng):
    return (sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 10))),
            sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 10))))


SPECS = [
    spec(1, "find_max", ref=max, gen=g_arr,
         cases=[(([3, 1, 4, 1, 5, 9, 2, 6],), 9), (([-5],), -5)]),
    spec(2, "count_occurrences", ref=lambda a, t: a.count(t), gen=g_arr_target,
         cases=[(([1, 2, 2, 3, 2, 4], 2), 3), (([1], 9), 0)]),
    spec(3, "array_sum", ref=sum, gen=g_arr,
         cases=[(([1, 2, 3, 4, 5],), 15), (([],), 0)]),
    spec(4, "element_exists", ref=lambda a, t: t in a, gen=g_arr_target,
         cases=[(([1, 2, 3], 2), True), (([1, 2, 3], 9), False)]),
    spec(5, "find_pairs_sum_naive", ref=_pairs, gen=g_arr_target,
         norm=as_set_of_tuples,
         cases=[(([1, 2, 3, 4], 5), [(0, 3), (1, 2)])]),
    spec(5, "find_pairs_sum_optimized", ref=_pairs, gen=g_arr_target,
         norm=as_set_of_tuples,
         cases=[(([1, 2, 3, 4], 5), [(0, 3), (1, 2)])]),
    spec(6, "has_duplicates_naive", ref=lambda a: len(a) != len(set(a)),
         gen=lambda r: g_arr(r, 0, 8, 0, 12),
         cases=[(([1, 2, 3],), False), (([1, 2, 1],), True), (([],), False)]),
    spec(6, "has_duplicates_optimized", ref=lambda a: len(a) != len(set(a)),
         gen=lambda r: g_arr(r, 0, 8, 0, 12),
         cases=[(([1, 2, 3],), False), (([1, 2, 1],), True)]),
    spec(7, "find_missing_number",
         ref=lambda a: (len(a) * (len(a) + 1) // 2) - sum(a), gen=g_missing,
         cases=[(([3, 0, 1],), 2), (([0],), 1)]),
    spec(8, "merge_sorted_arrays", ref=lambda a, b: sorted(a + b),
         gen=g_two_sorted,
         cases=[(([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
                (([], []), [])]),
    spec(9, "find_subarrays_with_sum", ref=_subarrays, gen=g_arr_target,
         norm=as_set_of_tuples,
         cases=[(([1, 2, 3, 4], 3), [(0, 1), (2, 2)])]),
    # Only the *_optimized variant actually exists. The unoptimised
    # `find_closest_pair` appears inside a triple-quoted string in the
    # problem text, as the "current implementation" to be improved -- so it
    # is not a real module attribute. The harness reported MISSING and was
    # correct; this spec was the thing that was wrong.
    spec(11, "find_closest_pair_optimized", ref=_closest_pair,
         gen=lambda r: g_arr(r, -50, 50, 2, 12),
         norm=lambda x: tuple(sorted(x)) if x else x,
         cases=[(([1, 5, 3, 19, 18],), (18, 19))]),
]
