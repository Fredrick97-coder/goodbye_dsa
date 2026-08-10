"""Specs for Topic 22 -- Math for Interviews.

Almost every reference here is the standard library (math.gcd, math.comb,
math.isqrt, pow, int(s, base)), which is the strongest kind of check
available: independently implemented, in C, and widely trusted.
"""

import math
from fractions import Fraction

from ..spec import spec

# ------------------------------------------------------------- references


def _ref_is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _ref_sieve(n):
    return [i for i in range(2, n + 1) if _ref_is_prime(i)]


def _ref_gcd(a, b):
    return math.gcd(a, b)


def _ref_lcm(a, b):
    return math.lcm(a, b)


def _ref_power(a, b, mod=0):
    return pow(a, b, mod) if mod else a ** b


def _ref_digits(n):
    n = abs(n)
    return [int(c) for c in reversed(str(n))]


def _ref_digit_sum(n):
    return sum(int(c) for c in str(abs(n)))


def _ref_reverse_number(n):
    sign = -1 if n < 0 else 1
    return sign * int(str(abs(n))[::-1])


def _ref_count_digits(n):
    return len(str(abs(n)))


def _ref_is_pal_num(n):
    return n >= 0 and str(n) == str(n)[::-1]


def _ref_factorise(n):
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def _ref_mod_inverse(a, m):
    return pow(a, -1, m)


def _ref_comb(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def _ref_pascal(rows):
    return [[math.comb(n, k) for k in range(n + 1)] for n in range(rows + 1)]


def _ref_comb_mod(n, k, p):
    return math.comb(n, k) % p if 0 <= k <= n else 0


DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _ref_to_base(n, base):
    if n == 0:
        return "0"
    neg, n = n < 0, abs(n)
    out = []
    while n:
        out.append(DIGITS[n % base])
        n //= base
    return ("-" if neg else "") + "".join(reversed(out))


def _ref_from_base(s, base):
    return int(s, base)


def _ref_is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(c) ** 2 for c in str(n))
    return n == 1


def _ref_trailing_zeroes(n):
    count = 0
    p = 5
    while p <= n:
        count += n // p
        p *= 5
    return count


INT_MAX, INT_MIN = 2 ** 31 - 1, -2 ** 31


def _ref_reverse_32(n):
    r = _ref_reverse_number(n)
    return 0 if r < INT_MIN or r > INT_MAX else r


