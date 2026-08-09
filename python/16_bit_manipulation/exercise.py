"""
Exercises: Bit Manipulation

Practice bitwise operators, XOR tricks, bitmasks, and bitmask DP.
"""

from typing import List, Tuple

print("=" * 70)
print("EXERCISES: Bit Manipulation")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. COUNT SET BITS (HAMMING WEIGHT)")
print("Input: A non-negative integer")
print("Output: Number of 1 bits")
print("Example: 11 (1011) -> 3")
def count_set_bits(n: int) -> int:
    # TODO: Use Brian Kernighan's trick: n &= n - 1 clears the lowest set bit
    pass

print("\n2. IS POWER OF TWO")
print("Input: An integer")
print("Output: True if it is a power of two")
print("Example: 16 -> True, 12 -> False")
def is_power_of_two(n: int) -> bool:
    # TODO: A power of two has exactly one set bit -> n > 0 and (n & (n-1)) == 0
    pass

print("\n3. SINGLE NUMBER")
print("Input: Array where every element appears twice except one")
print("Output: The element that appears once")
print("Example: [4, 1, 2, 1, 2] -> 4")
def single_number(nums: List[int]) -> int:
    # TODO: XOR everything; pairs cancel (x ^ x = 0), the loner survives
    pass

print("\n4. GET / SET / CLEAR BIT")
print("Input: Integer n, bit index i")
print("Output: Bit value, or n with bit i set / cleared")
print("Example: n=10 (1010), i=1 -> get=1, set=10, clear=8")
def get_bit(n: int, i: int) -> int:
    # TODO: Shift bit i down to position 0, then mask with 1
    pass

def set_bit(n: int, i: int) -> int:
    # TODO: OR with a mask that has only bit i set
    pass

def clear_bit(n: int, i: int) -> int:
    # TODO: AND with the complement of the bit-i mask
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. MISSING NUMBER")
print("Input: Array containing n distinct numbers from 0..n, one missing")
print("Output: The missing number")
print("Example: [3, 0, 1] -> 2")
def missing_number(nums: List[int]) -> int:
    # TODO: XOR all indices 0..n against all values; the missing one survives
    pass

print("\n6. COUNTING BITS FOR A RANGE")
print("Input: Integer n")
print("Output: List where result[i] = set bits in i, for i in 0..n")
print("Example: n=5 -> [0, 1, 1, 2, 1, 2]")
def count_bits_range(n: int) -> List[int]:
    # TODO: DP recurrence -- dp[i] = dp[i >> 1] + (i & 1). O(n) total.
    pass

print("\n7. REVERSE BITS (32-BIT)")
print("Input: A 32-bit unsigned integer")
print("Output: The integer with its bit order reversed")
print("Example: 43261596 -> 964176192")
def reverse_bits(n: int) -> int:
    # TODO: Pull bits off the right of n, push them onto the right of result
    pass

print("\n8. HAMMING DISTANCE")
print("Input: Two integers")
print("Output: Number of positions where their bits differ")
print("Example: (1, 4) -> 2")
def hamming_distance(x: int, y: int) -> int:
    # TODO: XOR gives a 1 at each differing position; count those bits
    pass

print("\n9. SUM OF TWO INTEGERS WITHOUT + OR -")
print("Input: Two integers")
print("Output: Their sum, using only bitwise operators")
print("Example: (7, 5) -> 12")
def add_without_plus(a: int, b: int) -> int:
    # TODO: XOR is sum-without-carry; (a & b) << 1 is the carry. Loop until
    # carry is 0. Mask with 0xFFFFFFFF to keep Python's unbounded ints in check.
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n10. SINGLE NUMBER III (TWO LONERS)")
print("Input: Array where every element appears twice except two")
print("Output: The two elements that appear once")
print("Example: [1, 2, 1, 3, 2, 5] -> [3, 5]")
def two_single_numbers(nums: List[int]) -> Tuple[int, int]:
    # TODO: XOR all -> a ^ b. Isolate one differing bit with (xor & -xor),
    # then partition the array on that bit and XOR each group separately.
    pass

