# Bit Manipulation - Thinking in Binary

Master bitwise operators, bit tricks, and the problems they solve in O(1) space.

---

## 1. Why Bit Manipulation?

Every integer is a sequence of bits. Manipulating bits directly gives you:

- **Speed**: bitwise ops are single CPU instructions
- **Space**: a 64-bit integer stores 64 booleans
- **Elegance**: many problems collapse to one line
- **Interview relevance**: a staple category of tricky questions

### Binary Refresher

```
Decimal    Binary      Bits set
   0       0000            0
   1       0001            1
   5       0101            2
  10       1010            2
  15       1111            4
```

Bit `i` has value `2^i`. Bit 0 is the least significant (rightmost).

```python
bin(10)          # '0b1010'
int('1010', 2)   # 10
format(10, '08b')  # '00001010'
```

---

## 2. The Six Bitwise Operators

| Operator | Name | Rule | Example |
|----------|------|------|---------|
| `&` | AND | 1 only if both are 1 | `1010 & 0110 = 0010` |
| `\|` | OR | 1 if either is 1 | `1010 \| 0110 = 1110` |
| `^` | XOR | 1 if bits differ | `1010 ^ 0110 = 1100` |
| `~` | NOT | flip every bit | `~1010 = ...0101` |
| `<<` | Left shift | multiply by 2^k | `1010 << 1 = 10100` |
| `>>` | Right shift | floor-divide by 2^k | `1010 >> 1 = 0101` |

```python
a, b = 10, 6      # 1010, 0110

a & b   # 2   -> 0010
a | b   # 14  -> 1110
a ^ b   # 12  -> 1100
~a      # -11 (two's complement)
a << 1  # 20  -> 10100
a >> 1  # 5   -> 0101
```

### XOR: The Most Useful Operator

XOR has four properties that power dozens of tricks:

```
x ^ 0 = x          (identity)
x ^ x = 0          (self-inverse)
x ^ y = y ^ x      (commutative)
(x^y)^z = x^(y^z)  (associative)
```

Consequence: XOR-ing a list cancels every value that appears twice.

---

## 3. Core Bit Operations

```python
def get_bit(n, i):
    """Is bit i set?"""
    return (n >> i) & 1

def set_bit(n, i):
    """Turn bit i on."""
    return n | (1 << i)

def clear_bit(n, i):
    """Turn bit i off."""
    return n & ~(1 << i)

def toggle_bit(n, i):
    """Flip bit i."""
    return n ^ (1 << i)

def update_bit(n, i, value):
    """Set bit i to 0 or 1."""
    return (n & ~(1 << i)) | (value << i)
```

**Mask thinking**: `1 << i` builds a mask with only bit `i` set. AND with the mask
to test, OR to set, AND with the complement to clear, XOR to flip.

**Time**: O(1) for all, **Space**: O(1)

---

## 4. Essential Bit Tricks

### Check Even / Odd
```python
n & 1 == 0   # even (last bit is 0)
```

### Check Power of Two
```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```
Why: a power of two has exactly one bit set. `n - 1` flips that bit off and turns
all lower bits on, so the AND is zero.

```
8     = 1000
8 - 1 = 0111
AND   = 0000  ✓
```

### Clear the Lowest Set Bit
```python
n & (n - 1)
```

### Isolate the Lowest Set Bit
```python
n & -n       # 12 (1100) -> 4 (0100)
```

### Count Set Bits (Brian Kernighan)
```python
def count_bits(n):
    count = 0
    while n:
        n &= n - 1      # clear lowest set bit
        count += 1
    return count
```
Runs in O(number of set bits), not O(total bits).

```python
bin(n).count('1')   # Pythonic equivalent
n.bit_count()       # Python 3.10+
```

### Swap Without a Temp
```python
a ^= b
b ^= a
a ^= b
```

### Multiply / Divide by Powers of Two
```python
n << k    # n * 2^k
n >> k    # n // 2^k  (floor, for non-negative n)
```

---

## 5. Two's Complement and Negative Numbers

Negative integers are stored as two's complement: invert all bits, add one.

```
 5 (8-bit) = 0000 0101
-5 (8-bit) = 1111 1011
```

Key identities:
```python
-n == ~n + 1
~n == -n - 1
```

**Python caveat**: Python ints are arbitrary precision, so there is no fixed
width and `>>` is an arithmetic shift that preserves sign. To simulate 32-bit
behaviour, mask explicitly:

```python
MASK32 = 0xFFFFFFFF

def to_signed_32(n):
    n &= MASK32
    return n - (1 << 32) if n & (1 << 31) else n
```

---

## 6. XOR Problem Patterns

### Single Number (all others appear twice)
```python
def single_number(nums):
    result = 0
    for n in nums:
        result ^= n
    return result
```
Pairs cancel to 0; the loner survives. **O(n) time, O(1) space.**

### Missing Number from 0..n
```python
def missing_number(nums):
    result = len(nums)
    for i, n in enumerate(nums):
        result ^= i ^ n
    return result
```

### Two Single Numbers (all others appear twice)
```python
def single_number_two(nums):
    xor_all = 0
    for n in nums:
        xor_all ^= n            # = a ^ b

    diff_bit = xor_all & -xor_all   # a bit where a and b differ

    a = b = 0
    for n in nums:
        if n & diff_bit:
            a ^= n
        else:
            b ^= n
    return a, b
```
The differing bit partitions the array into two groups, each with one loner.

