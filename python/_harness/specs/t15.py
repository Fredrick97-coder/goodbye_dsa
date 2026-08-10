"""Specs for Topic 15 -- Greedy Algorithms."""

import heapq
import itertools
from collections import Counter

from ..spec import spec


def _activity_selection(activities):
    """Max non-overlapping count. Only the COUNT is compared, since several
    equally-large selections can be valid."""
    n = len(activities)
    for r in range(n, 0, -1):
        for combo in itertools.combinations(activities, r):
            srt = sorted(combo, key=lambda x: x[0])
            if all(srt[i][1] <= srt[i + 1][0] for i in range(len(srt) - 1)):
                return r
    return 0


def _fractional_knapsack(items, capacity):
    remaining = float(capacity)
    total = 0.0
    for w, v in sorted(items, key=lambda t: -t[1] / t[0]):
        if remaining <= 0:
            break
        take = min(w, remaining)
        total += v * take / w
        remaining -= take
    return total


def _min_coins_standard(amount):
    left = amount
    count = 0
    for c in (25, 10, 5, 1):
        count += left // c
        left %= c
    return count


def _job_sequencing(jobs):
    """Max profit. jobs are (id, deadline, profit)."""
    best = 0
    n = len(jobs)
    for r in range(n, 0, -1):
        for combo in itertools.combinations(jobs, r):
            # feasible iff we can order them so each meets its deadline
            srt = sorted(combo, key=lambda j: j[1])
            if all(srt[i][1] >= i + 1 for i in range(len(srt))):
                best = max(best, sum(j[2] for j in combo))
    return best


def _max_product(nums):
    """Maximum product of a contiguous subarray."""
    if not nums:
        return 0
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best


def _assign_cookies(children, cookies):
    kids = sorted(children)
    cs = sorted(cookies)
    i = j = 0
    while i < len(kids) and j < len(cs):
        if cs[j] >= kids[i]:
            i += 1
        j += 1
    return i


def _min_meeting_rooms(meetings):
    if not meetings:
        return 0
    lo = min(s for s, _ in meetings)
    hi = max(e for _, e in meetings)
    return max((sum(1 for s, e in meetings if s <= t < e)
                for t in range(lo, hi + 1)), default=0)


def _max_area(heights):
    return max((min(heights[i], heights[j]) * (j - i)
                for i in range(len(heights))
                for j in range(i + 1, len(heights))), default=0)


def _gas_station(gas, cost):
    n = len(gas)
    for start in range(n):
        tank = 0
        ok = True
        for k in range(n):
            i = (start + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return start
    return -1


def g_intervals(rng, nmax=7):
    iv = []
    for _ in range(rng.randint(0, nmax)):
        a = rng.randint(0, 18)
        iv.append((a, a + rng.randint(1, 8)))
    return (iv,)


def g_knapsack(rng):
    items = [(rng.randint(1, 20), rng.randint(1, 40))
             for _ in range(rng.randint(0, 8))]
    return (items, float(rng.randint(0, 50)))


def g_jobs(rng):
    n = rng.randint(0, 6)
    return ([(f"J{i}", rng.randint(1, 4), rng.randint(10, 100))
             for i in range(n)],)


def g_gas(rng):
    n = rng.randint(1, 8)
    gas = [rng.randint(0, 8) for _ in range(n)]
    cost = [rng.randint(0, 8) for _ in range(n)]
    return (gas, cost)


SPECS = [
    spec(1, "activity_selection", prop=lambda x: None if x is None else len(x),
         ref=_activity_selection, gen=g_intervals,
         cases=[(([(1, 3), (2, 5), (4, 6), (6, 7), (5, 8), (8, 9)],), 4)],
         note="only the COUNT is compared; ties are legitimate"),
    spec(2, "fractional_knapsack", ref=_fractional_knapsack, gen=g_knapsack,
         tol=1e-6,
         cases=[(([(10, 60), (20, 100), (30, 120)], 50), 240.0),
                (([], 10), 0.0)]),
    spec(4, "min_coins_standard", ref=_min_coins_standard,
         gen=lambda r: (r.randint(0, 500),),
         cases=[((0,), 0), ((41,), 4), ((99,), 9)],
         note="US coins 25/10/5/1, where greedy IS optimal"),
    spec(5, "job_sequencing", ref=_job_sequencing, gen=g_jobs,
         cases=[(([("J1", 2, 100), ("J2", 1, 50),
                   ("J3", 3, 30), ("J4", 2, 40)],), 180),
                (([],), 0)]),
    spec(6, "interval_schedule", prop=lambda x: None if x is None else len(x),
         ref=_activity_selection, gen=g_intervals,
         cases=[(([(1, 3), (2, 4), (4, 6), (6, 7)],), 3)]),
    spec(7, "max_product", ref=_max_product,
         gen=lambda r: ([r.randint(-4, 4) for _ in range(r.randint(1, 10))],),
         cases=[(([2, 3, -2, 4],), 6), (([-2, 0, -1],), 0)]),
    spec(8, "assign_cookies", ref=_assign_cookies,
         gen=lambda r: ([r.randint(1, 9) for _ in range(r.randint(0, 8))],
                        [r.randint(1, 9) for _ in range(r.randint(0, 8))]),
         cases=[(([1, 2, 3], [1, 1]), 1), (([1, 2], [1, 2, 3]), 2)]),
    spec(9, "min_meeting_rooms", ref=_min_meeting_rooms, gen=g_intervals,
         cases=[(([(0, 30), (5, 10), (15, 20)],), 2), (([],), 0)]),
    spec(10, "max_area", ref=_max_area,
         gen=lambda r: ([r.randint(0, 12) for _ in range(r.randint(0, 12))],),
         cases=[(([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49), (([1],), 0)]),
    spec(11, "gas_station", ref=_gas_station, gen=g_gas,
         cases=[(([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3),
                (([2, 3, 4], [3, 4, 3]), -1)]),
]
