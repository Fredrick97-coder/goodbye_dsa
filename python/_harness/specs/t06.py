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
]
