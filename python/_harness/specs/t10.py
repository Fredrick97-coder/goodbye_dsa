"""Specs for Topic 10 -- Basic Searching."""

import bisect
import math

from ..spec import spec


def _binary_search(nums, target):
    i = bisect.bisect_left(nums, target)
    return i if i < len(nums) and nums[i] == target else -1


def _search_range(nums, target):
    lo = bisect.bisect_left(nums, target)
    hi = bisect.bisect_right(nums, target) - 1
    return [lo, hi] if lo <= hi else [-1, -1]


def _two_sum_sorted(numbers, target):
    """1-indexed, the classic convention for this problem."""
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return []


def _search_rotated(nums, target):
    try:
        return nums.index(target)
    except ValueError:
        return -1


def _find_min_rotated(nums):
    return min(nums)


def _lis(nums):
    if not nums:
        return 0
    tails = []
    for v in nums:
        i = bisect.bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)


def _closest_elements(arr, k, x):
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])


def g_sorted_target(rng):
    arr = sorted(rng.randint(-30, 30) for _ in range(rng.randint(0, 18)))
    return (arr, rng.randint(-35, 35))


def g_sorted_unique_target(rng):
    n = rng.randint(0, 15)
    arr = sorted(rng.sample(range(-40, 40), n))
    return (arr, rng.randint(-45, 45))


def g_rotated(rng):
    n = rng.randint(1, 14)
    arr = sorted(rng.sample(range(-40, 40), n))
    k = rng.randrange(n)
    arr = arr[k:] + arr[:k]
    return (arr, rng.choice(arr + [999]))


def g_rotated_only(rng):
    n = rng.randint(1, 14)
    arr = sorted(rng.sample(range(-40, 40), n))
    k = rng.randrange(n)
    return (arr[k:] + arr[:k],)


def g_lis(rng):
    return ([rng.randint(-20, 20) for _ in range(rng.randint(0, 15))],)


def g_closest(rng):
    n = rng.randint(1, 12)
    arr = sorted(rng.sample(range(-30, 30), n))
    return (arr, rng.randint(1, n), rng.randint(-35, 35))


_FIRST_BAD = [1]        # the threshold the current trial was built with


def b_first_bad(module, rng):
    """
    Supplies the `is_bad_version` oracle the problem assumes exists.

    LeetCode hands this problem a given API; this exercise file never defines
    one, so without injecting it the problem is unsolvable as written. The
    threshold is also parked in `_FIRST_BAD` so the reference can read it --
    looking the module up in `sys.modules` worked under check.py but not in the
    web platform, where a submission is a namespace dict and not a module.
    """
    n = rng.randint(1, 200)
    first_bad = rng.randint(1, n)
    _FIRST_BAD[0] = first_bad
    module.is_bad_version = lambda v: v >= first_bad
    return (n,)


def _ref_first_bad(n):
    """The first bad version is the threshold, by construction."""
    return _FIRST_BAD[0]


def g_mountain(rng):
    """A strict mountain: up then down, with a single unambiguous peak."""
    up = rng.randint(1, 6)
    down = rng.randint(1, 6)
    peak = rng.randint(50, 100)
    left = sorted(rng.sample(range(0, 50), up))
    right = sorted(rng.sample(range(0, 50), down), reverse=True)
    return (left + [peak] + right,)


def _ref_peak_index(arr):
    return arr.index(max(arr))


SPECS = [
    spec(1, "binary_search", ref=_binary_search, gen=g_sorted_unique_target,
         cases=[(([-1, 0, 3, 5, 9, 12], 9), 4),
                (([-1, 0, 3, 5, 9, 12], 2), -1),
                (([], 1), -1)]),
    spec(2, "search_insert", ref=lambda a, t: bisect.bisect_left(a, t),
         gen=g_sorted_unique_target,
         cases=[(([1, 3, 5, 6], 5), 2), (([1, 3, 5, 6], 2), 1),
                (([1, 3, 5, 6], 7), 4), (([], 1), 0)]),
    spec(4, "is_perfect_square",
         ref=lambda n: math.isqrt(n) ** 2 == n if n >= 0 else False,
         gen=lambda r: (r.randint(0, 100000),),
         cases=[((16,), True), ((14,), False), ((1,), True), ((0,), True)]),
    spec(5, "search_range", ref=_search_range, gen=g_sorted_target,
         cases=[(([5, 7, 7, 8, 8, 10], 8), [3, 4]),
                (([5, 7, 7, 8, 8, 10], 6), [-1, -1]),
                (([], 0), [-1, -1])]),
    spec(6, "two_sum", ref=_two_sum_sorted,
         gen=lambda r: (sorted(r.randint(-20, 20)
                               for _ in range(r.randint(2, 12))),
                        r.randint(-30, 30)),
         cases=[(([2, 7, 11, 15], 9), [1, 2])],
         note="1-indexed result, as the problem states"),
    spec(7, "search_rotated", ref=_search_rotated, gen=g_rotated,
         cases=[(([4, 5, 6, 7, 0, 1, 2], 0), 4),
                (([4, 5, 6, 7, 0, 1, 2], 3), -1),
                (([1], 1), 0)]),
    spec(8, "find_min", ref=_find_min_rotated, gen=g_rotated_only,
         cases=[(([3, 4, 5, 1, 2],), 1), (([1],), 1),
                (([4, 5, 6, 7, 0, 1, 2],), 0)]),
    spec(9, "search_rotated_dup", ref=lambda a, t: t in a,
         gen=lambda r: ([r.randint(0, 4) for _ in range(r.randint(1, 12))],
                        r.randint(0, 5)),
         cases=[(([2, 5, 6, 0, 0, 1, 2], 0), True),
                (([2, 5, 6, 0, 0, 1, 2], 3), False)]),
    spec(10, "length_of_lis", ref=_lis, gen=g_lis,
         cases=[(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([],), 0),
                (([7, 7, 7],), 1)]),
    spec(12, "find_closest_elements", ref=_closest_elements, gen=g_closest,
         cases=[(([1, 2, 3, 4, 5], 4, 3), [1, 2, 3, 4]),
                (([1, 2, 3, 4, 5], 4, -1), [1, 2, 3, 4])]),

    spec(3, "first_bad_version", ref=_ref_first_bad, build=b_first_bad,
         trials=60,
         note="the tests give you `is_bad_version(v)` as a module-level "
              "function -- call it, do not implement it. Versions are 1..n "
              "and the answer is the first v where it returns True"),

    spec(11, "peak_index", ref=_ref_peak_index, gen=g_mountain,
         cases=[(([0, 2, 5, 3, 1],), 2), (([1, 2],), 1), (([2, 1],), 0)],
         note="the array strictly increases then strictly decreases, so the "
              "peak is unique"),
]