print("\n11. SINGLE NUMBER II (APPEARS THREE TIMES)")
print("Input: Array where every element appears 3x except one")
print("Output: The element that appears once")
print("Example: [2, 2, 3, 2] -> 3")
def single_number_three_times(nums: List[int]) -> int:
    # TODO: XOR fails (x^x^x = x). For each of 32 bit positions, sum that bit
    # across all numbers; if the sum % 3 is nonzero, the loner has that bit set.
    pass

print("\n12. MAXIMUM XOR OF TWO NUMBERS IN AN ARRAY")
print("Input: Array of integers")
print("Output: Maximum value of nums[i] ^ nums[j]")
print("Example: [3, 10, 5, 25, 2, 8] -> 28 (5 ^ 25)")
def max_xor_pair(nums: List[int]) -> int:
    # TODO: Build the answer bit by bit from the high end. At each step, assume
    # the next bit can be 1, collect prefixes into a set, and check whether any
    # pair of prefixes XORs to the candidate. O(32n) instead of O(n^2).
    pass

print("\n13. SUBSETS VIA BITMASK")
print("Input: List of distinct items")
print("Output: All 2^n subsets")
print("Example: [1, 2] -> [[], [1], [2], [1, 2]]")
def all_subsets(items: List[int]) -> List[List[int]]:
    # TODO: Loop mask from 0 to (1 << n) - 1; include items[i] when mask has bit i
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n14. TRAVELLING SALESMAN (BITMASK DP)")
print("Input: n x n distance matrix")
print("Output: Minimum cost of a cycle visiting every city, starting at 0")
print("Example: 4 cities -> minimum tour cost")
def tsp(dist: List[List[int]]) -> int:
    # TODO: dp[mask][i] = min cost having visited set `mask`, standing at i.
    # Base: dp[1][0] = 0. Transition: extend to any unvisited j.
    # Answer: min over i of dp[FULL][i] + dist[i][0].  O(2^n * n^2)
    pass

print("\n15. MAXIMUM PRODUCT OF WORD LENGTHS (NO SHARED LETTERS)")
print("Input: List of lowercase words")
print("Output: Max len(a) * len(b) where a and b share no letter")
print("Example: ['abcw','baz','foo','bar','xtfn','abcdef'] -> 16 ('abcw','xtfn')")
def max_product_no_shared_letters(words: List[str]) -> int:
    # TODO: Encode each word as a 26-bit mask of the letters it uses.
    # Two words are disjoint when (mask_a & mask_b) == 0. Compare all pairs.
    pass

print("\n16. GRAY CODE SEQUENCE")
print("Input: Integer n")
print("Output: Sequence of 2^n integers where neighbours differ by one bit")
print("Example: n=2 -> [0, 1, 3, 2]")
def gray_code(n: int) -> List[int]:
    # TODO: The i-th Gray code is i ^ (i >> 1)
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Bit Manipulation Cheat Sheet:

1. The Six Operators:
   &   AND    1 only if both bits are 1
   |   OR     1 if either bit is 1
   ^   XOR    1 if the bits differ
   ~   NOT    flips every bit (~n == -n - 1)
   <<  SHL    multiply by 2^k
   >>  SHR    floor-divide by 2^k

2. Mask Operations (the (1 << i) family):
   Test bit i    (n >> i) & 1
   Set bit i     n | (1 << i)
   Clear bit i   n & ~(1 << i)
   Toggle bit i  n ^ (1 << i)
   Full n-mask   (1 << n) - 1

3. The Two Magic Identities:
   n & (n - 1)   clears the LOWEST set bit
                 -> power-of-two test, Kernighan bit counting
   n & -n        ISOLATES the lowest set bit
                 -> partitioning tricks, Fenwick trees

