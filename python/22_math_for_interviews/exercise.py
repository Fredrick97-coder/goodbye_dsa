"""
Exercises: Math for Interviews

Primes, GCD/LCM, modular arithmetic, fast exponentiation, combinatorics,
digits, base conversion, and overflow.
"""

from typing import List, Dict, Tuple, Optional

print("=" * 70)
print("EXERCISES: Math for Interviews")
print("=" * 70)
print("""
THE SIX FACTS THIS TOPIC RESTS ON

  1. Divisors come in pairs, so check only up to sqrt(n)
  2. Write `i * i <= n`, never `i <= sqrt(n)` -- integers are exact
  3. gcd(a, b) = gcd(b, a % b), and it is O(log n)
  4. There is no modular division -- multiply by the modular inverse
  5. The exponent's BITS schedule the squarings in fast power
  6. `n % 10` and `n // 10` are all of digit manipulation
""")

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. PRIMALITY TEST")
print("Input: An integer n")
print("Output: True if n is prime")
print("Example: 97 -> True, 91 -> False (7 x 13)")
def is_prime(n: int) -> bool:
    # TODO: Handle n < 2 first. Then loop while i * i <= n.
    # Write `i * i <= n`, NOT `i <= math.sqrt(n)` -- sqrt returns a float
    # and can misjudge the boundary on large n. Use math.isqrt if you want
    # the root itself.
    # Bonus: after handling 2 and 3, step by 6 and test i and i+2. Every
    # prime > 3 has the form 6k +/- 1, which cuts divisions ~3x.
    pass

print("\n2. SIEVE OF ERATOSTHENES")
print("Input: n")
print("Output: All primes <= n")
print("Example: n=30 -> [2,3,5,7,11,13,17,19,23,29]")
def sieve(n: int) -> List[int]:
    # TODO: Boolean array, is_p[0] = is_p[1] = False.
    # Outer loop only to isqrt(n) -- beyond that every composite already
    # has a smaller factor that marked it.
    # Inner loop STARTS AT i*i, not 2*i. Multiples below i*i were marked
    # when processing a smaller prime. Count the marking operations both
    # ways to see the saving.
    # Check against known counts: 25 primes < 100, 168 < 1000, 9592 < 1e5.
    pass

print("\n3. GCD AND LCM")
print("Input: Two integers")
print("Output: Their greatest common divisor and least common multiple")
print("Example: gcd(48,18)=6, lcm(4,6)=12")
def gcd(a: int, b: int) -> int:
    # TODO: while b: a, b = b, a % b. Four lines.
    # Then explain WHY it is O(log min(a,b)): each step at least halves the
    # larger argument. The worst case is consecutive Fibonacci numbers --
    # try gcd(610, 377) and count the steps.
    pass

def lcm(a: int, b: int) -> int:
    # TODO: a // gcd(a,b) * b -- DIVIDE FIRST. a * b // gcd is correct in
    # Python but overflows in fixed-width languages. Build the habit.
    # Handle a == 0 or b == 0.
    pass

print("\n4. FAST EXPONENTIATION")
print("Input: base a, exponent b, optional modulus")
print("Output: a^b, or a^b mod m, in O(log b)")
print("Example: 2^10 = 1024 in 4 multiplications, not 10")
def power(a: int, b: int, mod: int = 0) -> int:
    # TODO: While b > 0: if b & 1, fold the base into the result; then
    # square the base and shift b right.
    # The exponent's binary representation IS the schedule of which
    # squares to multiply in. That is Topic 16 showing up again.
    # Verify against pow(a, b, mod) -- and then note that in real code you
    # should just USE pow(a, b, mod), which is C.
    pass

print("\n5. DIGIT EXTRACTION")
print("Input: An integer")
print("Output: Its digits, digit sum, and reversal -- no strings")
print("Example: 1234 -> [4,3,2,1], sum 10, reversed 4321")
def digits_of(n: int) -> List[int]:
    # TODO: while n: append n % 10; n //= 10. Handle n == 0 (return [0])
    # and negatives (use abs).
    pass

def digit_sum(n: int) -> int:
    # TODO: Same loop, accumulating instead of collecting.
    pass

def reverse_number(n: int) -> int:
    # TODO: rev = rev * 10 + n % 10 each step. Preserve the sign.
    pass