### Find Duplicate / Sum Without `+`
```python
def add_without_plus(a, b):
    MASK = 0xFFFFFFFF
    while b & MASK:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a & MASK if b > MASK else a
```
XOR is sum-without-carry; AND-then-shift is the carry.

---

## 7. Bitmasks as Sets

An integer is a compact subset of `{0, 1, ..., n-1}`.

```python
mask = 0                # {}
mask |= (1 << 3)        # add 3
mask &= ~(1 << 3)       # remove 3
mask ^= (1 << 3)        # toggle 3
bool(mask & (1 << 3))   # contains 3?
mask.bit_count()        # size
```

### Enumerate All Subsets
```python
def all_subsets(items):
    n = len(items)
    for mask in range(1 << n):          # 2^n masks
        subset = [items[i] for i in range(n) if mask & (1 << i)]
        yield subset
```
**Time**: O(n · 2^n) — generating every subset costs at least that.

### Enumerate Submasks of a Mask
```python
sub = mask
while sub:
    process(sub)
    sub = (sub - 1) & mask
```
Total over all masks: O(3^n), the classic subset-sum-over-subsets bound.

### Bitmask DP (Travelling Salesman)
```python
def tsp(dist):
    n = len(dist)
    FULL = (1 << n) - 1
    INF = float('inf')

    # dp[mask][i] = min cost visiting `mask`, currently at i
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == INF or not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                nxt = mask | (1 << j)
                dp[nxt][j] = min(dp[nxt][j], dp[mask][i] + dist[i][j])

    return min(dp[FULL][i] + dist[i][0] for i in range(1, n))
```
**Time**: O(2^n · n²) — feasible up to n ≈ 20, versus O(n!) brute force.

---

## 8. Bit Reversal and Rotation

```python
def reverse_bits_32(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

def rotate_left_32(n, k):
    k %= 32
    return ((n << k) | (n >> (32 - k))) & 0xFFFFFFFF
```

Reversal via divide-and-conquer swaps halves, then quarters, then pairs — O(log w)
instead of O(w).

---

## 9. Complexity Summary

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| get/set/clear/toggle bit | O(1) | O(1) | single mask op |
| Count set bits (Kernighan) | O(k) | O(1) | k = set bits |
| Count set bits (naive) | O(w) | O(1) | w = word width |
| Is power of two | O(1) | O(1) | `n & (n-1)` |
| Single number (XOR) | O(n) | O(1) | beats hash set's O(n) space |
| Missing number (XOR) | O(n) | O(1) | no overflow risk |
| Reverse bits | O(w) | O(1) | O(log w) with halving |
| Enumerate subsets | O(n · 2ⁿ) | O(n) | output-bound |
| Iterate submasks | O(3ⁿ) total | O(1) | sum over all masks |
| Bitmask DP (TSP) | O(2ⁿ · n²) | O(2ⁿ · n) | n ≤ ~20 |

---

## 10. Bit Manipulation vs Alternatives

| Problem | Bit approach | Conventional | Winner |
|---------|--------------|--------------|--------|
| Find unique element | XOR, O(1) space | hash set, O(n) space | **Bits** |
| Track seen chars (a–z) | 32-bit mask | set / dict | **Bits** (small alphabet) |
| Subset enumeration | mask loop | recursion | Tie (bits are iterative) |
| Permutation state | bitmask DP | memo on tuples | **Bits** (faster hashing) |
| Large sparse sets | — | set / dict | **Conventional** |
| Readable business logic | — | plain code | **Conventional** |

Bit tricks are a tool, not a default. Reach for them when space is tight, the
universe is small and fixed, or the problem is inherently about bits.

---

## 11. Common Pitfalls

1. **Operator precedence**: `&` binds looser than `==`. Write `(n & 1) == 0`,
   not `n & 1 == 0` (the latter parses as `n & (1 == 0)`).
2. **Python has no fixed width**: `~n` and `>>` behave differently than in C.
   Mask with `0xFFFFFFFF` when a problem specifies 32 bits.
3. **Negative shifts raise**: `n << -1` is a `ValueError`, not a right shift.
4. **`n & -n` on zero** returns 0 — guard the empty case.
5. **XOR does not detect triples**: `x^x^x = x`. For "appears three times",
   count bits mod 3 instead.
6. **Off-by-one in masks**: full mask for n bits is `(1 << n) - 1`, not `1 << n`.

---

## 12. Key Takeaways

✅ **`&` `|` `^` `~` `<<` `>>`** — six operators cover every trick
✅ **XOR cancels duplicates** — the single-number family in O(1) space
✅ **`n & (n-1)`** clears the lowest set bit → power-of-two test, bit counting
✅ **`n & -n`** isolates the lowest set bit → partitioning tricks
✅ **`1 << i`** is your mask builder — test, set, clear, toggle
✅ **Integers are sets** — bitmask DP turns O(n!) into O(2ⁿ · n²)
✅ **Mask to 32 bits** in Python when the problem assumes fixed width
✅ **Parenthesize** bitwise expressions; precedence surprises are the #1 bug

**Interview Focus**:
- Explain *why* `n & (n-1)` works, don't just recite it
- Reach for XOR when you see "appears twice / exactly one differs"
- Recognize bitmask DP when state is "which subset have I used?"
- State the space win: O(1) instead of O(n)

Next: Implement the operators, then the tricks, then bitmask DP!
