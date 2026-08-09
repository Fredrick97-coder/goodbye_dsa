# Math for Interviews - The Number Theory You Actually Need

Master primes and sieves, GCD/LCM, modular arithmetic, fast exponentiation,
combinatorics, digit manipulation, and overflow — the maths that shows up in
coding interviews and nowhere else in this curriculum.

---

## 1. Why This Topic Exists

Most interview maths is not hard maths. It's a small set of techniques that
turn an O(n) or O(n²) loop into O(log n) or O(1). The gap is almost always
one of: *"I didn't know that was a known trick."*

| Naive | Better | Technique |
|-------|--------|-----------|
| test divisibility to n | test to √n | primality bound |
| test each number for primality | mark multiples | sieve |
| subtract repeatedly | Euclid | GCD |
| multiply b times | square and halve | fast exponentiation |
| compute n! then divide | multiply k terms | combinations |
| build a string and reverse | `n % 10`, `n // 10` | digit extraction |

None of these are deep. All of them are expected.

---

## 2. Primes and the √n Bound

**Primality testing.** You only need to check divisors up to √n, because
divisors come in pairs: if `d × e = n` and `d ≤ e`, then `d ≤ √n`.

```python
def is_prime(n):
    """O(sqrt(n))"""
    if n < 2:
        return False
    if n < 4:
        return True                 # 2 and 3
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:               # i*i, not i <= sqrt(n) -- no float error
        if n % i == 0:
            return False
        i += 2                      # skip evens
    return True
```

Write `i * i <= n`, not `i <= math.sqrt(n)`. Integer multiplication is exact;
`sqrt` returns a float and can misjudge the boundary on large values.

### The 6k ± 1 Optimisation

Every prime greater than 3 is of the form 6k ± 1 (all other residues mod 6
are divisible by 2 or 3). That lets you step by 6 and test two candidates:

```python
def is_prime_fast(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

Roughly a 3× reduction in divisions versus stepping by 2.

### Sieve of Eratosthenes

To find **all** primes up to n, don't test each one — mark the multiples.

```python
def sieve(n):
    """All primes <= n. O(n log log n) time, O(n) space."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            # Start at i*i: smaller multiples already have a smaller factor
            for j in range(i * i, n + 1, i):
                is_p[j] = False

    return [i for i, p in enumerate(is_p) if p]
```

Two details that matter:
- **Outer loop stops at √n.** Beyond that, every composite has already been
  marked by a smaller factor.
- **Inner loop starts at `i * i`.** Multiples below that (`2i`, `3i`, …) were
  marked when processing 2, 3, … already.

**Why O(n log log n)?** The work is `n/2 + n/3 + n/5 + n/7 + …` over primes,
and the sum of prime reciprocals up to n grows like `log log n`. It is
*nearly linear* in practice.

### Smallest Prime Factor Sieve

A variant that gives O(log n) factorisation for any number in range:

```python
def spf_sieve(n):
    """spf[i] = smallest prime factor of i."""
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:                     # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:             # not yet assigned
                    spf[j] = i
    return spf

def factorise(n, spf):
    """O(log n) using a precomputed SPF table."""
    factors = {}
    while n > 1:
        p = spf[n]
        factors[p] = factors.get(p, 0) + 1
        n //= p
    return factors
```

Build the table once, then factorise any number in range in O(log n) instead
of O(√n). Worth it when you factorise many numbers.

---

## 3. GCD and LCM

**Euclid's algorithm**: `gcd(a, b) = gcd(b, a mod b)`, until `b` is zero.

```python
def gcd(a, b):
    """O(log min(a, b))"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Divide BEFORE multiplying to limit intermediate size."""
    return a // gcd(a, b) * b
```

**Why it's O(log n)**: each step at least halves the larger argument (a
Fibonacci-adjacent bound). The worst case is consecutive Fibonacci numbers.

`lcm(a, b) = a * b // gcd(a, b)` is correct but `a // gcd * b` is better in
languages with fixed-width integers — it avoids an intermediate overflow.
Python has arbitrary precision, so it's stylistic here, but the habit
transfers.

### Extended Euclid

