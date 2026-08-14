"""
Rosetta Code Challenges -- Warm-up

Five classic tasks. Every description here is written for this platform; only
the task names are shared with the wider community, and a name is an idea
rather than protected text.

Solve them in Python, TypeScript or JavaScript -- the tests are the same either
way, which is the entire point of a Rosetta-style course.
"""

from typing import Dict, List

print("=" * 70)
print("ROSETTA CODE: Warm-up")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. FIZZBUZZ")
print("Input: An integer n >= 0")
print("Output: A list of n strings for the numbers 1..n")
print("Example: n=5 -> ['1','2','Fizz','4','Buzz']")
def fizzbuzz(n: int) -> List[str]:
    """
    For each number from 1 to n, produce a string:
      - "Fizz" when it divides by 3
      - "Buzz" when it divides by 5
      - "FizzBuzz" when it divides by both
      - otherwise the number itself, as text
    """
    # TODO: Write your code here
    pass

print("\n2. LEAP YEAR")
print("Input: A year as an integer")
print("Output: True if it is a leap year in the Gregorian calendar")
print("Example: 1900 -> False, 2000 -> True, 2024 -> True")
def is_leap_year(year: int) -> bool:
    """
    Divisible by 4, except centuries, except those divisible by 400.

    1900 is the case that catches a naive rule: divisible by 4 and by 100,
    but not by 400, so it is NOT a leap year.
    """
    # TODO: Write your code here
    pass

print("\n3. SUM MULTIPLES OF 3 AND 5")
print("Input: An integer limit")
print("Output: The sum of every positive multiple of 3 or 5 below it")
print("Example: 10 -> 23  (3 + 5 + 6 + 9)")
def sum_multiples(limit: int) -> int:
    """
    Strictly BELOW the limit, and each number counted once -- 15 is a multiple
    of both and must not be added twice.
    """
    # TODO: Write your code here
    pass

print("\n4. GENERATE LOWER CASE ASCII ALPHABET")
print("Input: Two letters, first and last, inclusive")
print("Output: The letters from first to last")
print("Example: 'a','e' -> ['a','b','c','d','e']")
def ascii_range(first: str, last: str) -> List[str]:
    """
    Build it from character codes rather than typing the alphabet out: the
    point of the task is the arithmetic, and a hardcoded string cannot answer
    'h' to 'p'. Return an empty list when last comes before first.
    """
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. 100 DOORS")
print("Input: The number of doors, n")
print("Output: The 1-based numbers of the doors left open")
print("Example: n=10 -> [1, 4, 9]")
def open_doors(n: int) -> List[int]:
    """
    n doors all start closed. On pass i you toggle every i-th door: pass 1
    touches every door, pass 2 every second, and so on to pass n.

    Simulating it is fine and is the honest first answer. Once it works, look
    at which numbers survive and you will see why -- a door ends open exactly
    when it has an odd number of divisors.
    """
    # TODO: Write your code here
    pass
