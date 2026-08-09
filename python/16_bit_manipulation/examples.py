"""
Examples: Bit Manipulation

Demonstrate bitwise operators, bit tricks, XOR patterns, and bitmask DP.
"""

import time
from typing import List, Tuple

print("=" * 70)
print("BIT MANIPULATION")
print("=" * 70)

# ==================== (1) The Six Operators ====================
print("\n[1] The Six Bitwise Operators")
print("-" * 70)

a, b = 10, 6  # 1010, 0110

print(f"a = {a:>3}  ->  {a:08b}")
print(f"b = {b:>3}  ->  {b:08b}")
print()
print(f"a & b  = {a & b:>3}  ->  {a & b:08b}   (AND: 1 if both)")
print(f"a | b  = {a | b:>3}  ->  {a | b:08b}   (OR:  1 if either)")
print(f"a ^ b  = {a ^ b:>3}  ->  {a ^ b:08b}   (XOR: 1 if different)")
print(f"~a     = {~a:>3}  ->  two's complement (-a - 1)")
print(f"a << 1 = {a << 1:>3}  ->  {a << 1:08b}   (x2)")
print(f"a >> 1 = {a >> 1:>3}  ->  {a >> 1:08b}   (//2)")

print("\n-> All O(1): single CPU instructions")

# ==================== (2) Core Bit Operations ====================
print("\n[2] Core Bit Operations (get / set / clear / toggle)")
print("-" * 70)

def get_bit(n: int, i: int) -> int:
    """Return bit i of n (0 or 1)"""
    return (n >> i) & 1

def set_bit(n: int, i: int) -> int:
    """Turn bit i on"""
    return n | (1 << i)

def clear_bit(n: int, i: int) -> int:
    """Turn bit i off"""
    return n & ~(1 << i)

def toggle_bit(n: int, i: int) -> int:
    """Flip bit i"""
    return n ^ (1 << i)

def update_bit(n: int, i: int, value: int) -> int:
    """Set bit i to value (0 or 1)"""
    return (n & ~(1 << i)) | (value << i)

n = 0b1010  # 10
print(f"n = {n} -> {n:08b}\n")

print(f"{'Operation':<22} {'Result':>5}  Binary")
print("-" * 45)
print(f"{'get_bit(n, 1)':<22} {get_bit(n, 1):>5}  (bit 1 is set)")
print(f"{'get_bit(n, 2)':<22} {get_bit(n, 2):>5}  (bit 2 is clear)")
print(f"{'set_bit(n, 0)':<22} {set_bit(n, 0):>5}  {set_bit(n, 0):08b}")
print(f"{'clear_bit(n, 3)':<22} {clear_bit(n, 3):>5}  {clear_bit(n, 3):08b}")
print(f"{'toggle_bit(n, 1)':<22} {toggle_bit(n, 1):>5}  {toggle_bit(n, 1):08b}")
print(f"{'update_bit(n, 2, 1)':<22} {update_bit(n, 2, 1):>5}  {update_bit(n, 2, 1):08b}")

print("\n-> Mask trick: (1 << i) isolates bit i")

# ==================== (3) Essential Bit Tricks ====================
print("\n[3] Essential Bit Tricks")
print("-" * 70)

def is_even(n: int) -> bool:
    """Last bit 0 means even"""
    return (n & 1) == 0

def is_power_of_two(n: int) -> bool:
    """Exactly one bit set"""
    return n > 0 and (n & (n - 1)) == 0

def lowest_set_bit(n: int) -> int:
    """Isolate rightmost 1-bit"""
    return n & -n

def clear_lowest_set_bit(n: int) -> int:
    """Turn off rightmost 1-bit"""
    return n & (n - 1)

print("Power of two check:  n > 0 and (n & (n-1)) == 0")
for x in [1, 8, 12, 16, 31, 64]:
    mark = "YES" if is_power_of_two(x) else "no "
    print(f"  {x:>3} = {x:08b}  ->  {mark}   (n-1 = {x-1:08b}, AND = {x & (x-1):08b})")

print("\nIsolate / clear the lowest set bit:")
for x in [12, 10, 40]:
    print(f"  {x:>3} = {x:08b}   n & -n = {lowest_set_bit(x):08b}"
          f"   n & (n-1) = {clear_lowest_set_bit(x):08b}")