def _ref_divide(a, b):
    """C-style truncation toward zero, which is what the problem asks for."""
    sign = -1 if (a < 0) != (b < 0) else 1
    q = sign * (abs(a) // abs(b))
    return max(INT_MIN, min(INT_MAX, q))


def _ref_sqrt(n):
    return math.isqrt(n)


def _ref_my_pow(x, n):
    return x ** n


def _ref_col_title(n):
    out = []
    while n:
        n, rem = divmod(n - 1, 26)
        out.append(chr(ord("A") + rem))
    return "".join(reversed(out))


def _ref_from_col_title(s):
    total = 0
    for ch in s:
        total = total * 26 + (ord(ch) - ord("A") + 1)
    return total


def _ref_fraction(numerator, denominator):
    """Long division with remainder tracking."""
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) != (denominator < 0) else ""
    n, d = abs(numerator), abs(denominator)
    whole, rem = divmod(n, d)
    if rem == 0:
        return f"{sign}{whole}"
    seen = {}
    frac = []
    while rem and rem not in seen:
        seen[rem] = len(frac)
        rem *= 10
        frac.append(str(rem // d))
        rem %= d
    if rem:
        i = seen[rem]
        body = "".join(frac[:i]) + "(" + "".join(frac[i:]) + ")"
    else:
        body = "".join(frac)
    return f"{sign}{whole}.{body}"


def _ref_segmented_sieve(lo, hi):
    return [n for n in range(max(2, lo), hi + 1) if _ref_is_prime(n)]


def _ref_crt(remainders, moduli):
    """Combine pairwise. Returns None when the moduli are not coprime."""
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if math.gcd(moduli[i], moduli[j]) != 1:
                return None
    x, m = 0, 1
    for a, n in zip(remainders, moduli):
        # solve x + m*t == a (mod n)
        t = ((a - x) * pow(m, -1, n)) % n
        x += m * t
        m *= n
    return x % m


def _ref_miller_rabin(n, witnesses=None):
    return _ref_is_prime(n)


def _ref_count_primes(n):
    return len(_ref_sieve(n))


def _ref_array_gcd(nums):
    g = 0
    for v in nums:
        g = math.gcd(g, v)
    return g


def _ref_distinct_subarray_gcds(nums):
    seen = set()
    for i in range(len(nums)):
        g = 0
        for j in range(i, len(nums)):
            g = math.gcd(g, nums[j])
            seen.add(g)
    return len(seen)


def _ref_spf_sieve(n):
    spf = list(range(n + 1))
    for i in range(2, math.isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


# ------------------------------------------------------------- generators


def g_small_int(rng, lo=0, hi=5000):
    return (rng.randint(lo, hi),)


def g_two_pos(rng):
    return (rng.randint(1, 5000), rng.randint(1, 5000))


def g_pow(rng):
    return (rng.randint(0, 50), rng.randint(0, 30), rng.choice([0, 97, 10 ** 9 + 7]))


def g_any_int(rng):
    return (rng.randint(-10 ** 9, 10 ** 9),)


def g_n_k(rng):
    n = rng.randint(0, 40)
    return (n, rng.randint(0, n))


def g_base(rng):
    return (rng.randint(-10 ** 6, 10 ** 6), rng.randint(2, 36))


def g_base_str(rng):
    base = rng.randint(2, 36)
    n = rng.randint(0, 10 ** 6)
    return (_ref_to_base(n, base), base)


def g_divide(rng):
    b = rng.choice([x for x in range(-50, 51) if x != 0])
    return (rng.randint(-10 ** 6, 10 ** 6), b)


def g_fraction(rng):
    d = rng.choice([x for x in range(-30, 31) if x != 0])
    return (rng.randint(-40, 40), d)


def g_int_list(rng):
    return ([rng.randint(1, 60) for _ in range(rng.randint(1, 12))],)


SPECS = [
    spec(1, "is_prime", ref=_ref_is_prime, gen=lambda r: g_small_int(r, 0, 20000),
         cases=[((0,), False), ((1,), False), ((2,), True), ((3,), True),
                ((4,), False), ((97,), True), ((91,), False),
                ((7919,), True), ((-5,), False)]),
    spec(2, "sieve", ref=_ref_sieve, gen=lambda r: (r.randint(0, 600),),
         cases=[((0,), []), ((1,), []), ((2,), [2]),
                ((30,), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])]),
    spec(2, "sieve", prop=lambda x: None if x is None else len(x),
         cases=[((100,), 25), ((1000,), 168), ((10000,), 1229)],
         note="known prime counts"),
    spec(3, "gcd", ref=_ref_gcd, gen=g_two_pos,
         cases=[((48, 18), 6), ((1071, 462), 21), ((17, 5), 1),
                ((610, 377), 1), ((100, 100), 100)]),
    spec(3, "lcm", ref=_ref_lcm, gen=g_two_pos,
         cases=[((4, 6), 12), ((12, 18), 36), ((7, 5), 35)]),
    spec(4, "power", ref=_ref_power, gen=g_pow,
         cases=[((2, 10, 0), 1024), ((3, 0, 0), 1),
                ((2, 100, 10 ** 9 + 7), pow(2, 100, 10 ** 9 + 7))]),
    spec(5, "digits_of", ref=_ref_digits, gen=g_any_int,
         cases=[((1234,), [4, 3, 2, 1]), ((0,), [0]), ((-45,), [5, 4])]),
    spec(5, "digit_sum", ref=_ref_digit_sum, gen=g_any_int,
         cases=[((1234,), 10), ((0,), 0), ((-99,), 18)]),
    spec(5, "reverse_number", ref=_ref_reverse_number, gen=g_any_int,
         cases=[((1234,), 4321), ((-456,), -654), ((0,), 0), ((1200,), 21)]),
    spec(6, "count_digits", ref=_ref_count_digits, gen=g_any_int,
         cases=[((12345,), 5), ((0,), 1), ((1000,), 4), ((999999,), 6),
                ((-7,), 1)]),
    spec(7, "is_palindrome_number", ref=_ref_is_pal_num,
         gen=lambda r: (r.randint(-2000, 2000),),
         cases=[((12321,), True), ((-121,), False), ((10,), False),
                ((0,), True)]),
    spec(8, "factorise", ref=_ref_factorise,
         gen=lambda r: (r.randint(2, 50000),),
         cases=[((60,), {2: 2, 3: 1, 5: 1}), ((97,), {97: 1}),
                ((1024,), {2: 10})]),
    spec(9, "spf_sieve", ref=_ref_spf_sieve,
         gen=lambda r: (r.randint(2, 300),),
         cases=[((10,), [0, 1, 2, 3, 2, 5, 2, 7, 2, 3, 2])]),
    spec(10, "mod_inverse", ref=_ref_mod_inverse,
         gen=lambda r: (r.randint(1, 10 ** 6), 10 ** 9 + 7),
         cases=[((3, 11), 4), ((7, 13), 2)]),
    spec(11, "comb", ref=_ref_comb, gen=g_n_k,
         cases=[((5, 2), 10), ((52, 5), 2598960), ((1000, 998), 499500),
                ((5, 0), 1), ((5, 6), 0), ((5, -1), 0)]),
    spec(12, "pascal_triangle", ref=_ref_pascal,
         gen=lambda r: (r.randint(0, 12),),
         cases=[((4,), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1],
                        [1, 4, 6, 4, 1]])]),
    spec(13, "comb_mod", ref=_ref_comb_mod,
         gen=lambda r: (lambda n: (n, r.randint(0, n), 10 ** 9 + 7))(
             r.randint(0, 200)),
         cases=[((20, 7, 10 ** 9 + 7), math.comb(20, 7)),
                ((100, 50, 10 ** 9 + 7), math.comb(100, 50) % (10 ** 9 + 7))]),
    spec(14, "to_base", ref=_ref_to_base, gen=g_base,
         cases=[((255, 16), "FF"), ((0, 2), "0"), ((10, 2), "1010"),
                ((-5, 2), "-101")]),
    spec(14, "from_base", ref=_ref_from_base, gen=g_base_str,
         cases=[(("FF", 16), 255), (("1010", 2), 10), (("0", 8), 0)]),
    spec(15, "is_happy", ref=_ref_is_happy, gen=lambda r: (r.randint(1, 5000),),
         cases=[((19,), True), ((2,), False), ((1,), True), ((7,), True)]),
    spec(16, "trailing_zeroes", ref=_ref_trailing_zeroes,
         gen=lambda r: (r.randint(0, 100000),),
         cases=[((25,), 6), ((5,), 1), ((0,), 0), ((100,), 24),
                ((1000,), 249)]),
    spec(17, "reverse_integer_32", ref=_ref_reverse_32, gen=g_any_int,
         cases=[((123,), 321), ((-456,), -654), ((1534236469,), 0),
                ((0,), 0), ((1000000003,), 0)]),
    spec(18, "divide", ref=_ref_divide, gen=g_divide,
         cases=[((10, 3), 3), ((-7, 2), -3), ((7, -2), -3), ((-7, -2), 3),
                ((1, 1), 1)],
         note="C-style truncation toward zero, NOT Python's floor"),
    spec(19, "my_sqrt", ref=_ref_sqrt, gen=lambda r: (r.randint(0, 10 ** 9),),
         cases=[((8,), 2), ((16,), 4), ((0,), 0), ((1,), 1),
                ((2147395599,), 46339)]),
    spec(20, "my_pow", ref=_ref_my_pow, tol=1e-9,
         gen=lambda r: (round(r.uniform(-3, 3), 4), r.randint(-8, 8)),
         cases=[((2.0, 10), 1024.0), ((2.0, -2), 0.25), ((2.0, 0), 1.0)]),
    spec(21, "to_column_title", ref=_ref_col_title,
         gen=lambda r: (r.randint(1, 10 ** 6),),
         cases=[((1,), "A"), ((26,), "Z"), ((27,), "AA"), ((28,), "AB"),
                ((701,), "ZY"), ((702,), "ZZ"), ((703,), "AAA")]),
    spec(21, "from_column_title", ref=_ref_from_col_title,
         gen=lambda r: (_ref_col_title(r.randint(1, 10 ** 6)),),
         cases=[(("A",), 1), (("Z",), 26), (("AA",), 27), (("ZY",), 701)]),
    spec(22, "fraction_to_decimal", ref=_ref_fraction, gen=g_fraction,
         cases=[((1, 2), "0.5"), ((2, 1), "2"), ((1, 6), "0.1(6)"),
                ((4, 333), "0.(012)"), ((0, 5), "0"), ((-1, 2), "-0.5")]),
    spec(23, "segmented_sieve", ref=_ref_segmented_sieve,
         gen=lambda r: (lambda lo: (lo, lo + r.randint(0, 200)))(
             r.randint(0, 5000)),
         cases=[((10, 30), [11, 13, 17, 19, 23, 29]), ((0, 1), []),
                ((2, 2), [2])]),
    spec(24, "crt", ref=_ref_crt,
         gen=lambda r: (lambda ms: ([r.randrange(m) for m in ms], ms))(
             r.sample([3, 5, 7, 11, 13], r.randint(1, 4))),
         cases=[(([2, 3, 2], [3, 5, 7]), 23), (([0], [5]), 0)]),
    spec(25, "miller_rabin", ref=_ref_miller_rabin,
         gen=lambda r: (r.randint(0, 200000), None),
         cases=[((2, None), True), ((561, None), False),
                ((1000000007, None), True), ((1, None), False)],
         note="561 is a Carmichael number -- a naive Fermat test fails it"),
    spec(26, "count_primes", ref=_ref_count_primes,
         gen=lambda r: (r.randint(0, 2000),),
         cases=[((10,), 4), ((100,), 25), ((1000,), 168), ((0,), 0),
                ((2,), 1)]),
    spec(27, "array_gcd", ref=_ref_array_gcd, gen=g_int_list,
         cases=[(([12, 18, 24],), 6), (([7],), 7), (([5, 10, 15],), 5)]),
    spec(27, "distinct_subarray_gcds", ref=_ref_distinct_subarray_gcds,
         gen=g_int_list,
         cases=[(([6, 10, 3],), 5), (([4],), 1)],
         note="gcds of [6,10,3] subarrays: {6,10,3,2,1} = 5"),
]
