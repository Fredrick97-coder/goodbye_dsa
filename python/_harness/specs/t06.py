"""Specs for Topic 06 -- Basic Sorting.

Every sort is checked against `sorted`, which is the ideal reference: an
independent, C-implemented, stable algorithm.
"""

from ..spec import spec


def g_arr(rng, lo=-40, hi=40, nmin=0, nmax=25):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_tuples(rng):
    return ([(rng.randint(0, 9), rng.choice("abcde"))
             for _ in range(rng.randint(0, 10))],)


def g_strings(rng):
    return (["".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
             for _ in range(rng.randint(0, 10))],)


def _comparisons_ok(result):
    """bubble_sort_count_* return (sorted_list, count)."""
    if result is None:
        return None
    arr, count = result
    return (arr == sorted(arr), isinstance(count, int) and count >= 0)


def _ref_perf_shape(result):
    """
    Structure only -- wall-clock timings are machine-dependent.

    Grading the actual comparison counts would mean inventing a counting
    convention (does the outer loop's test count?) and failing correct code
    that chose a different one. So this checks that all three sorts are
    reported with the three required metrics and plausible values, which is
    what distinguishes an implementation from a stub.
    """
    if not isinstance(result, dict):
        return None
    algos = sorted(result)
    if algos != ["bubble", "insertion", "selection"]:
        return None
    for stats in result.values():
        if not isinstance(stats, dict):
            return None
        if not {"time", "comparisons", "swaps"} <= set(stats):
            return None
        if stats["comparisons"] <= 0 or stats["time"] < 0:
            return None
    return True


def _ref_adaptive_shape(result):
    """
    Insertion sort must do LESS work on a sorted array than a reversed one.

    That ordering is the entire lesson of the problem and it holds for every
    correct implementation regardless of how comparisons are counted, which a
    raw count comparison would not.
    """
    if not isinstance(result, dict) or len(result) != 3:
        return None
    counts = [result[k] for k in sorted(result)]
    if any(not isinstance(c, (int, float)) for c in counts):
        return None
    return counts[0] < counts[2]      # sorted cheaper than reversed


SPECS = [
    spec(1, "bubble_sort", ref=sorted, gen=g_arr,
         cases=[(([3, 1, 2],), [1, 2, 3]), (([],), []), (([1],), [1])]),
    spec(2, "selection_sort", ref=sorted, gen=g_arr,
         cases=[(([3, 1, 2],), [1, 2, 3]), (([],), [])]),
    spec(3, "insertion_sort", ref=sorted, gen=g_arr,
         cases=[(([3, 1, 2],), [1, 2, 3]), (([],), [])]),
    spec(4, "bubble_sort_descending",
         ref=lambda a: sorted(a, reverse=True), gen=g_arr,
         cases=[(([3, 1, 2],), [3, 2, 1]), (([],), [])]),
    spec(5, "bubble_sort_count_comparisons", prop=_comparisons_ok,
         cases=[(([5, 2, 9, 1],), (True, True)), (([1, 2, 3],), (True, True))],
         note="returns (sorted_list, count); the count is only sanity-checked"),
    spec(5, "bubble_sort_count_swaps", prop=_comparisons_ok,
         cases=[(([5, 2, 9, 1],), (True, True)), (([1, 2, 3],), (True, True))]),
    spec(6, "sort_tuples", ref=sorted, gen=g_tuples,
         cases=[(([(3, "c"), (1, "a")],), [(1, "a"), (3, "c")])]),
    spec(7, "sort_strings", ref=sorted, gen=g_strings,
         cases=[((["banana", "apple"],), ["apple", "banana"]), (([],), [])]),
    spec(11, "cocktail_sort", ref=sorted, gen=g_arr,
         cases=[(([3, 1, 2],), [1, 2, 3]), (([],), [])]),
    spec(12, "double_selection_sort", ref=sorted, gen=g_arr,
         cases=[(([3, 1, 2],), [1, 2, 3]), (([],), [])]),

    spec(8, "sort_strings", ref=sorted,
         gen=lambda r: ([("".join(r.choice("abcz") for _ in range(r.randint(1, 5))))
                         for _ in range(r.randint(0, 8))],),
         cases=[((["zebra", "apple", "banana", "cherry"],),
                 ["apple", "banana", "cherry", "zebra"]), (([],), [])]),

    # The three metrics-style problems are graded on structure and on the one
    # invariant that does not depend on a counting convention.
    spec(9, "performance_analysis", prop=_ref_perf_shape,
         cases=[(([5, 2, 9, 1, 7, 3],), True)],
         note="only the SHAPE is graded -- keys bubble/selection/insertion, "
              "each with time/comparisons/swaps. Wall-clock numbers vary by "
              "machine, so they are not compared"),

    spec(10, "compare_adaptive_performance", prop=_ref_adaptive_shape,
         cases=[(([[1, 2, 3, 4, 5, 6], [1, 3, 2, 5, 4, 6],
                   [6, 5, 4, 3, 2, 1]],), True)],
         note="return one comparison count per input array, keyed so that "
              "sorted order comes first. The graded property is that the "
              "sorted array costs less than the reversed one"),
]
