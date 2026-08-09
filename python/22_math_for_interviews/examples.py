"""
Examples: Math for Interviews

Primes and sieves, GCD/LCM, modular arithmetic, fast exponentiation,
combinatorics, digit manipulation, base conversion, and overflow.

Every implementation is verified against brute force or the standard library.
"""

import math
import random
import time
from typing import List, Dict, Tuple

print("=" * 70)
print("MATH FOR INTERVIEWS")
print("=" * 70)

# ==================== (1) Primality and the sqrt(n) Bound ====================
print("\n[1] Primality Testing -- Why sqrt(n) Is Enough")
print("-" * 70)

def is_prime_naive(n: int) -> Tuple[bool, int]:
    """Test every divisor up to n-1. Returns (result, divisions)."""
    if n < 2:
        return False, 0
    div = 0
    for i in range(2, n):
        div += 1
        if n % i == 0:
            return False, div
    return True, div


def is_prime_sqrt(n: int) -> Tuple[bool, int]:
    """Test up to sqrt(n). Divisors come in pairs d*e = n with d <= sqrt(n)."""
    if n < 2:
        return False, 0
    div = 0
    i = 2
    while i * i <= n:                    # i*i, NOT i <= sqrt(n)
        div += 1
        if n % i == 0:
            return False, div
        i += 1
    return True, div


def is_prime_6k(n: int) -> Tuple[bool, int]:
    """6k +/- 1: every prime > 3 has that form. ~3x fewer divisions."""
    if n < 2:
        return False, 0
    if n in (2, 3):
        return True, 0
    div = 2
    if n % 2 == 0 or n % 3 == 0:
        return False, div
    i = 5
    while i * i <= n:
        div += 2
        if n % i == 0 or n % (i + 2) == 0:
            return False, div
        i += 6
    return True, div


print("  Divisors pair up: if d*e = n and d <= e, then d <= sqrt(n).")
print("  So finding no divisor at or below sqrt(n) proves primality.\n")
print("  Example: 36 = 1x36, 2x18, 3x12, 4x9, 6x6, 9x4, 12x3, 18x2, 36x1")
print("           sqrt(36) = 6, and every pair has one member <= 6.\n")

print(f"  {'n':>10} {'prime':>7} {'naive divs':>12} {'sqrt divs':>11} "
      f"{'6k+/-1 divs':>13}")
print("  " + "-" * 58)
for n in [97, 997, 10_007, 100_003, 1_000_003]:
    p1, d1 = is_prime_naive(n)
    p2, d2 = is_prime_sqrt(n)
    p3, d3 = is_prime_6k(n)
    assert p1 == p2 == p3, f"disagreement on {n}"
    print(f"  {n:>10} {str(p2):>7} {d1:>12,} {d2:>11,} {d3:>13,}")

print("\n  -> The sqrt bound turns O(n) into O(sqrt(n)): for 1,000,003 that")
print("     is ~1,000 divisions instead of ~1,000,000.")
print("  -> 6k+/-1 cuts it roughly threefold again by skipping multiples")
print("     of 2 and 3 up front.")

print("\n  Why `i * i <= n` and not `i <= math.sqrt(n)`:")
big = 10**18 + 9
print(f"    n = {big}")
print(f"    math.sqrt(n)  = {math.sqrt(big)!r}  (a float -- lossy)")
print(f"    math.isqrt(n) = {math.isqrt(big)}  (exact integer)")
print(f"    int(sqrt) == isqrt : {int(math.sqrt(big)) == math.isqrt(big)}")
print("    -> Integer multiplication is exact; float sqrt is not. Use i*i,")
print("       or math.isqrt if you want the root itself.")

print("\n  Verifying all three against each other:")
fails = 0
for n in range(0, 2000):
    a = is_prime_naive(n)[0]
    b = is_prime_sqrt(n)[0]
    c = is_prime_6k(n)[0]
    if not (a == b == c):
        fails += 1