Finds `x, y` such that `ax + by = gcd(a, b)` — the basis of modular inverses.

```python
def extended_gcd(a, b):
    """Returns (g, x, y) with a*x + b*y == g == gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
```

### Standard Library

```python
import math
math.gcd(a, b)          # C-implemented, use this
math.lcm(a, b)          # Python 3.9+
math.isqrt(n)           # exact integer sqrt, no float error
math.comb(n, k)         # exact binomial coefficient
math.perm(n, k)
math.factorial(n)
```

Know these exist. Writing your own `gcd` in production when `math.gcd` is
right there is a small red flag.

---

## 4. Modular Arithmetic

Interview problems say "return the answer modulo 10⁹ + 7" constantly. That
modulus is chosen because it's prime and fits in 32 bits.

### The Rules

```
(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a - b) mod m = ((a mod m) - (b mod m) + m) mod m      <- the +m matters
(a * b) mod m = ((a mod m) * (b mod m)) mod m
(a / b) mod m = (a * inverse(b)) mod m                 <- NOT a/b mod m
```

**Division is the trap.** There is no modular division; you multiply by the
modular *inverse*. And subtraction needs `+ m` before the final `%` in
languages where `%` can return a negative result.

**Python's `%` is always non-negative for a positive modulus** — `-7 % 3 == 2`,
not `-1`. That's friendlier than C/Java/JS, but write the `+ m` anyway; the
habit protects you when you switch languages.

### Modular Inverse

When `m` is prime, Fermat's little theorem gives `a^(m-1) ≡ 1 (mod m)`, so:

```python
def mod_inverse(a, m):
    """Only valid when m is PRIME and a is not a multiple of m."""
    return pow(a, m - 2, m)
```

For non-prime moduli, use extended Euclid (the inverse exists only when
`gcd(a, m) == 1`).

---

## 5. Fast Exponentiation

Computing `a^b` by multiplying b times is O(b). Squaring is O(log b).

```python
def power(a, b, mod=None):
    """O(log b) multiplications."""
    result = 1
    a = a % mod if mod else a
    while b > 0:
        if b & 1:                   # odd exponent -> take one factor out
            result = result * a
            if mod:
                result %= mod
        a = a * a                   # square the base
        if mod:
            a %= mod
        b >>= 1                     # halve the exponent
    return result
```

The bit test `b & 1` and shift `b >>= 1` are Topic 16 again: the exponent's
binary representation *is* the schedule of which squares to multiply in.

```
a^13, 13 = 1101 in binary

a^13 = a^8 * a^4 * a^1
       ^     ^     ^
       bits 3, 2, 0 are set

4 squarings + 3 multiplications, instead of 12 multiplications.
```

**Python has this built in**: `pow(a, b, mod)` is C-implemented and handles
the modulus. Use it. But be able to write the loop — it's a common ask.

---

## 6. Combinatorics

### Factorials and Binomials

```
n!            = n × (n-1) × … × 1        (0! = 1)
P(n, k)       = n! / (n-k)!              ordered selections
C(n, k)       = n! / (k! (n-k)!)         unordered selections
```

**Never compute `C(n, k)` by evaluating three factorials.** Multiply k terms
and divide as you go:

```python
def comb(n, k):
    """O(k), no huge intermediates."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)               # symmetry: C(n,k) == C(n,n-k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result
```

The `k = min(k, n - k)` step matters: `C(1000, 998)` becomes `C(1000, 2)`,
which is 2 iterations instead of 998.

The division is exact at each step (the running product is always divisible),
so integer division is safe here — but only in this order.

### Pascal's Triangle

```
row 0:            1
row 1:          1   1
row 2:        1   2   1
row 3:      1   3   3   1
row 4:    1   4   6   4   1

C(n, k) = C(n-1, k-1) + C(n-1, k)
```

Row n contains the coefficients of `(x + y)^n`, and sums to 2ⁿ. Building the
triangle gives you all binomials up to n in O(n²) with no division at all —
useful when you need many of them, or when working modulo a non-prime.

### Counting Facts Worth Knowing

