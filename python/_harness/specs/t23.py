"""Specs for Rosetta module 23 -- Warm-up."""

import string

from ..spec import spec


def _ref_fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        word = ("FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0
                else "Buzz" if i % 5 == 0 else str(i))
        out.append(word)
    return out


def _ref_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _ref_sum_multiples(limit):
    return sum(i for i in range(1, limit) if i % 3 == 0 or i % 5 == 0)


def _ref_ascii_range(first, last):
    return [chr(c) for c in range(ord(first), ord(last) + 1)]


def _ref_open_doors(n):
    """
    Brute force on purpose: toggle every door on every pass.

    The closed form is the perfect squares, but a reference should be the
    obvious reading of the task -- if the two disagree, the interesting
    possibility is that my clever version is wrong.
    """
    doors = [False] * (n + 1)
    for step in range(1, n + 1):
        for door in range(step, n + 1, step):
            doors[door] = not doors[door]
    return [i for i in range(1, n + 1) if doors[i]]


SPECS = [
    spec(1, "fizzbuzz", ref=_ref_fizzbuzz,
         gen=lambda r: (r.randint(0, 40),),
         cases=[((5,), ["1", "2", "Fizz", "4", "Buzz"]),
                ((0,), []),
                ((15,), ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
                         "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"])],
         note="numbers come back as STRINGS, and 15 is FizzBuzz rather than "
              "Fizz followed by Buzz"),

    spec(2, "is_leap_year", ref=_ref_leap,
         gen=lambda r: (r.randint(1, 4000),),
         cases=[((1900,), False), ((2000,), True), ((2024,), True),
                ((2023,), False), ((1600,), True), ((2100,), False)],
         note="1900 is the case a naive rule fails: divisible by 4 and 100 but "
              "not 400"),

    spec(3, "sum_multiples", ref=_ref_sum_multiples,
         gen=lambda r: (r.randint(0, 2000),),
         cases=[((10,), 23), ((1,), 0), ((16,), 60)],
         note="strictly below the limit, and 15 counts once"),

    spec(4, "ascii_range", ref=_ref_ascii_range,
         gen=lambda r: tuple(sorted(r.sample(string.ascii_lowercase, 2))),
         cases=[(("a", "e"), ["a", "b", "c", "d", "e"]),
                (("h", "p"), list("hijklmnop")),
                (("c", "c"), ["c"]),
                (("e", "a"), [])],
         note="inclusive at both ends; an empty list when last precedes first"),

    spec(5, "open_doors", ref=_ref_open_doors,
         gen=lambda r: (r.randint(0, 120),),
         cases=[((10,), [1, 4, 9]), ((100,), [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]),
                ((0,), [])],
         note="door numbers are 1-based"),
]
