"""Specs for Rosetta module 24 -- Numbers."""

import math

from ..spec import spec


def _ref_hailstone(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def _ref_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


SPECS = [
    spec(1, "factorial", ref=math.factorial,
         gen=lambda r: (r.randint(0, 60),),
         cases=[((0,), 1), ((1,), 1), ((5,), 120), ((10,), 3628800)],
         note="0! is 1 -- the empty product"),

    spec(2, "gcd", ref=math.gcd,
         gen=lambda r: (r.randint(-500, 500), r.randint(-500, 500)),
         cases=[((48, 18), 6), ((0, 5), 5), ((5, 0), 5), ((0, 0), 0),
                ((-4, 6), 2), ((17, 17), 17)],
         note="always non-negative, and gcd(0, n) is n"),

    spec(3, "lcm", ref=math.lcm,
         gen=lambda r: (r.randint(-300, 300), r.randint(-300, 300)),
         cases=[((4, 6), 12), ((0, 5), 0), ((21, 6), 42), ((-4, 6), 12)],
         note="non-negative; lcm with 0 is 0 and must not divide by zero"),

    spec(4, "hailstone", ref=_ref_hailstone,
         gen=lambda r: (r.randint(1, 5000),),
         cases=[((1,), [1]), ((2,), [2, 1]),
                ((7,), [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16,
                        8, 4, 2, 1])],
         note="include both the starting number and the final 1"),

    spec(5, "is_happy", ref=_ref_happy,
         gen=lambda r: (r.randint(1, 2000),),
         cases=[((1,), True), ((7,), True), ((4,), False), ((100,), True),
                ((2,), False)],
         note="you must detect the cycle, or an unhappy number loops forever"),
]