print("\nSwap without a temp variable:")
p, q = 7, 19
print(f"  before: p={p}, q={q}")
p ^= q
q ^= p
p ^= q
print(f"  after:  p={p}, q={q}")

print("\n-> All O(1), no arithmetic needed")

# ==================== (4) Counting Set Bits ====================
print("\n[4] Counting Set Bits (Three Ways)")
print("-" * 70)

def count_bits_naive(n: int) -> int:
    """Check every bit: O(width)"""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_bits_kernighan(n: int) -> int:
    """Clear lowest set bit each pass: O(set bits)"""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count

def count_bits_builtin(n: int) -> int:
    """Python's own popcount"""
    return bin(n).count("1")

print(f"{'Value':>10}  {'Binary':>18}  {'Naive':>6} {'Kernighan':>10} {'Builtin':>8}")
print("-" * 60)
for x in [0, 7, 255, 1024, 4095, 123456]:
    print(f"{x:>10}  {x:>18b}  {count_bits_naive(x):>6} "
          f"{count_bits_kernighan(x):>10} {count_bits_builtin(x):>8}")

# Benchmark: Kernighan wins on sparse numbers
sparse = 1 << 30  # one bit set, 31 bits wide
ITERS = 100_000

start = time.perf_counter()
for _ in range(ITERS):
    count_bits_naive(sparse)
naive_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for _ in range(ITERS):
    count_bits_kernighan(sparse)
kern_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for _ in range(ITERS):
    count_bits_builtin(sparse)
builtin_ms = (time.perf_counter() - start) * 1000

print(f"\nBenchmark on 2^30 (1 set bit, {ITERS:,} iterations):")
print(f"  Naive     : {naive_ms:>8.2f}ms  (31 loop passes)")
print(f"  Kernighan : {kern_ms:>8.2f}ms  (1 loop pass, {naive_ms/kern_ms:.1f}x faster)")
print(f"  Builtin   : {builtin_ms:>8.2f}ms  (C-level)")

print("\n-> Kernighan: O(set bits) beats O(width) on sparse values")

# ==================== (5) XOR Patterns ====================
print("\n[5] XOR Patterns (O(1) Space Solutions)")
print("-" * 70)

def single_number(nums: List[int]) -> int:
    """All appear twice except one. XOR cancels pairs."""
    result = 0
    for n in nums:
        result ^= n
    return result

def missing_number(nums: List[int]) -> int:
    """Array holds 0..n with one missing"""
    result = len(nums)
    for i, n in enumerate(nums):
        result ^= i ^ n
    return result

def two_single_numbers(nums: List[int]) -> Tuple[int, int]:
    """All appear twice except two. Partition by a differing bit."""
    xor_all = 0
    for n in nums:
        xor_all ^= n            # == a ^ b

    diff_bit = xor_all & -xor_all   # a bit where a and b differ

    x = y = 0
    for n in nums:
        if n & diff_bit:
            x ^= n
        else:
            y ^= n
    return x, y

print("XOR properties:  x^0 = x   x^x = 0   commutative   associative\n")

nums = [4, 1, 2, 1, 2]
print(f"single_number({nums})")
print(f"  -> {single_number(nums)}   (pairs cancel, loner survives)")

nums = [3, 0, 1]
print(f"\nmissing_number({nums})  # from range 0..3")
print(f"  -> {missing_number(nums)}   (XOR indices against values)")

nums = [1, 2, 1, 3, 2, 5]
x, y = two_single_numbers(nums)
print(f"\ntwo_single_numbers({nums})")
print(f"  xor_all = {3 ^ 5} -> differing bit = {(3 ^ 5) & -(3 ^ 5)}")
print(f"  -> {sorted((x, y))}   (two groups, one loner each)")

print("\n-> O(n) time, O(1) space -- a hash set would need O(n) space")

# ==================== (6) Bitmasks as Sets ====================
print("\n[6] Bitmasks as Sets (Subset Enumeration)")
print("-" * 70)

def all_subsets(items: List[str]) -> List[List[str]]:
    """Every subset via 2^n bitmasks"""
    n = len(items)
    subsets = []
    for mask in range(1 << n):
        subsets.append([items[i] for i in range(n) if mask & (1 << i)])
    return subsets

items = ["a", "b", "c"]
subsets = all_subsets(items)