| Question | Count |
|----------|-------|
| Subsets of n items | 2ⁿ |
| Permutations of n items | n! |
| Permutations with repeats | n! / (n₁! n₂! …) |
| k-subsets of n | C(n, k) |
| Arrangements of k from n | P(n, k) = n!/(n−k)! |
| Ways to place n non-attacking rooks | n! |
| Balanced parenthesis strings, n pairs | Catalan(n) = C(2n,n)/(n+1) |
| Distinct BST shapes with n nodes | Catalan(n) |

Catalan numbers appearing in *both* the parenthesis and BST problems (Topic
20) is not a coincidence — both count binary tree shapes.

---

## 7. Digit Manipulation

Extract digits with arithmetic, not strings.

```python
def digits(n):
    """Least significant first."""
    n = abs(n)
    if n == 0:
        return [0]
    out = []
    while n:
        out.append(n % 10)          # last digit
        n //= 10                    # drop it
    return out

def digit_sum(n):
    total = 0
    n = abs(n)
    while n:
        total += n % 10
        n //= 10
    return total

def reverse_number(n):
    sign = -1 if n < 0 else 1
    n = abs(n)
    rev = 0
    while n:
        rev = rev * 10 + n % 10
        n //= 10
    return sign * rev

def count_digits(n):
    """O(1) via logarithm, or O(log n) by division."""
    return len(str(abs(n))) if n else 1
```

`n % 10` gives the last digit, `n // 10` removes it. That pair is the whole
technique.

### Digital Root

Repeatedly summing digits until one remains has a closed form:

```python
def digital_root(n):
    """O(1). Follows from 10 ≡ 1 (mod 9)."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9
```

Because `10 ≡ 1 (mod 9)`, every power of 10 is ≡ 1, so a number is congruent
to its digit sum mod 9. That's also why "casting out nines" works as an
arithmetic check.

---

## 8. Overflow (and Why Python Is Different)

**Python integers are arbitrary precision.** They never overflow. This is a
genuine convenience *and* an interview trap: problems often specify 32-bit
behaviour, and you must simulate it.

```python
INT_MAX = 2**31 - 1        #  2147483647
INT_MIN = -2**31           # -2147483648

def clamp_32(n):
    return max(INT_MIN, min(INT_MAX, n))

def reverse_integer_32(n):
    """LeetCode-style: return 0 on 32-bit overflow."""
    sign = -1 if n < 0 else 1
    rev = 0
    n = abs(n)
    while n:
        rev = rev * 10 + n % 10
        n //= 10
    rev *= sign
    return 0 if rev < INT_MIN or rev > INT_MAX else rev
```

In C or Java you'd have to detect overflow *before* it happens (check
`rev > INT_MAX // 10` before multiplying). In Python you can check after.
Say which you're doing and why — it shows you know the difference.

### Integer Division and Negative Numbers

Python's `//` floors; C truncates toward zero.

```python
 7 //  2 ==  3        7 /  2 in C ==  3
-7 //  2 == -4       -7 /  2 in C == -3      <- DIFFERENT
 7 % -2  == -1        7 % -2 in C ==  1      <- DIFFERENT
```

For C-style truncation in Python: `int(a / b)` (watch float precision) or
`abs(a) // abs(b) * sign`. This asymmetry causes real bugs when porting.

---

## 9. Base Conversion

```python
def to_base(n, base):
    """Digits most-significant-first."""
    if n == 0:
        return "0"
    digits_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = []
    neg = n < 0
    n = abs(n)
    while n:
        out.append(digits_map[n % base])
        n //= base
    return ("-" if neg else "") + "".join(reversed(out))

def from_base(s, base):
    """Horner's method."""
    result = 0
    for ch in s.upper().lstrip("-"):
        result = result * base + int(ch, 36)
    return -result if s.startswith("-") else result
```

Same `% base` / `// base` pattern as digit extraction — base 10 is just the
special case. Python's built-ins: `bin()`, `oct()`, `hex()`, and
`int(s, base)`.

---

## 10. Complexity Summary

