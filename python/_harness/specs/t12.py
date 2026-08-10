"""Specs for Topic 12 -- Dynamic Programming."""

import functools
import itertools
import math

from ..spec import spec


def _fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _climb(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _rob(nums):
    take, skip = 0, 0
    for v in nums:
        take, skip = skip + v, max(skip, take)
    return max(take, skip)


def _coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]


def _lcs(a, b):
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for j, cb in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ca == cb
                       else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def _edit(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    half = total // 2
    reach = {0}
    for v in nums:
        reach |= {r + v for r in reach if r + v <= half}
    return half in reach


def _knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def _lis(nums):
    if not nums:
        return 0
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)


def _word_break(s, words):
    wset = set(words)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in wset for j in range(i))
    return dp[-1]


def _change(coins, amount):
    """Coin Change II -- count the combinations."""
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


def g_small_n(rng, hi=25):
    return (rng.randint(0, hi),)


def g_coins(rng):
    coins = sorted(set(rng.randint(1, 12) for _ in range(rng.randint(1, 4))))
    return (coins, rng.randint(0, 40))


def g_two_str(rng, hi=9):
    def s():
        return "".join(rng.choice("abc") for _ in range(rng.randint(0, hi)))
    return (s(), s())


def g_int_list(rng, lo=1, hi=20, nmin=0, nmax=12):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_knapsack(rng):
    n = rng.randint(0, 8)
    return ([rng.randint(1, 10) for _ in range(n)],
            [rng.randint(1, 20) for _ in range(n)],
            rng.randint(0, 25))


def g_grid(rng):
    return (rng.randint(1, 8), rng.randint(1, 8))


SPECS = [
    spec(1, "fib", ref=_fib, gen=lambda r: g_small_n(r, 30),
         cases=[((0,), 0), ((1,), 1), ((10,), 55), ((30,), 832040)]),
    spec(2, "climb_stairs", ref=_climb, gen=lambda r: g_small_n(r, 30),
         cases=[((1,), 1), ((2,), 2), ((3,), 3), ((5,), 8)],
         note="climb_stairs(n) = Fibonacci(n+1)"),
    spec(3, "rob", ref=_rob, gen=g_int_list,
         cases=[(([1, 2, 3, 1],), 4), (([2, 7, 9, 3, 1],), 12), (([],), 0)]),
    spec(4, "unique_paths", ref=lambda m, n: math.comb(m + n - 2, m - 1),
         gen=g_grid,
         cases=[((3, 7), 28), ((1, 1), 1), ((3, 2), 3)]),
    spec(5, "coin_change", ref=_coin_change, gen=g_coins,
         cases=[(([1, 2, 5], 11), 3), (([2], 3), -1), (([1], 0), 0)]),
    spec(6, "lcs_length", ref=_lcs, gen=g_two_str,
         cases=[(("abcde", "ace"), 3), (("abc", "abc"), 3),
                (("abc", "def"), 0)]),
    spec(7, "edit_distance", ref=_edit, gen=g_two_str,
         cases=[(("horse", "ros"), 3), (("intention", "execution"), 5),
                (("", ""), 0)]),
    spec(8, "can_partition", ref=_can_partition,
         gen=lambda r: g_int_list(r, 1, 15, 1, 10),
         cases=[(([1, 5, 11, 5],), True), (([1, 2, 3, 5],), False),
                (([1],), False)]),
    spec(9, "knapsack", ref=_knapsack, gen=g_knapsack,
         cases=[(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9),
                (([], [], 5), 0)]),
    spec(10, "lis_length", ref=_lis, gen=lambda r: g_int_list(r, -20, 20, 0, 14),
         cases=[(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([],), 0)]),
    spec(11, "word_break", ref=_word_break,
         gen=lambda r: ("".join(r.choice("ab") for _ in range(r.randint(0, 10))),
                        ["a", "b", "ab", "ba", "aab"]),
         cases=[(("leetcode", ["leet", "code"]), True),
                (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False)]),
    spec(12, "change", ref=_change, gen=g_coins,
         cases=[(([1, 2, 5], 5), 4), (([2], 3), 0), (([1], 0), 1)],
         note="counts COMBINATIONS, so order does not matter"),
]