print("\n6. COUNT DIGITS")
print("Input: An integer")
print("Output: How many decimal digits it has")
print("Example: 12345 -> 5, 0 -> 1")
def count_digits(n: int) -> int:
    # TODO: Three ways -- repeated division, len(str(n)), or
    # int(log10(n)) + 1. The logarithm version is O(1) but has float
    # precision traps at exact powers of 10; test 1000 and 999999.
    pass

print("\n7. IS A PALINDROME NUMBER")
print("Input: An integer")
print("Output: True if it reads the same both ways")
print("Example: 12321 -> True, -121 -> False")
def is_palindrome_number(n: int) -> bool:
    # TODO: Do it WITHOUT converting to a string -- that is the actual
    # exercise. Reverse the number arithmetically and compare.
    # Negatives are conventionally not palindromes.
    # Bonus: reverse only HALF the digits to avoid overflow in a
    # fixed-width language.
    pass


# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n8. PRIME FACTORISATION")
print("Input: An integer n")
print("Output: Its prime factors with multiplicities")
print("Example: 60 -> {2:2, 3:1, 5:1}")
def factorise(n: int) -> Dict[int, int]:
    # TODO: Trial division to sqrt(n), dividing out each factor fully.
    # CRITICAL: after the loop, if n > 1 then that remainder is itself
    # prime and must be included. Forgetting it loses the largest factor.
    # Verify by multiplying the factors back AND checking each is prime.
    pass

print("\n9. SMALLEST PRIME FACTOR SIEVE")
print("Input: n")
print("Output: A table giving O(log n) factorisation for any value <= n")
print("Example: build once, then factorise thousands of numbers cheaply")
def spf_sieve(n: int) -> List[int]:
    # TODO: spf[i] starts as i. For each prime i, mark spf[j] = i for
    # multiples j = i*i.. that do not already have a smaller factor
    # assigned. Then factorise by repeatedly dividing by spf[n].
    # Compare total time against trial division for 20,000 numbers,
    # INCLUDING the build cost -- that is the honest comparison.
    pass

print("\n10. MODULAR INVERSE")
print("Input: a and a prime modulus m")
print("Output: x with a*x == 1 (mod m)")
print("Example: needed whenever a problem says 'mod 1e9+7' and divides")
def mod_inverse(a: int, m: int) -> int:
    # TODO: Fermat's little theorem: when m is prime, a^(m-2) == a^-1.
    # So it is pow(a, m - 2, m).
    # Then write the extended-Euclid version, which works for any m
    # coprime to a, and confirm both give the same answer.
    # State the precondition out loud: Fermat needs m PRIME.
    pass

print("\n11. COMBINATIONS C(n, k)")
print("Input: n and k")
print("Output: The binomial coefficient")
print("Example: C(52,5) = 2598960 poker hands")
def comb(n: int, k: int) -> int:
    # TODO: Do NOT compute three factorials. Apply the symmetry
    # k = min(k, n-k) first, then multiply k terms dividing as you go:
    #   result = result * (n - i) // (i + 1)
    # The division is exact at each step in that order.
    # Handle k < 0 and k > n (return 0).
    # C(1000, 998) should take 2 iterations, not 998.
    pass

print("\n12. PASCAL'S TRIANGLE")
print("Input: Number of rows")
print("Output: The triangle")
print("Example: no division needed at all -- just additions")
def pascal_triangle(rows: int) -> List[List[int]]:
    # TODO: Each row starts and ends with 1; interior entries are the sum
    # of the two above. C(n,k) = C(n-1,k-1) + C(n-1,k).
    # Verify that row n sums to 2^n.
    # This is the right approach when you need MANY binomials, or when
    # working modulo a NON-prime (where inverses may not exist).
    pass

print("\n13. C(n, k) MODULO A PRIME")
print("Input: n, k, and a prime modulus")
print("Output: C(n,k) mod p")
print("Example: this is where the division trap actually bites")
def comb_mod(n: int, k: int, p: int) -> int:
    # TODO: Precompute factorials and inverse factorials mod p.
    # C(n,k) = n! * inv(k!) * inv((n-k)!)  (mod p)
    # You CANNOT use // after taking a modulus -- demonstrate the wrong
    # answer alongside the right one so the trap is memorable.
    # Bonus: build the inverse factorial table backwards from
    # inv_fact[n] = pow(fact[n], p-2, p) in O(n) total.
    pass

print("\n14. BASE CONVERSION")
print("Input: A number and a base (2-36), or a string and a base")
print("Output: The converted value")
print("Example: same % and // pattern as digit extraction")
def to_base(n: int, base: int) -> str:
    # TODO: while n: take n % base as a digit, n //= base. Reverse at the
    # end. Handle n == 0 and negatives. Digits beyond 9 use A-Z.
    pass