print(f"Items: {items}  ->  2^{len(items)} = {len(subsets)} subsets\n")
print(f"{'Mask':>6}  {'Binary':>8}  Subset")
print("-" * 34)
for mask, subset in enumerate(subsets):
    label = "{" + ", ".join(subset) + "}" if subset else "{}"
    print(f"{mask:>6}  {mask:>8b}  {label}")

# Bitmask as a character-seen tracker
def has_unique_chars(s: str) -> bool:
    """Track a-z in a single 32-bit int"""
    seen = 0
    for ch in s:
        bit = 1 << (ord(ch) - ord("a"))
        if seen & bit:
            return False
        seen |= bit
    return True

print("\nBitmask as a 'seen characters' set (26 bits, one int):")
for word in ["algorithm", "letter", "python"]:
    print(f"  has_unique_chars('{word}') -> {has_unique_chars(word)}")

print("\n-> One integer replaces a whole set object")

# ==================== (7) Bitmask DP: Travelling Salesman ====================
print("\n[7] Bitmask DP: Travelling Salesman Problem")
print("-" * 70)

def tsp(dist: List[List[int]]) -> int:
    """Minimum cost Hamiltonian cycle from city 0. O(2^n * n^2)"""
    n = len(dist)
    FULL = (1 << n) - 1
    INF = float("inf")

    # dp[mask][i] = min cost to visit set `mask`, ending at city i
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0, only city 0 visited

    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == INF or not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue  # already visited
                nxt = mask | (1 << j)
                cost = dp[mask][i] + dist[i][j]
                if cost < dp[nxt][j]:
                    dp[nxt][j] = cost

    return min(dp[FULL][i] + dist[i][0] for i in range(1, n))

def tsp_brute_force(dist: List[List[int]]) -> int:
    """All permutations. O(n!)"""
    from itertools import permutations
    n = len(dist)
    best = float("inf")
    for perm in permutations(range(1, n)):
        route = (0,) + perm + (0,)
        cost = sum(dist[route[k]][route[k + 1]] for k in range(len(route) - 1))
        best = min(best, cost)
    return best

dist = [
    [0, 20, 42, 35],
    [20, 0, 30, 34],
    [42, 30, 0, 12],
    [35, 34, 12, 0],
]
cities = ["A", "B", "C", "D"]

print("Distance matrix:")
print("       " + "".join(f"{c:>5}" for c in cities))
for i, row in enumerate(dist):
    print(f"  {cities[i]}  " + "".join(f"{d:>5}" for d in row))

start = time.perf_counter()
dp_cost = tsp(dist)
dp_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
bf_cost = tsp_brute_force(dist)
bf_ms = (time.perf_counter() - start) * 1000

print(f"\nBitmask DP  : cost = {dp_cost}  ({dp_ms:.3f}ms)  O(2^n * n^2)")
print(f"Brute force : cost = {bf_cost}  ({bf_ms:.3f}ms)  O(n!)")
print(f"Match: {dp_cost == bf_cost}")

print("\nGrowth comparison (operations):")
print(f"{'n':>4}  {'n! (brute)':>16}  {'2^n * n^2 (DP)':>16}")
print("-" * 42)
import math
for size in [5, 10, 15, 20]:
    print(f"{size:>4}  {math.factorial(size):>16,}  {(1 << size) * size * size:>16,}")

print("\n-> Bitmask DP makes n=20 tractable; n! does not")

# ==================== (8) Bit Reversal and Rotation ====================
print("\n[8] Bit Reversal and Rotation (32-bit)")
print("-" * 70)

MASK32 = 0xFFFFFFFF

def reverse_bits_32(n: int) -> int:
    """Reverse bit order in a 32-bit word. O(32)"""
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

def rotate_left_32(n: int, k: int) -> int:
    """Circular left shift"""
    k %= 32
    return ((n << k) | (n >> (32 - k))) & MASK32

def rotate_right_32(n: int, k: int) -> int:
    """Circular right shift"""
    k %= 32
    return ((n >> k) | (n << (32 - k))) & MASK32

def to_signed_32(n: int) -> int:
    """Interpret a 32-bit pattern as signed"""
    n &= MASK32
    return n - (1 << 32) if n & (1 << 31) else n

n = 0b00000010100101000001111010011100
print(f"original : {n:032b}  ({n})")
print(f"reversed : {reverse_bits_32(n):032b}  ({reverse_bits_32(n)})")

