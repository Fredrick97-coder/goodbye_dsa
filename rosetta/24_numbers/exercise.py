"""
Rosetta Code Challenges -- Numbers

Five number-theory tasks. Descriptions written for this platform.
"""

from typing import List

print("=" * 70)
print("ROSETTA CODE: Numbers")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. FACTORIAL")
print("Input: A non-negative integer n")
print("Output: n!")
print("Example: 5 -> 120,  0 -> 1")
def factorial(n: int) -> int:
    """
    0! is 1, not 0 -- the empty product. That single case is what most first
    attempts get wrong.
    """
    # TODO: Write your code here
    pass

print("\n2. GREATEST COMMON DIVISOR")
print("Input: Two integers")
print("Output: Their greatest common divisor, always non-negative")
print("Example: 48,18 -> 6,  -4,6 -> 2,  0,5 -> 5")
def gcd(a: int, b: int) -> int:
    """
    Euclid's algorithm: replace (a, b) with (b, a mod b) until b is zero.

    Handle negatives and zero -- gcd(0, 5) is 5, and the result of gcd(-4, 6)
    is 2 rather than -2.
    """
    # TODO: Write your code here
    pass

print("\n3. LEAST COMMON MULTIPLE")
print("Input: Two integers")
print("Output: Their least common multiple, always non-negative")
print("Example: 4,6 -> 12,  0,5 -> 0")
def lcm(a: int, b: int) -> int:
    """
    a*b // gcd(a, b), with the sign dropped. Dividing before multiplying keeps
    the intermediate value small, which matters for large inputs.

    lcm with zero is zero, and must not divide by zero on the way there.
    """
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n4. HAILSTONE SEQUENCE")
print("Input: A positive integer n")
print("Output: The full sequence from n down to 1")
print("Example: 7 -> [7,22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1]")
def hailstone(n: int) -> List[int]:
    """
    Halve it when even, otherwise triple it and add one, until you reach 1.
    Include both n and the final 1.

    Nobody has proved this terminates for every n. It does for everything you
    will test with.
    """
    # TODO: Write your code here
    pass

print("\n5. HAPPY NUMBERS")
print("Input: A positive integer n")
print("Output: True if n is happy")
print("Example: 7 -> True,  4 -> False")
def is_happy(n: int) -> bool:
    """
    Replace n with the sum of the squares of its digits and repeat. Reach 1 and
    the number is happy; otherwise you fall into a cycle.

    You need to detect the cycle. A set of everything already seen is the
    simplest way; the cycle always passes through 4 if you would rather test
    for that.
    """
    # TODO: Write your code here
    pass