def from_base(s: str, base: int) -> int:
    # TODO: Horner's method: result = result * base + digit_value.
    # Verify round-trips, and check against int(s, base) and bin()/hex().
    pass

print("\n15. HAPPY NUMBER")
print("Input: An integer")
print("Output: True if repeatedly summing squared digits reaches 1")
print("Example: 19 -> 82 -> 68 -> 100 -> 1, so True")
def is_happy(n: int) -> bool:
    # TODO: The digit loop plus CYCLE DETECTION. Either keep a seen set,
    # or use Floyd's tortoise-and-hare (Topic 07) for O(1) space.
    # Recognising that this is cycle detection in disguise is the point.
    pass

print("\n16. COUNT TRAILING ZEROES IN n!")
print("Input: n")
print("Output: The number of trailing zeroes in n factorial")
print("Example: 25! has 6 trailing zeroes")
def trailing_zeroes(n: int) -> int:
    # TODO: Do NOT compute n!. A trailing zero comes from a factor of 10,
    # i.e. a 2-5 pair, and 5s are scarcer. So count factors of 5:
    #   n//5 + n//25 + n//125 + ...
    # This is a "find the mathematical shortcut" question, and computing
    # the factorial is the wrong answer even when it works.
    pass


# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n17. REVERSE A 32-BIT INTEGER WITH OVERFLOW DETECTION")
print("Input: A signed 32-bit integer")
print("Output: Its digits reversed, or 0 on overflow")
print("Example: 1534236469 -> 0 (reversal exceeds INT_MAX)")
def reverse_integer_32(n: int) -> int:
    # TODO: Python never overflows, so you must SIMULATE the bound:
    #   INT_MAX = 2**31 - 1, INT_MIN = -2**31
    # Reverse, then check the range. Then ALSO write the version that
    # detects overflow BEFORE it happens (check rev > INT_MAX // 10
    # before multiplying) -- that is what you would need in C or Java.
    # Say which you are doing and why.
    pass

print("\n18. DIVIDE TWO INTEGERS WITHOUT / OR %")
print("Input: Dividend and divisor")
print("Output: The quotient, truncated toward zero")
print("Example: use doubling subtraction -- and mind the sign semantics")
def divide(dividend: int, divisor: int) -> int:
    # TODO: Repeatedly subtract the largest doubling of the divisor that
    # still fits (Topic 16's shift-and-subtract). O(log^2 n).
    # THE TRAP: Python's // FLOORS while this problem wants C-style
    # TRUNCATION toward zero. -7 // 2 is -4, but the expected answer is -3.
    # Work with absolute values and apply the sign at the end.
    # Also handle the INT_MIN / -1 overflow case.
    pass

print("\n19. SQRT WITHOUT MATH.SQRT")
print("Input: A non-negative integer")
print("Output: floor(sqrt(n))")
print("Example: 8 -> 2, 16 -> 4")
def my_sqrt(n: int) -> int:
    # TODO: Binary search on the answer (Topic 10). Invariant:
    # find the largest x with x*x <= n. Use x*x, not floats.
    # Then implement Newton's method: x = (x + n//x) // 2, which converges
    # quadratically. Compare iteration counts.
    # Verify both against math.isqrt for every n up to 10,000.
    pass

print("\n20. POW(x, n) WITH A NEGATIVE EXPONENT")
print("Input: A float base and an integer exponent (possibly negative)")
print("Output: x^n")
print("Example: 2.0^-2 = 0.25")
def my_pow(x: float, n: int) -> float:
    # TODO: Fast exponentiation on floats. For n < 0, compute x^|n| and
    # take the reciprocal -- but watch the INT_MIN case where -n overflows
    # in fixed-width languages.
    # Note that float multiplication is not associative, so your result
    # may differ from pow() in the last bits. Compare with a tolerance,
    # not equality, and say why.
    pass

print("\n21. EXCEL COLUMN TITLE <-> NUMBER")
print("Input: A column number, or a title like 'AB'")
print("Output: The other representation")
print("Example: 1->'A', 26->'Z', 27->'AA', 28->'AB'")
def to_column_title(n: int) -> str:
    # TODO: Base-26 conversion, but 1-INDEXED with no zero digit. That
    # off-by-one is the whole difficulty: subtract 1 before each %/// step.
    # Test the boundaries 26 -> 'Z' and 27 -> 'AA' specifically.
    pass