n = 0b1011
print(f"\nn = {n:032b}  ({n})")
print(f"rot_left  4 : {rotate_left_32(n, 4):032b}  ({rotate_left_32(n, 4)})")
print(f"rot_right 1 : {rotate_right_32(n, 1):032b}  ({rotate_right_32(n, 1)})")

print("\nTwo's complement in fixed width:")
for x in [5, -5, 1, -1]:
    print(f"  {x:>3} -> {x & MASK32:032b} -> signed back: {to_signed_32(x & MASK32)}")

print("\n-> Python ints are unbounded; mask with 0xFFFFFFFF for 32-bit semantics")

# ==================== (9) Arithmetic Without Operators ====================
print("\n[9] Arithmetic Using Only Bits")
print("-" * 70)

def add_without_plus(a: int, b: int) -> int:
    """XOR is sum-without-carry; (a & b) << 1 is the carry"""
    MASK = 0xFFFFFFFF
    INT_MAX = 0x7FFFFFFF
    a &= MASK
    b &= MASK
    while b:
        carry = (a & b) << 1
        a = (a ^ b) & MASK
        b = carry & MASK
    return a if a <= INT_MAX else ~(a ^ MASK)

def multiply_by_shifts(a: int, b: int) -> int:
    """Shift-and-add multiplication"""
    result = 0
    while b:
        if b & 1:
            result += a
        a <<= 1
        b >>= 1
    return result

def divide_by_shifts(dividend: int, divisor: int) -> int:
    """Repeated subtraction with doubling. O(log^2 n)"""
    quotient = 0
    while dividend >= divisor:
        shift, temp = 0, divisor
        while dividend >= (temp << 1):
            temp <<= 1
            shift += 1
        dividend -= temp
        quotient += 1 << shift
    return quotient

print("add_without_plus (XOR + carry loop):")
for x, y in [(7, 5), (13, 29), (-3, 8)]:
    print(f"  {x:>4} + {y:>3} = {add_without_plus(x, y):>5}   (check: {x + y})")

print("\nmultiply_by_shifts (shift-and-add):")
for x, y in [(6, 7), (13, 11), (25, 4)]:
    print(f"  {x:>3} * {y:>3} = {multiply_by_shifts(x, y):>5}   (check: {x * y})")

print("\ndivide_by_shifts (doubling subtraction):")
for x, y in [(100, 7), (255, 16), (81, 9)]:
    print(f"  {x:>3} / {y:>3} = {divide_by_shifts(x, y):>5}   (check: {x // y})")

print("\n-> How hardware ALUs actually work")

# ==================== (10) Applied Bit Techniques ====================
print("\n[10] Applied Bit Techniques")
print("-" * 70)

def count_bits_range(n: int) -> List[int]:
    """Set-bit count for 0..n using DP: dp[i] = dp[i >> 1] + (i & 1)"""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

def hamming_distance(x: int, y: int) -> int:
    """Number of differing bit positions"""
    return bin(x ^ y).count("1")

def gray_code(n: int) -> List[int]:
    """Sequence where consecutive values differ by one bit"""
    return [i ^ (i >> 1) for i in range(1 << n)]

def single_number_three_times(nums: List[int]) -> int:
    """All appear 3x except one. Count each bit position mod 3."""
    result = 0
    for bit in range(32):
        total = sum((n >> bit) & 1 for n in nums)
        if total % 3:
            result |= 1 << bit
    return result

print("count_bits_range(15) via dp[i] = dp[i>>1] + (i&1):")
counts = count_bits_range(15)
print("  " + "  ".join(f"{i}:{c}" for i, c in enumerate(counts)))
print("  -> O(n) total instead of O(n log n)")

print("\nhamming_distance (XOR then popcount):")
for x, y in [(1, 4), (3, 1), (93, 73)]:
    print(f"  d({x}, {y}) = {hamming_distance(x, y)}"
          f"   ({x:07b} vs {y:07b}, XOR = {x ^ y:07b})")

print("\ngray_code(3)  -- consecutive values differ by exactly one bit:")
for code in gray_code(3):
    print(f"  {code:>2}  {code:03b}")

nums = [2, 2, 3, 2]
print(f"\nsingle_number_three_times({nums}) -> {single_number_three_times(nums)}")
print("  -> XOR fails here (x^x^x = x); count bits mod 3 instead")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
