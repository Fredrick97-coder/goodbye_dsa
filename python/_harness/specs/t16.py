"""Specs for Topic 16 -- Bit Manipulation."""

import itertools
import math

from ..spec import as_set_of_tuples, spec

MASK32 = 0xFFFFFFFF


def _reverse_bits(n):
    return int(format(n & MASK32, "032b")[::-1], 2)


def _two_singles(nums):
    return tuple(sorted(v for v in set(nums) if nums.count(v) == 1))


def _single_three(nums):
    for v in set(nums):
        if nums.count(v) == 1:
            return v
    return 0


def _max_xor(nums):
    return max((a ^ b for a, b in itertools.combinations(nums, 2)), default=0)


def _all_subsets(items):
    return [list(c) for r in range(len(items) + 1)
            for c in itertools.combinations(items, r)]


def _tsp(dist):
    """Brute force over permutations -- independent of the bitmask DP."""
    n = len(dist)
    if n <= 1:
        return 0
    best = float("inf")
    for perm in itertools.permutations(range(1, n)):
        route = (0,) + perm + (0,)
        best = min(best, sum(dist[route[i]][route[i + 1]]
                             for i in range(len(route) - 1)))
    return best


def _max_prod_words(words):
    best = 0
    for a, b in itertools.combinations(words, 2):
        if not (set(a) & set(b)):
            best = max(best, len(a) * len(b))
    return best


def g_n(rng, lo=0, hi=10 ** 6):
    return (rng.randint(lo, hi),)


def g_pairs_plus_one(rng):
    """Every value twice except one -- for single_number."""
    vals = rng.sample(range(1, 200), rng.randint(1, 8))
    loner = rng.randint(200, 300)
    arr = [v for v in vals for _ in (0, 1)] + [loner]
    rng.shuffle(arr)
    return (arr,)


def g_pairs_plus_two(rng):
    vals = rng.sample(range(1, 200), rng.randint(0, 8))
    a, b = rng.sample(range(200, 300), 2)
    arr = [v for v in vals for _ in (0, 1)] + [a, b]
    rng.shuffle(arr)
    return (arr,)


def g_triples_plus_one(rng):
    vals = rng.sample(range(1, 200), rng.randint(0, 6))
    loner = rng.randint(200, 300)
    arr = [v for v in vals for _ in range(3)] + [loner]
    rng.shuffle(arr)
    return (arr,)


def g_missing(rng):
    n = rng.randint(1, 25)
    arr = list(range(n + 1))
    arr.remove(rng.randrange(n + 1))
    rng.shuffle(arr)
    return (arr,)


def g_n_i(rng):
    return (rng.randint(0, 10 ** 6), rng.randint(0, 19))


def g_dist(rng):
    n = rng.randint(1, 7)
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w = rng.randint(1, 40)
            m[i][j] = m[j][i] = w
    return (m,)


SPECS = [
    spec(1, "count_set_bits", ref=lambda n: bin(n).count("1"), gen=g_n,
         cases=[((11,), 3), ((0,), 0), ((255,), 8), ((1024,), 1)]),
    spec(2, "is_power_of_two", ref=lambda n: n > 0 and n & (n - 1) == 0,
         gen=lambda r: (r.randint(-5, 5000),),
         cases=[((16,), True), ((12,), False), ((1,), True), ((0,), False),
                ((-8,), False)]),
    spec(3, "single_number", ref=_single_three, gen=g_pairs_plus_one,
         cases=[(([4, 1, 2, 1, 2],), 4), (([1],), 1)]),
    spec(4, "get_bit", ref=lambda n, i: (n >> i) & 1, gen=g_n_i,
         cases=[((10, 1), 1), ((10, 2), 0), ((10, 0), 0)]),
    spec(4, "set_bit", ref=lambda n, i: n | (1 << i), gen=g_n_i,
         cases=[((10, 0), 11), ((10, 1), 10)]),
    spec(4, "clear_bit", ref=lambda n, i: n & ~(1 << i), gen=g_n_i,
         cases=[((10, 3), 2), ((10, 2), 10)]),
    spec(5, "missing_number",
         ref=lambda a: len(a) * (len(a) + 1) // 2 - sum(a), gen=g_missing,
         cases=[(([3, 0, 1],), 2), (([0],), 1)]),
    spec(6, "count_bits_range",
         ref=lambda n: [bin(i).count("1") for i in range(n + 1)],
         gen=lambda r: (r.randint(0, 200),),
         cases=[((5,), [0, 1, 1, 2, 1, 2]), ((0,), [0])]),
    spec(7, "reverse_bits", ref=_reverse_bits,
         gen=lambda r: (r.randint(0, MASK32),),
         cases=[((43261596,), 964176192), ((0,), 0)]),
    spec(8, "hamming_distance", ref=lambda x, y: bin(x ^ y).count("1"),
         gen=lambda r: (r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)),
         cases=[((1, 4), 2), ((3, 1), 1), ((0, 0), 0)]),
    spec(9, "add_without_plus", ref=lambda a, b: a + b,
         gen=lambda r: (r.randint(0, 10 ** 5), r.randint(0, 10 ** 5)),
         cases=[((7, 5), 12), ((0, 0), 0), ((13, 29), 42)],
         note="non-negative inputs only in these checks"),
    spec(10, "two_single_numbers", ref=_two_singles, gen=g_pairs_plus_two,
         norm=lambda x: tuple(sorted(x)) if x is not None else None,
         cases=[(([1, 2, 1, 3, 2, 5],), (3, 5))]),
    spec(11, "single_number_three_times", ref=_single_three,
         gen=g_triples_plus_one,
         cases=[(([2, 2, 3, 2],), 3), (([1],), 1)]),
    spec(12, "max_xor_pair", ref=_max_xor,
         gen=lambda r: ([r.randint(0, 5000) for _ in range(r.randint(2, 12))],),
         cases=[(([3, 10, 5, 25, 2, 8],), 28)]),
    spec(13, "all_subsets", ref=_all_subsets,
         gen=lambda r: (r.sample(range(1, 30), r.randint(0, 7)),),
         norm=as_set_of_tuples,
         cases=[(([1, 2],), [[], [1], [2], [1, 2]]), (([],), [[]])]),
    spec(14, "tsp", ref=_tsp, gen=g_dist,
         cases=[(([[0, 20, 42, 35], [20, 0, 30, 34],
                   [42, 30, 0, 12], [35, 34, 12, 0]],), 97)]),
    spec(15, "max_product_no_shared_letters", ref=_max_prod_words,
         gen=lambda r: (["".join(r.choice("abcd")
                                 for _ in range(r.randint(1, 5)))
                         for _ in range(r.randint(0, 8))],),
         cases=[((["abcw", "baz", "foo", "bar", "xtfn", "abcdef"],), 16),
                ((["a", "aa"],), 0)]),
    spec(16, "gray_code", ref=lambda n: [i ^ (i >> 1) for i in range(1 << n)],
         gen=lambda r: (r.randint(0, 8),),
         cases=[((2,), [0, 1, 3, 2]), ((0,), [0])]),
]