def from_column_title(s: str) -> int:
    # TODO: Horner's method with A=1..Z=26.
    # Verify round-trips for 1..10000.
    pass

print("\n22. FRACTION TO RECURRING DECIMAL")
print("Input: A numerator and denominator")
print("Output: The decimal string, with any repeating part in parentheses")
print("Example: 1/6 -> '0.1(6)', 4/333 -> '0.(012)'")
def fraction_to_decimal(numerator: int, denominator: int) -> str:
    # TODO: Long division by hand. Track each REMAINDER you have seen and
    # the position where it occurred; when a remainder repeats, the cycle
    # started at that position -- insert the parentheses there.
    # Handle sign, exact division, and the numerator == 0 case.
    # This is cycle detection again, now on remainders.
    pass


# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n23. SEGMENTED SIEVE")
print("Input: A range [lo, hi] where hi may be very large")
print("Output: All primes in that range, without a size-hi array")
print("Example: primes in [10^12, 10^12 + 10^6]")
def segmented_sieve(lo: int, hi: int) -> List[int]:
    # TODO: A plain sieve needs O(hi) memory, which is impossible here.
    # Instead sieve the primes up to sqrt(hi), then use them to mark
    # composites within the WINDOW [lo, hi] only. Memory is O(hi - lo).
    # This is the same "bounded memory over a stream" idea as reservoir
    # sampling and k-way merging.
    pass

print("\n24. CHINESE REMAINDER THEOREM")
print("Input: Congruences x == a_i (mod m_i) with pairwise coprime moduli")
print("Output: The unique x modulo the product of the moduli")
print("Example: x==2 (mod 3), x==3 (mod 5), x==2 (mod 7) -> x=23")
def crt(remainders: List[int], moduli: List[int]) -> Optional[int]:
    # TODO: Combine two congruences at a time using extended Euclid.
    # Return None if the moduli are not pairwise coprime (the general
    # form needs a compatibility check).
    # Verify by checking x % m_i == a_i for every i.
    pass

print("\n25. MILLER-RABIN PRIMALITY TEST")
print("Input: A large integer")
print("Output: Whether it is prime, probabilistically (or deterministically)")
print("Example: trial division to sqrt(10^18) is 10^9 operations -- hopeless")
def miller_rabin(n: int, witnesses: Optional[List[int]] = None) -> bool:
    # TODO: Write n-1 = d * 2^r. For each witness a, check whether
    # a^d == 1 or a^(d*2^i) == -1 for some i < r. If not, n is composite.
    # Using the witnesses [2,3,5,7,11,13,17,19,23,29,31,37] makes this
    # DETERMINISTIC for all n < 3.3 * 10^24.
    # Compare timing against trial division on a 15-digit prime.
    pass

print("\n26. COUNT PRIMES IN A RANGE, FAST")
print("Input: n")
print("Output: How many primes are <= n")
print("Example: compare your count against the known 78498 below 10^6")
def count_primes(n: int) -> int:
    # TODO: Start with the plain sieve. Then implement an ODD-ONLY sieve
    # (half the memory) or a bitarray version, and measure both memory
    # and time.
    # Report the actual numbers -- including if the "optimised" version is
    # SLOWER in CPython because of indexing overhead. That result is as
    # useful as a speedup.
    pass

print("\n27. GCD OF AN ARRAY, AND SUBARRAY GCDs")
print("Input: An array of integers")
print("Output: The overall GCD, and the number of distinct subarray GCDs")
print("Example: gcd is associative, which is what makes this tractable")
def array_gcd(nums: List[int]) -> int:
    # TODO: functools.reduce(math.gcd, nums). Note the early exit: once
    # the running gcd hits 1 you can stop.
    pass

def distinct_subarray_gcds(nums: List[int]) -> int:
    # TODO: The naive approach is O(n^2 log n). Better: for each right
    # endpoint, keep the SET of gcds of all subarrays ending there. That
    # set is small (gcds at least halve as they shrink), so this is
    # effectively O(n log(max) log n).
    # Because gcd is associative, a segment tree (Topic 17) also answers
    # arbitrary range-gcd queries -- connect the two.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Math for Interviews Cheat Sheet:

1. Primes:
   Test divisors only up to sqrt(n) -- divisors pair up (d*e = n with
   d <= sqrt(n) <= e), so no divisor below the root means none at all.

   ALWAYS write `i * i <= n`, never `i <= math.sqrt(n)`. Integer
   multiplication is exact; float sqrt is not. Use math.isqrt for the root.

   6k +/- 1: every prime > 3 has that form, because the other residues mod
   6 are divisible by 2 or 3. Step by 6, test i and i+2. ~3x fewer
   divisions.

   SIEVE when you need many primes, trial division for one.
     outer loop stops at sqrt(n)  -- larger composites already marked
     inner loop STARTS at i*i     -- smaller multiples had smaller factors
   O(n log log n), because the sum of prime reciprocals grows like
   log log n. Nearly linear.

   Known counts to check against: 25 primes < 100, 168 < 1000,
   1229 < 10^4, 9592 < 10^5, 78498 < 10^6.

2. Factorisation:
   Single number  -> trial division, O(sqrt(n))
   Many numbers   -> SPF sieve once, then O(log n) each
   After the loop, ANY remainder > 1 is itself prime -- include it.

3. GCD and LCM:
   gcd(a, b) = gcd(b, a % b). Four lines, O(log min(a,b)) because each
   step at least halves the larger argument. Worst case is consecutive
   Fibonacci numbers -- and even then it is only ~log2(n) steps, which you
   can measure.

   lcm = a // gcd(a,b) * b -- DIVIDE FIRST. Correct either way in Python;
   the habit prevents overflow elsewhere.

   Extended Euclid gives x, y with a*x + b*y = gcd(a,b), which is how you
   get modular inverses for non-prime moduli.

4. Modular Arithmetic:
     (a + b) % m = ((a%m) + (b%m)) % m
     (a - b) % m = ((a%m) - (b%m) + m) % m      <- the +m matters
     (a * b) % m = ((a%m) * (b%m)) % m
     (a / b) % m = (a * inverse(b)) % m         <- NO modular division

   1e9+7 is the usual modulus because it is PRIME and fits in 32 bits.
   Prime m means Fermat applies: inverse(a) = pow(a, m-2, m).

   Python's % is always non-negative for positive m (-7 % 3 == 2), unlike
   C/Java/JS. Write the +m anyway.

5. Fast Exponentiation:
   O(log b) instead of O(b). The exponent's BITS are the schedule:
     a^13, 13 = 1101 -> a^8 * a^4 * a^1
   Same bit-testing idea as Topic 16. In real code use pow(a, b, mod) --
   it is C and roughly an order of magnitude faster than a Python loop.

6. Combinatorics:
     C(n,k) = n! / (k!(n-k)!)     unordered
     P(n,k) = n! / (n-k)!         ordered

   NEVER three factorials. Apply k = min(k, n-k), then multiply k terms
   dividing as you go. C(1000,998) becomes 2 iterations instead of 998.
   In production: math.comb.

   Pascal's triangle gives all binomials in O(n^2) with NO division --
   the right tool when the modulus is not prime.

   Counting facts:
     subsets of n              2^n
     permutations of n         n!
     with repeats              n!/(n1! n2! ...)
     k-subsets                 C(n,k)
     balanced parens, n pairs  Catalan(n) = C(2n,n)/(n+1)
     distinct BST shapes       Catalan(n)   <- same count, same reason

7. Digits:
   `n % 10` gives the last digit, `n // 10` removes it. That pair is the
   entire technique -- for digit sums, reversal, palindromes, and base
   conversion (where 10 becomes `base`).

   Digital root has a CLOSED FORM: 1 + (n-1) % 9, because 10 == 1 (mod 9)
   so every power of 10 is == 1 and n == digit_sum(n) (mod 9). That is
   also why "casting out nines" works.