| Operation | Time | Note |
|-----------|------|------|
| Primality test | O(√n) | 6k±1 cuts the constant ~3× |
| Sieve of Eratosthenes | O(n log log n) | nearly linear |
| SPF sieve build | O(n log log n) | then O(log n) per factorisation |
| Trial-division factorise | O(√n) | fine for one number |
| GCD (Euclid) | O(log min(a,b)) | worst case: Fibonacci pair |
| LCM | O(log min(a,b)) | via GCD |
| Extended GCD | O(log min(a,b)) | gives modular inverse |
| Fast power | O(log b) | vs O(b) naive |
| Modular inverse (prime m) | O(log m) | `pow(a, m-2, m)` |
| C(n, k) iterative | O(k) | use `min(k, n-k)` |
| Pascal's triangle to row n | O(n²) | all binomials, no division |
| Digit extraction | O(log n) | one pass |
| Digital root | **O(1)** | closed form |
| Base conversion | O(log n) | per direction |

---

## 11. Common Pitfalls

1. **`i <= math.sqrt(n)` instead of `i * i <= n`.** Float rounding can
   misjudge the boundary on large n. Use `math.isqrt` if you want the root.
2. **Sieve inner loop starting at `2 * i`** instead of `i * i` — correct but
   does redundant work.
3. **Forgetting `is_p[0] = is_p[1] = False`.** 0 and 1 are not prime.
4. **Computing `C(n, k)` via three factorials.** `C(100, 50)` builds a
   158-digit intermediate for no reason.
5. **Not applying `k = min(k, n - k)`.** Turns O(k) into O(n − k) needlessly.
6. **Modular division.** `(a / b) % m` is meaningless; use `a * pow(b, m-2, m) % m`,
   and only when m is prime.
7. **Negative results from subtraction under a modulus.** Add m before the
   final `%`. Python is forgiving; other languages are not.
8. **Assuming Python's `%` and `//` match C's** for negative operands. They
   don't — `-7 // 2` is `-4`, not `-3`.
9. **Ignoring a stated 32-bit constraint** because Python won't overflow. The
   problem is testing whether you noticed.
10. **`0` and `1` in `is_prime`, `n == 0` in `digits`, `k == 0` in `comb`.**
    Edge cases in every one of these functions.
11. **Reinventing `math.gcd`, `math.comb`, or `pow(a,b,m)`.** Know the stdlib.
12. **Sieving to n when you need the nth prime.** You need an upper bound
    estimate first (`n log n` is a usable one).

---

## 12. Key Takeaways

✅ **Check divisors to √n** — divisors pair up, so one must be ≤ √n
✅ **Write `i * i <= n`**, never `i <= sqrt(n)` — integers are exact
✅ **Sieve when you need many primes**, trial division for one
✅ **Sieve inner loop starts at `i * i`**; outer loop stops at √n
✅ **Euclid's GCD is O(log n)** — each step at least halves the larger value
✅ **`lcm = a // gcd * b`** — divide before multiplying
✅ **No modular division** — multiply by `pow(b, m-2, m)` when m is prime
✅ **Add m before `%`** on subtraction, as a portable habit
✅ **Fast power is O(log b)** — the exponent's bits schedule the squarings
✅ **`C(n,k)` iteratively with `min(k, n-k)`** — never three factorials
✅ **Catalan numbers** count parenthesis strings *and* BST shapes
✅ **`n % 10` and `n // 10`** are all of digit manipulation
✅ **Digital root is O(1)** because `10 ≡ 1 (mod 9)`
✅ **Python never overflows** — which means you must *simulate* 32-bit limits
✅ **Python's `//` floors, C truncates** — a real porting bug

**Interview Focus**:
- Say "divisors come in pairs, so I only need √n" rather than just writing it.
- Justify the sieve's `i * i` start — it shows you understand the algorithm
  rather than having memorised it.
- Mention `math.gcd`, `math.comb`, and three-argument `pow` — knowing the
  stdlib is part of the job.
- When a problem says "modulo 10⁹+7", note that it's prime, so Fermat gives
  you inverses.
- When a problem specifies 32-bit ints, say out loud that Python won't
  overflow and that you're simulating the bound deliberately.
- For anything counting arrangements, name the formula before coding it.

Next: implement the sieve, Euclid, fast power, and combinations — then verify
every one against brute force and the standard library!