4. XOR Properties (why the tricks work):
   x ^ 0 = x            identity
   x ^ x = 0            self-inverse -> duplicates cancel
   x ^ y = y ^ x        commutative
   (x^y)^z = x^(y^z)    associative -> order does not matter

5. The XOR Problem Family:
   Appears twice, one loner    -> XOR everything          O(1) space
   Missing from 0..n           -> XOR indices vs values   O(1) space
   Two loners                  -> split on (xor & -xor)   O(1) space
   Appears 3x, one loner       -> count bits mod 3        XOR fails here
   Max XOR pair                -> greedy prefix building  O(32n)

6. Bitmasks as Sets:
   An int is a subset of {0..n-1}. 26 bits covers the lowercase alphabet.
   Enumerate subsets   for mask in range(1 << n)
   Iterate submasks    sub = (sub - 1) & mask
   Subset size         mask.bit_count()   (Python 3.10+)

7. Bitmask DP:
   State: dp[mask][i] where mask = "which items have I used?"
   Turns O(n!) permutation search into O(2^n * n^2).
   Practical up to n ~= 20.
   Classic uses: TSP, assignment problem, Hamiltonian paths, set cover.

Complexity Reference:

Operation                   Time         Space    Note
──────────────────────────────────────────────────────────────────
get/set/clear/toggle        O(1)         O(1)     one mask op
Count bits (Kernighan)      O(k)         O(1)     k = set bits
Count bits (naive)          O(w)         O(1)     w = word width
Power of two test           O(1)         O(1)     n & (n-1)
Single number               O(n)         O(1)     beats hash set
Counting bits for 0..n      O(n)         O(n)     dp[i>>1] + (i&1)
Reverse bits                O(w)         O(1)     O(log w) by halving
Max XOR pair                O(32n)       O(n)     vs O(n^2) brute
Enumerate subsets           O(n * 2^n)   O(n)     output-bound
Iterate all submasks        O(3^n)       O(1)     summed over masks
Bitmask DP (TSP)            O(2^n * n^2) O(2^n n) n <= ~20

Python Gotchas:

1. Precedence: & binds LOOSER than ==.
   Write (n & 1) == 0, not n & 1 == 0.
2. No fixed width: Python ints are arbitrary precision, so ~n and >>
   differ from C. Mask with 0xFFFFFFFF to simulate 32-bit.
3. Negative shift counts raise ValueError, they do not reverse direction.
4. n & -n on 0 returns 0 -- guard the empty case.
5. Full mask for n bits is (1 << n) - 1, not (1 << n).
6. bin(n).count('1') and n.bit_count() are faster than any hand loop.

Problem Recognition Guide:

"exactly one element differs"     -> XOR
"appears twice / k times"         -> XOR or bit-count mod k
"which subset have I chosen"      -> bitmask DP
"all combinations of n items"     -> mask loop over 1 << n
"track seen chars a-z"            -> 26-bit mask
"O(1) extra space required"       -> strong hint toward bits
"power of two / alignment"        -> n & (n-1)

Interview Tips:

1. Explain WHY, not just WHAT. "n & (n-1) clears the lowest set bit
   because n-1 flips that bit off and sets everything below it."
2. Draw the binary. An 8-bit example makes any trick obvious.
3. State the space win out loud: O(1) instead of O(n).
4. Watch the edge cases: 0, negatives, and the full-width value.
5. Do not force it. If a dict is clearer and space is not constrained,
   use the dict.

Learning Progression:

1. Basic: the six operators, get/set/clear/toggle
2. Intermediate: n & (n-1), n & -n, XOR duplicate cancellation
3. Advanced: 32-bit semantics, bit reversal, arithmetic without operators
4. Expert: bitmask DP, submask enumeration, max-XOR prefix greedy

Next: Implement each stub, then run project.py to see bits in production!
""")