8. Overflow and Division Semantics:
   Python ints are arbitrary precision and NEVER overflow. That is a trap:
   when a problem specifies 32-bit ints you must simulate the bound
   deliberately.
     INT_MAX = 2**31 - 1 = 2147483647
     INT_MIN = -2**31    = -2147483648

   Python FLOORS, C TRUNCATES toward zero:
      7 // 2 ==  3        7 % -2 == -1
     -7 // 2 == -4       (C gives -3 and 1)
   A real porting bug. For C semantics use int(a/b), or
   sign * (abs(a) // abs(b)).

   Python 3.11+ also refuses int->str conversion beyond 4300 digits, so
   `len(str(math.factorial(2000)))` RAISES. Count digits with logarithms
   instead: int(sum(log10(i) for i in 1..n)) + 1.

Complexity Reference:

Operation                    Time              Note
──────────────────────────────────────────────────────────────────
Primality test               O(sqrt(n))        6k+/-1 cuts constant ~3x
Sieve of Eratosthenes        O(n log log n)    nearly linear
SPF sieve build              O(n log log n)    then O(log n) per factorise
Trial-division factorise     O(sqrt(n))        fine for one number
GCD (Euclid)                 O(log min(a,b))   worst case Fibonacci pair
LCM                          O(log min(a,b))   via GCD
Extended GCD                 O(log min(a,b))   gives modular inverse
Fast power                   O(log b)          vs O(b) naive
Modular inverse (prime m)    O(log m)          pow(a, m-2, m)
C(n,k) iterative             O(k)              with min(k, n-k)
Pascal to row n              O(n^2)            all binomials, no division
Digit extraction             O(log n)          one pass
Digital root                 O(1)              closed form
Base conversion              O(log n)          per direction
Miller-Rabin                 O(k log^3 n)      deterministic with fixed
                                               witnesses below 3.3e24

Standard Library You Should Name:

  math.gcd(a, b)          math.lcm(a, b)        [3.9+]
  math.isqrt(n)           exact integer sqrt, no float error
  math.comb(n, k)         math.perm(n, k)       [3.8+]
  math.factorial(n)
  pow(a, b, mod)          three-argument, C-implemented
  divmod(a, b)            quotient and remainder in one call
  int(s, base)            parse any base 2-36
  bin() / oct() / hex()

  Reinventing these in production is a small red flag. Writing them in an
  interview to show you understand them is fine -- say which you are doing.

Problem Recognition Guide:

"is n prime"                        -> sqrt bound, or Miller-Rabin if huge
"all primes up to n"                -> sieve
"factorise many numbers"            -> SPF sieve
"simplify a fraction"               -> divide both by gcd
"cycle length / repeating decimal"  -> track remainders (cycle detection)
"answer modulo 1e9+7"               -> modular arithmetic, and it is PRIME
"... and the answer involves /"     -> modular inverse, NOT //
"a^b for huge b"                    -> fast power / pow(a,b,m)
"how many ways to choose"           -> C(n,k), iteratively
"count arrangements with repeats"   -> multinomial
"trailing zeroes of n!"             -> count factors of 5, never compute n!
"sum/reverse the digits"            -> % 10 and // 10
"32-bit overflow"                   -> simulate it; Python will not help
"convert to base k"                 -> % k and // k
"largest x with x*x <= n"           -> binary search or Newton

Common Pitfalls:

1. `i <= math.sqrt(n)` instead of `i * i <= n`.
2. Sieve inner loop from 2*i instead of i*i (correct but wasteful).
3. Forgetting is_p[0] = is_p[1] = False.
4. Losing the final prime factor when the remainder exceeds 1.
5. Computing C(n,k) via three factorials.
6. Skipping k = min(k, n-k).
7. Using // after taking a modulus. There is no modular division.
8. Negative results from modular subtraction (add m first).
9. Assuming Python's // and % match C's for negatives.
10. Ignoring a stated 32-bit constraint because Python cannot overflow.
11. Computing n! to count its trailing zeroes.
12. str(huge_int) raising in Python 3.11+ past 4300 digits.
13. Reinventing math.gcd / math.comb / pow(a,b,m).
14. Edge cases: n<2 in is_prime, n==0 in digits, k>n in comb, b==0 in gcd.

Interview Tips:

1. SAY "divisors come in pairs, so sqrt(n) suffices" -- do not just write
   the loop. The reasoning is what is being assessed.
2. Justify the sieve's i*i start. It distinguishes understanding from
   memorisation.
3. When you see "mod 1e9+7", note out loud that it is PRIME, so Fermat
   gives you inverses cheaply.
4. When a problem says 32-bit, say that Python will not overflow and that
   you are simulating the bound on purpose.
5. Name the stdlib function even if you then implement it by hand.
6. For counting problems, state the formula before coding it.
7. For trailing zeroes, resist computing the factorial. Interviewers use
   that problem specifically to see whether you look for the shortcut.

Learning Progression:

1. Basic: sqrt primality, sieve, Euclid, digit extraction
2. Intermediate: factorisation, fast power, C(n,k) iteratively, base
   conversion, trailing zeroes
3. Advanced: modular inverses, C(n,k) mod p, overflow simulation, C-style
   division, recurring decimals
4. Expert: segmented sieve, Chinese Remainder Theorem, Miller-Rabin, and
   subarray-gcd structures

Next: implement each stub, then run project.py to see this maths running a
crypto toolkit, a hash-ring balancer, a probability calculator, and a
number-theory explorer.
""")