print(f"    n from 0 to 1,999, disagreements: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# ==================== (2) Sieve of Eratosthenes ====================
print("\n[2] Sieve of Eratosthenes -- Mark, Do Not Test")
print("-" * 70)

def sieve(n: int) -> List[int]:
    """All primes <= n. O(n log log n) time, O(n) space."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False            # 0 and 1 are NOT prime
    for i in range(2, math.isqrt(n) + 1):    # outer loop stops at sqrt(n)
        if is_p[i]:
            for j in range(i * i, n + 1, i):  # inner loop STARTS at i*i
                is_p[j] = False
    return [i for i, p in enumerate(is_p) if p]


def sieve_from_2i(n: int) -> Tuple[List[int], int]:
    """Same result, inner loop from 2*i. Counts marking operations."""
    if n < 2:
        return [], 0
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    ops = 0
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            for j in range(2 * i, n + 1, i):
                is_p[j] = False
                ops += 1
    return [i for i, p in enumerate(is_p) if p], ops


def sieve_from_ii(n: int) -> Tuple[List[int], int]:
    if n < 2:
        return [], 0
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    ops = 0
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
                ops += 1
    return [i for i, p in enumerate(is_p) if p], ops


print("  Sieving to 50, step by step:")
N = 50
is_p = [True] * (N + 1)
is_p[0] = is_p[1] = False
for i in range(2, math.isqrt(N) + 1):
    if is_p[i]:
        marked = [j for j in range(i * i, N + 1, i)]
        for j in marked:
            is_p[j] = False
        print(f"    i={i}: mark multiples from {i*i:>2} -> {marked}")
print(f"\n  primes <= 50: {[i for i, p in enumerate(is_p) if p]}")

print(f"\n  Why the inner loop starts at i*i (marking operations saved):")
print(f"  {'n':>10} {'from 2i':>12} {'from i*i':>12} {'saved':>8}")
print("  " + "-" * 46)
for n in [1000, 10_000, 100_000, 1_000_000]:
    p1, o1 = sieve_from_2i(n)
    p2, o2 = sieve_from_ii(n)
    assert p1 == p2, f"different primes at n={n}"
    print(f"  {n:>10} {o1:>12,} {o2:>12,} {(1 - o2 / o1) * 100:>7.0f}%")
print("\n  -> Identical prime lists. Multiples below i*i already had a")
print("     SMALLER prime factor, so they were marked earlier.")

print("\n  Sieve vs testing each number individually:")
print(f"  {'n':>10} {'primes':>9} {'sieve':>11} {'per-number test':>17} {'speedup':>9}")
print("  " + "-" * 60)
for n in [1000, 10_000, 100_000]:
    start = time.perf_counter()
    s = sieve(n)
    t_sieve = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    t_list = [i for i in range(2, n + 1) if is_prime_6k(i)[0]]
    t_each = (time.perf_counter() - start) * 1000
    assert s == t_list, f"mismatch at n={n}"
    print(f"  {n:>10} {len(s):>9,} {t_sieve:>9.1f}ms {t_each:>15.1f}ms "
          f"{t_each / t_sieve:>8.1f}x")
print("\n  -> Same primes. The sieve wins because it never TESTS anything --")
print("     it just crosses out multiples. O(n log log n) is nearly linear.")

print("\n  Verifying the sieve against per-number primality testing:")
fails = 0
for n in [0, 1, 2, 3, 10, 100, 500, 1000]:
    if sieve(n) != [i for i in range(2, n + 1) if is_prime_6k(i)[0]]:
        fails += 1
print(f"    8 sizes including edge cases (0, 1, 2), mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")
print(f"    Known: 25 primes below 100 -> got {len(sieve(100))}")
print(f"    Known: 168 primes below 1000 -> got {len(sieve(1000))}")
print(f"    Known: 78498 primes below 1e6 -> got {len(sieve(1_000_000)):,}")

# ==================== (3) Factorisation ====================
print("\n[3] Factorisation -- Trial Division vs an SPF Sieve")
print("-" * 70)

def factorise_trial(n: int) -> Dict[int, int]:
    """O(sqrt(n)) for a single number."""
    factors: Dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1   # the remaining prime
    return factors


def spf_sieve(n: int) -> List[int]:
    """spf[i] = smallest prime factor of i. O(n log log n)."""
    spf = list(range(n + 1))
    for i in range(2, math.isqrt(n) + 1):
        if spf[i] == i:                      # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:              # not yet assigned
                    spf[j] = i
    return spf


def factorise_spf(n: int, spf: List[int]) -> Dict[int, int]:
    """O(log n) with a precomputed table."""
    factors: Dict[int, int] = {}
    while n > 1:
        p = spf[n]
        factors[p] = factors.get(p, 0) + 1
        n //= p
    return factors


print(f"  {'n':>8}  factorisation")
print("  " + "-" * 40)
for n in [12, 60, 97, 1024, 9973, 123456]:
    f = factorise_trial(n)
    expr = " * ".join(f"{p}^{e}" if e > 1 else str(p)
                      for p, e in sorted(f.items()))
    print(f"  {n:>8}  {expr}")

LIMIT = 200_000
print(f"\n  Building an SPF table up to {LIMIT:,}...")
start = time.perf_counter()
spf = spf_sieve(LIMIT)
build_ms = (time.perf_counter() - start) * 1000
print(f"    built in {build_ms:.0f}ms")

random.seed(1)
nums = [random.randint(2, LIMIT) for _ in range(20_000)]

start = time.perf_counter()
r_trial = [factorise_trial(x) for x in nums]
trial_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
r_spf = [factorise_spf(x, spf) for x in nums]
spf_ms = (time.perf_counter() - start) * 1000

print(f"\n  Factorising 20,000 numbers:")
print(f"    Trial division O(sqrt(n)) each : {trial_ms:>8.0f}ms")
print(f"    SPF table O(log n) each        : {spf_ms:>8.0f}ms  "
      f"(+{build_ms:.0f}ms build)")
print(f"    Results identical              : {r_trial == r_spf}")
total_spf = spf_ms + build_ms
print(f"    Including the build            : {total_spf:>8.0f}ms  "
      f"-> {trial_ms / total_spf:.1f}x faster overall")
print("    -> Build the table once when factorising MANY numbers in range.")
print("       For a single number, trial division needs no setup.")

print("\n  Verifying both against a product check:")
fails = 0
for _ in range(5000):
    n = random.randint(2, LIMIT)
    f1 = factorise_trial(n)
    f2 = factorise_spf(n, spf)
    prod = 1
    for p, e in f1.items():
        prod *= p ** e
    all_prime = all(is_prime_6k(p)[0] for p in f1)
    if f1 != f2 or prod != n or not all_prime:
        fails += 1
print(f"    5,000 numbers -- factors multiply back AND all are prime: "
      f"{'PASS' if not fails else 'FAIL'} ({fails} failures)")

# ==================== (4) GCD and LCM ====================
print("\n[4] GCD and LCM -- Euclid in Four Lines")
print("-" * 70)

def gcd_euclid(a: int, b: int) -> Tuple[int, int]:
    """Returns (gcd, steps). O(log min(a,b))."""
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return a, steps


def gcd_subtract(a: int, b: int) -> Tuple[int, int]:
    """The slow ancestor: repeated subtraction. O(max(a,b)/gcd)."""
    steps = 0
    while a != b and a > 0 and b > 0:
        steps += 1
        if a > b:
            a -= b
        else:
            b -= a
    return a, steps


def gcd_brute(a: int, b: int) -> int:
    """Reference: check every candidate downward."""
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    for d in range(min(abs(a), abs(b)), 0, -1):
        if a % d == 0 and b % d == 0:
            return d
    return 1


def lcm(a: int, b: int) -> int:
    """Divide BEFORE multiplying to keep intermediates small."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd_euclid(abs(a), abs(b))[0] * abs(b)


print(f"  {'a':>10} {'b':>10} {'gcd':>7} {'Euclid steps':>14} {'subtract steps':>16}")
print("  " + "-" * 62)
for a, b in [(48, 18), (1071, 462), (100, 3), (98765, 12345), (610, 377)]:
    g, s1 = gcd_euclid(a, b)
    _, s2 = gcd_subtract(a, b)
    assert g == gcd_brute(a, b) == math.gcd(a, b)
    print(f"  {a:>10} {b:>10} {g:>7} {s1:>14} {s2:>16,}")

print("\n  -> (610, 377) are consecutive Fibonacci numbers: that is Euclid's")
print("     WORST case, and it still took only a handful of steps.")
print("  -> Repeated subtraction is correct but can take thousands of steps")
print("     for the same answer. `a % b` does all those subtractions at once.")

print(f"\n  Euclid's O(log n) bound, empirically:")
print(f"  {'magnitude':>18} {'max steps seen':>16} {'log2(n)':>10}")
print("  " + "-" * 48)
random.seed(3)
for mag in [10**3, 10**6, 10**9, 10**12]:
    worst = 0
    for _ in range(3000):
        a, b = random.randint(1, mag), random.randint(1, mag)
        worst = max(worst, gcd_euclid(a, b)[1])
    print(f"  {mag:>18,} {worst:>16} {math.log2(mag):>10.1f}")
print("\n  -> Steps grow like log(n), not n. Each step at least halves the")
print("     larger argument.")

print("\n  LCM: divide before multiplying")
print(f"    lcm(12, 18) = {lcm(12, 18)}   (verify: {math.lcm(12, 18)})")
print(f"    lcm(4, 6)   = {lcm(4, 6)}   (verify: {math.lcm(4, 6)})")
print(f"    gcd * lcm == a * b : "
      f"{gcd_euclid(12, 18)[0] * lcm(12, 18) == 12 * 18}")

print("\n  Verifying GCD and LCM against math.gcd / math.lcm and brute force:")
fails = 0
for _ in range(5000):
    a, b = random.randint(0, 500), random.randint(0, 500)
    g = gcd_euclid(a, b)[0] if (a or b) else 0
    if a and b:
        if g != math.gcd(a, b) or g != gcd_brute(a, b):
            fails += 1
        if lcm(a, b) != math.lcm(a, b):
            fails += 1
        if g * lcm(a, b) != a * b:
            fails += 1
print(f"    5,000 pairs -- gcd, lcm, and gcd*lcm==a*b: "
      f"{'PASS' if not fails else 'FAIL'} ({fails} failures)")

# Extended Euclid
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Returns (g, x, y) with a*x + b*y == g."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


print("\n  Extended Euclid -- finds x, y with a*x + b*y = gcd(a, b):")
print(f"  {'a':>6} {'b':>6} {'g':>5} {'x':>7} {'y':>7}  check a*x + b*y == g")
print("  " + "-" * 54)
for a, b in [(48, 18), (240, 46), (17, 5)]:
    g, x, y = extended_gcd(a, b)
    print(f"  {a:>6} {b:>6} {g:>5} {x:>7} {y:>7}  "
          f"{a*x + b*y} == {g} -> {a*x + b*y == g}")

fails = sum(1 for _ in range(5000)
            if (lambda a, b: (lambda r: r[0] != math.gcd(a, b)
                              or a * r[1] + b * r[2] != r[0])(extended_gcd(a, b)))
            (random.randint(1, 1000), random.randint(1, 1000)))
print(f"\n    5,000 pairs, identity a*x+b*y==gcd holds: "
      f"{'PASS' if not fails else 'FAIL'} ({fails} failures)")

# ==================== (5) Fast Exponentiation ====================
print("\n[5] Fast Exponentiation -- The Exponent's Bits Are the Schedule")
print("-" * 70)

def power_naive(a: int, b: int) -> Tuple[int, int]:
    """O(b) multiplications."""
    result = 1
    for _ in range(b):
        result *= a
    return result, b


def power_fast(a: int, b: int, mod: int = 0) -> Tuple[int, int]:
    """O(log b). Square the base, halve the exponent."""
    result = 1
    mults = 0
    base = a % mod if mod else a
    while b > 0:
        if b & 1:                        # this bit is set -> multiply in
            result = result * base
            if mod:
                result %= mod
            mults += 1
        base = base * base               # square
        if mod:
            base %= mod
        mults += 1
        b >>= 1
    return result, mults


print("  a^13 where 13 = 1101 in binary:")
print("    a^13 = a^8 * a^4 * a^1     (bits 3, 2, and 0 are set)")
print("    4 squarings + 3 multiplies, instead of 12 multiplies.\n")

print(f"  {'a':>4} {'b':>7} {'naive mults':>13} {'fast mults':>12} {'result match':>14}")
print("  " + "-" * 56)
for a, b in [(2, 10), (3, 20), (7, 50), (2, 1000)]:
    r1, m1 = power_naive(a, b)
    r2, m2 = power_fast(a, b)
    print(f"  {a:>4} {b:>7} {m1:>13,} {m2:>12} "
          f"{str(r1 == r2 == a ** b):>14}")

print("\n  Modular exponentiation (what 'answer mod 1e9+7' problems need):")
MOD = 10**9 + 7
for a, b in [(2, 100), (3, 1000), (123456789, 987654321)]:
    mine, _ = power_fast(a, b, MOD)
    builtin = pow(a, b, MOD)
    print(f"    {a}^{b} mod {MOD} = {mine}   match pow(): {mine == builtin}")

print("\n  Timing vs Python's built-in three-argument pow:")
A, B = 123456789, 10**6
start = time.perf_counter()
for _ in range(2000):
    power_fast(A, B, MOD)
mine_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for _ in range(2000):
    pow(A, B, MOD)
builtin_ms = (time.perf_counter() - start) * 1000
print(f"    Our loop      : {mine_ms:>8.1f}ms")
print(f"    pow(a, b, m)  : {builtin_ms:>8.1f}ms")
print(f"    -> Built-in is {mine_ms / builtin_ms:.0f}x faster (it is C).")
print(f"       Write the loop to prove you understand it; SHIP pow().")

print("\n  Verifying fast power against the built-in:")
fails = 0
for _ in range(5000):
    a = random.randint(0, 1000)
    b = random.randint(0, 100)
    m = random.choice([0, 97, 1000, MOD])
    mine = power_fast(a, b, m)[0]
    want = pow(a, b, m) if m else a ** b
    if mine != want:
        fails += 1
print(f"    5,000 random (a, b, mod) triples, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# ==================== (6) Modular Arithmetic ====================
print("\n[6] Modular Arithmetic -- and the Division Trap")
print("-" * 70)

print("  The rules:")
print("    (a + b) % m = ((a%m) + (b%m)) % m")
print("    (a - b) % m = ((a%m) - (b%m) + m) % m     <- the +m matters")
print("    (a * b) % m = ((a%m) * (b%m)) % m")
print("    (a / b) % m = (a * inverse(b)) % m        <- NOT (a/b) % m\n")

a, b, m = 987654321, 123456789, 1000
print(f"  a={a}, b={b}, m={m}")
print(f"    (a+b)%m : direct={(a+b)%m}, stepwise={((a%m)+(b%m))%m}  "
      f"match={((a+b)%m) == ((a%m)+(b%m))%m}")
print(f"    (a*b)%m : direct={(a*b)%m}, stepwise={((a%m)*(b%m))%m}  "
      f"match={((a*b)%m) == ((a%m)*(b%m))%m}")
print(f"    (a-b)%m : direct={(a-b)%m}, stepwise={((a%m)-(b%m)+m)%m}  "
      f"match={((a-b)%m) == ((a%m)-(b%m)+m)%m}")

print("\n  Python's % is always non-negative for a positive modulus:")
for x in [-7, -1, 7]:
    print(f"    {x:>3} % 3 = {x % 3:>2}   (C/Java/JS would give "
          f"{int(math.fmod(x, 3)):>2})")
print("    -> Python is friendlier here, but write the +m anyway. The habit")
print("       protects you the moment you switch languages.")

def mod_inverse(a: int, m: int) -> int:
    """Fermat's little theorem. Requires m PRIME."""
    return pow(a, m - 2, m)


def mod_inverse_extgcd(a: int, m: int) -> int:
    """Works for any m coprime to a."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"no inverse: gcd({a}, {m}) = {g}")
    return x % m


print("\n  Modular inverse -- there is no modular division:")
print(f"  {'a':>12} {'m':>12} {'inv (Fermat)':>14} {'a*inv % m':>11}")
print("  " + "-" * 54)
for a in [3, 7, 123456789]:
    inv = mod_inverse(a, MOD)
    print(f"  {a:>12} {MOD:>12} {inv:>14} {a * inv % MOD:>11}")
print("  -> a * inverse(a) == 1 (mod m) in every row. That is the definition.")

print("\n  Both inverse methods agree, and both satisfy a*inv == 1:")
fails = 0
for _ in range(3000):
    a = random.randint(1, 10**6)
    i1 = mod_inverse(a, MOD)
    i2 = mod_inverse_extgcd(a, MOD)
    if i1 != i2 or a * i1 % MOD != 1:
        fails += 1
print(f"    3,000 values, failures: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

print("\n  A worked example -- C(n,k) mod p needs division:")
n, k = 20, 7
num = math.factorial(n) % MOD
den = math.factorial(k) * math.factorial(n - k) % MOD
wrong = (num // den) % MOD if den else 0
right = num * mod_inverse(den, MOD) % MOD
print(f"    C({n},{k}) exactly            = {math.comb(n, k)}")
print(f"    C({n},{k}) mod p, WRONG (//)  = {wrong}")
print(f"    C({n},{k}) mod p, RIGHT (inv) = {right}")
print(f"    exact value mod p            = {math.comb(n, k) % MOD}")
print(f"    -> Integer division after taking a modulus is meaningless.")
print(f"       Multiply by the inverse instead.")

# ==================== (7) Combinatorics ====================
print("\n[7] Combinatorics -- Never Three Factorials")
print("-" * 70)

def comb_factorials(n: int, k: int) -> int:
    """The naive way: builds enormous intermediates."""
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def comb_iterative(n: int, k: int) -> int:
    """O(k) with small intermediates and exact integer division."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)                    # symmetry: C(n,k) == C(n,n-k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def pascal_triangle(rows: int) -> List[List[int]]:
    """All binomials up to row `rows`, with NO division at all."""
    tri = [[1]]
    for r in range(1, rows + 1):
        prev = tri[-1]
        row = [1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1]
        tri.append(row)
    return tri


print("  Pascal's triangle (each entry is the sum of the two above):")
tri = pascal_triangle(6)
width = 4
for r, row in enumerate(tri):
    pad = " " * ((len(tri) - r) * width // 2)
    print(f"    {pad}" + "".join(f"{v:^{width}}" for v in row))

print(f"\n  Row sums are powers of 2:")
for r, row in enumerate(tri):
    print(f"    row {r}: sum = {sum(row):>3}  = 2^{r}  -> {sum(row) == 2 ** r}")

print(f"\n  C(n,k) three ways:")
print(f"  {'n':>5} {'k':>4} {'factorials':>22} {'iterative':>22} {'math.comb':>22}")
print("  " + "-" * 78)
for n, k in [(5, 2), (20, 10), (52, 5), (100, 50)]:
    a = comb_factorials(n, k)
    b = comb_iterative(n, k)
    c = math.comb(n, k)
    astr = str(a) if len(str(a)) <= 20 else str(a)[:17] + "..."
    print(f"  {n:>5} {k:>4} {astr:>22} "
          f"{(str(b) if len(str(b)) <= 20 else str(b)[:17] + '...'):>22} "
          f"{(str(c) if len(str(c)) <= 20 else str(c)[:17] + '...'):>22}")
    assert a == b == c

print(f"\n  Why the symmetry step matters -- C(1000, 998):")
print(f"    without min(k, n-k): 998 iterations")
print(f"    with    min(k, n-k):   2 iterations")
print(f"    result: {comb_iterative(1000, 998)}  "
      f"(verify: {math.comb(1000, 998)})")

print(f"\n  Cost of the factorial approach at scale (n=2000, k=1000):")
start = time.perf_counter()
for _ in range(200):
    comb_factorials(2000, 1000)
fact_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for _ in range(200):
    comb_iterative(2000, 1000)
iter_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for _ in range(200):
    math.comb(2000, 1000)
lib_ms = (time.perf_counter() - start) * 1000
# Count digits via logarithms: log10(n!) = sum of log10(i).
# str(math.factorial(2000)) would raise -- Python 3.11+ caps int->str
# conversion at 4300 digits, and 2000! is far past that. A neat reminder
# that "just print it" is not always available.
digits_2000 = int(sum(math.log10(i) for i in range(1, 2001))) + 1
print(f"    2000! has {digits_2000:,} digits -- that is the intermediate")
print(f"    three factorials : {fact_ms:>8.1f}ms")
print(f"    iterative O(k)   : {iter_ms:>8.1f}ms")
print(f"    math.comb        : {lib_ms:>8.1f}ms")
print(f"    -> math.comb wins clearly. But note the three-factorial version")
print(f"       is competitive with our O(k) loop, because math.factorial is C")
print(f"       and the loop is interpreted big-integer division. The textbook")
print(f"       'never use three factorials' rule assumes YOU wrote factorial.")
print(f"       Write the iterative form to show you understand the")
print(f"       intermediates; ship math.comb.")

print("\n  Verifying against math.comb across a wide range:")
fails = 0
for n in range(0, 40):
    for k in range(-1, n + 2):
        want = math.comb(n, k) if 0 <= k <= n else 0
        if comb_iterative(n, k) != want:
            fails += 1
print(f"    all (n,k) for n<40 including out-of-range k, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# Catalan numbers
def catalan(n: int) -> int:
    return math.comb(2 * n, n) // (n + 1)

print("\n  Catalan numbers -- they count BOTH balanced parentheses AND")
print("  distinct BST shapes (Topic 20). Not a coincidence: both count")
print("  binary tree shapes.")
print(f"    {'n':>3} {'Catalan(n)':>12}")
print("    " + "-" * 18)
for n in range(0, 9):
    print(f"    {n:>3} {catalan(n):>12,}")

# Verify Catalan via the recurrence
def catalan_dp(n: int) -> int:
    c = [0] * (n + 1)
    c[0] = 1
    for i in range(1, n + 1):
        c[i] = sum(c[j] * c[i - 1 - j] for j in range(i))
    return c[n]

fails = sum(1 for n in range(0, 15) if catalan(n) != catalan_dp(n))
print(f"\n    Closed form matches the recurrence for n<15: "
      f"{'PASS' if not fails else 'FAIL'}")

# ==================== (8) Digit Manipulation ====================
print("\n[8] Digit Manipulation -- n % 10 and n // 10 Are Everything")
print("-" * 70)

def digits_of(n: int) -> List[int]:
    """Least significant first."""
    n = abs(n)
    if n == 0:
        return [0]
    out = []
    while n:
        out.append(n % 10)
        n //= 10
    return out


def digit_sum(n: int) -> int:
    total = 0
    n = abs(n)
    while n:
        total += n % 10
        n //= 10
    return total


def reverse_number(n: int) -> int:
    sign = -1 if n < 0 else 1
    n = abs(n)
    rev = 0
    while n:
        rev = rev * 10 + n % 10
        n //= 10
    return sign * rev


def is_palindrome_number(n: int) -> bool:
    if n < 0:
        return False
    return n == reverse_number(n)


def digital_root(n: int) -> int:
    """O(1) closed form. Works because 10 == 1 (mod 9)."""
    if n == 0:
        return 0
    return 1 + (abs(n) - 1) % 9


def digital_root_loop(n: int) -> int:
    """The definition: sum digits until one remains."""
    n = abs(n)
    while n >= 10:
        n = digit_sum(n)
    return n


print(f"  {'n':>10} {'digits':>18} {'sum':>5} {'reversed':>11} {'palin':>7} {'droot':>7}")
print("  " + "-" * 64)
for n in [0, 7, 12321, 98765, -456, 1000000]:
    d = digits_of(n)
    print(f"  {n:>10} {str(d):>18} {digit_sum(n):>5} "
          f"{reverse_number(n):>11} {str(is_palindrome_number(n)):>7} "
          f"{digital_root(n):>7}")

print("\n  Why the digital root has a closed form:")
print("    10 == 1 (mod 9), so every power of 10 is == 1 (mod 9).")
print("    Therefore a number == its digit sum (mod 9).")
print("    That is also why 'casting out nines' works as an arithmetic check.")
print(f"    {'n':>8} {'n % 9':>7} {'digit_sum % 9':>15} {'droot':>7}")
print("    " + "-" * 42)
for n in [12345, 99999, 123456789]:
    print(f"    {n:>8} {n % 9:>7} {digit_sum(n) % 9:>15} {digital_root(n):>7}")

print("\n  Verifying digit helpers against string-based references:")
fails = {"digits": 0, "digit_sum": 0, "reverse": 0, "palindrome": 0,
         "digital_root": 0}
for _ in range(20_000):
    n = random.randint(-10**9, 10**9)
    if digits_of(n) != [int(c) for c in reversed(str(abs(n)))]:
        fails["digits"] += 1
    if digit_sum(n) != sum(int(c) for c in str(abs(n))):
        fails["digit_sum"] += 1
    sgn = -1 if n < 0 else 1
    if reverse_number(n) != sgn * int(str(abs(n))[::-1]):
        fails["reverse"] += 1
    if is_palindrome_number(n) != (n >= 0 and str(n) == str(n)[::-1]):
        fails["palindrome"] += 1
    if digital_root(n) != digital_root_loop(n):
        fails["digital_root"] += 1
print(f"    {'Check':<16} {'Failures':>10}  Verdict")
print("    " + "-" * 38)
for k, v in fails.items():
    print(f"    {k:<16} {v:>10}  {'PASS' if not v else 'FAIL'}")

print("\n  Arithmetic vs string extraction, timed:")
vals = [random.randint(1, 10**12) for _ in range(200_000)]
start = time.perf_counter()
for v in vals:
    digit_sum(v)
arith_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for v in vals:
    sum(int(c) for c in str(v))
str_ms = (time.perf_counter() - start) * 1000
print(f"    arithmetic (% and //) : {arith_ms:>8.0f}ms")
print(f"    str + int per char    : {str_ms:>8.0f}ms")
faster = "arithmetic" if arith_ms < str_ms else "string"
print(f"    -> {faster} is faster here by "
      f"{max(arith_ms, str_ms) / min(arith_ms, str_ms):.1f}x")
print(f"       Arithmetic avoids allocating a string, but str() is C code.")
print(f"       Measure rather than assume; both are O(log n).")

# ==================== (9) Base Conversion ====================
print("\n[9] Base Conversion -- Same % and // Pattern")
print("-" * 70)

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def to_base(n: int, base: int) -> str:
    if not 2 <= base <= 36:
        raise ValueError("base must be 2..36")
    if n == 0:
        return "0"
    neg, n = n < 0, abs(n)
    out = []
    while n:
        out.append(DIGITS[n % base])     # same pattern as digit extraction
        n //= base
    return ("-" if neg else "") + "".join(reversed(out))


def from_base(s: str, base: int) -> int:
    """Horner's method."""
    neg = s.startswith("-")
    body = s.lstrip("-+").upper()
    result = 0
    for ch in body:
        result = result * base + DIGITS.index(ch)
    return -result if neg else result


print(f"  {'n':>8} {'base 2':>16} {'base 8':>10} {'base 16':>9} {'base 36':>9}")
print("  " + "-" * 56)
for n in [0, 10, 255, 4095, 123456]:
    print(f"  {n:>8} {to_base(n, 2):>16} {to_base(n, 8):>10} "
          f"{to_base(n, 16):>9} {to_base(n, 36):>9}")

print("\n  Round-trip and built-in agreement:")
fails = 0
for _ in range(20_000):
    n = random.randint(-10**9, 10**9)
    base = random.randint(2, 36)
    s = to_base(n, base)
    if from_base(s, base) != n:
        fails += 1
    if base == 2 and n >= 0 and s != (bin(n)[2:] if n else "0"):
        fails += 1
    if base == 16 and n >= 0 and s != (hex(n)[2:].upper() if n else "0"):
        fails += 1
    if int(s, base) != n:
        fails += 1
print(f"    20,000 conversions (round-trip + int(s,base) + bin/hex): "
      f"{'PASS' if not fails else 'FAIL'} ({fails} failures)")

# ==================== (10) Overflow and Division Semantics ====================
print("\n[10] Overflow and Division -- Where Python Differs")
print("-" * 70)

INT_MAX = 2**31 - 1
INT_MIN = -2**31

print(f"  Python integers are ARBITRARY PRECISION -- they never overflow.")
print(f"    2^100 = {2**100}")
print(f"    That is a convenience AND an interview trap: when a problem")
print(f"    specifies 32-bit ints, you must SIMULATE the bound.\n")
print(f"    INT_MAX = {INT_MAX:>12}")
print(f"    INT_MIN = {INT_MIN:>12}")

def reverse_integer_32(n: int) -> int:
    """LeetCode-style: return 0 on 32-bit overflow."""
    sign = -1 if n < 0 else 1
    rev, n = 0, abs(n)
    while n:
        rev = rev * 10 + n % 10
        n //= 10
    rev *= sign
    return 0 if rev < INT_MIN or rev > INT_MAX else rev


print(f"\n  {'input':>14} {'reversed':>14} {'32-bit safe':>13}")
print("  " + "-" * 46)
for n in [123, -456, 1534236469, 2147483647, -2147483648, 1000000003]:
    r = reverse_number(n)
    print(f"  {n:>14} {r:>14} {reverse_integer_32(n):>13}")
print("  -> 1534236469 reversed is 9646324351, which exceeds INT_MAX, so a")
print("     32-bit-constrained problem wants 0. Python happily computes the")
print("     big value, which is exactly why you must check deliberately.")

print("\n  Integer division: Python FLOORS, C TRUNCATES toward zero")
print(f"  {'expr':>12} {'Python':>9} {'C-style':>9}  differ?")
print("  " + "-" * 44)
for a, b in [(7, 2), (-7, 2), (7, -2), (-7, -2)]:
    py = a // b
    c = int(a / b)
    print(f"  {f'{a} // {b}':>12} {py:>9} {c:>9}  "
          f"{'YES' if py != c else 'no'}")

print("\n  Modulo follows the same asymmetry:")
print(f"  {'expr':>12} {'Python':>9} {'C-style':>9}  differ?")
print("  " + "-" * 44)
for a, b in [(7, 2), (-7, 2), (7, -2), (-7, -2)]:
    py = a % b
    c = int(math.fmod(a, b))
    print(f"  {f'{a} % {b}':>12} {py:>9} {c:>9}  "
          f"{'YES' if py != c else 'no'}")

print("\n  -> This is a real porting bug. If a problem expects C semantics")
print("     (many division problems do), use int(a/b) or")
print("     abs(a)//abs(b) with an explicit sign.")

def divide_c_style(a: int, b: int) -> int:
    """Truncate toward zero, like C."""
    if b == 0:
        raise ZeroDivisionError
    sign = -1 if (a < 0) != (b < 0) else 1
    return sign * (abs(a) // abs(b))

fails = 0
for _ in range(20_000):
    a = random.randint(-10**6, 10**6)
    b = random.randint(-1000, 1000)
    if b == 0:
        continue
    if divide_c_style(a, b) != int(a / b) and abs(a) < 2**52:
        fails += 1
print(f"\n  C-style division helper vs int(a/b): "
      f"{'PASS' if not fails else 'FAIL'} ({fails} failures)")

# ==================== (11) Verification Summary ====================
print("\n[11] Full Verification Summary")
print("-" * 70)

checks: Dict[str, int] = {}

# primality against a sieve
S = sieve(20_000)
prime_set = set(S)
checks["is_prime vs sieve"] = sum(
    1 for n in range(0, 20_001) if is_prime_6k(n)[0] != (n in prime_set))

# sieve prime counts against known values
known_counts = {10: 4, 100: 25, 1000: 168, 10_000: 1229, 100_000: 9592}
checks["sieve counts vs known"] = sum(
    1 for n, c in known_counts.items() if len(sieve(n)) != c)

# gcd/lcm
checks["gcd vs math.gcd"] = sum(
    1 for _ in range(3000)
    if (lambda a, b: gcd_euclid(a, b)[0] != math.gcd(a, b))
    (random.randint(1, 10**6), random.randint(1, 10**6)))

# fast power
checks["fast power vs pow()"] = sum(
    1 for _ in range(3000)
    if (lambda a, b: power_fast(a, b, MOD)[0] != pow(a, b, MOD))
    (random.randint(0, 10**6), random.randint(0, 10**4)))

# modular inverse
checks["mod inverse identity"] = sum(
    1 for _ in range(3000)
    if (lambda a: a * mod_inverse(a, MOD) % MOD != 1)(random.randint(1, 10**6)))

# combinations
c_fails = 0
for _ in range(3000):
    n = random.randint(0, 60)
    k = random.randint(0, n)
    if comb_iterative(n, k) != math.comb(n, k):
        c_fails += 1
checks["comb vs math.comb"] = c_fails

# Factorisation. NOTE: use is_prime_6k, not `prime_set` -- that set only
# holds primes up to 20,000, so a large prime factor of a 6-digit number
# would look like a failure when the factorisation was perfectly correct.
# An earlier version of this check did exactly that and reported 389 false
# failures. The reference has to cover the same range as the input.
f_fails = 0
for _ in range(3000):
    n = random.randint(2, 100_000)
    f = factorise_trial(n)
    prod = 1
    for p, e in f.items():
        prod *= p ** e
    if prod != n or any(not is_prime_6k(p)[0] for p in f):
        f_fails += 1
checks["factorisation product"] = f_fails

# base conversion
b_fails = 0
for _ in range(3000):
    n = random.randint(-10**9, 10**9)
    base = random.randint(2, 36)
    if from_base(to_base(n, base), base) != n:
        b_fails += 1
checks["base round-trip"] = b_fails

# digits
d_fails = 0
for _ in range(3000):
    n = random.randint(-10**12, 10**12)
    if digit_sum(n) != sum(int(c) for c in str(abs(n))):
        d_fails += 1
    if digital_root(n) != digital_root_loop(n):
        d_fails += 1
checks["digit helpers"] = d_fails

print(f"  {'Check':<28} {'Failures':>10}  Verdict")
print("  " + "-" * 50)
for name, f in checks.items():
    print(f"  {name:<28} {f:>10}  {'PASS' if f == 0 else 'FAIL'}")

print("\n-> Every function cross-checked against the standard library,")
print("   a brute-force reference, or a published constant.")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
