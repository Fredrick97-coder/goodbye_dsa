"""
Rosetta Code Challenges -- Sequences

Five sequence and matrix tasks. Descriptions written for this platform.
"""

from typing import List

print("=" * 70)
print("ROSETTA CODE: Sequences")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. FIBONACCI SEQUENCE")
print("Input: A count n >= 0")
print("Output: The first n Fibonacci numbers, starting 0, 1")
print("Example: 8 -> [0,1,1,2,3,5,8,13]")
def fibonacci(n: int) -> List[int]:
    """
    Start from 0 and 1. n=0 gives an empty list, n=1 gives [0].

    Iterate rather than recurse: the naive recursion recomputes the same values
    exponentially often and is unusable past about n=35.
    """
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n2. EQUILIBRIUM INDEX")
print("Input: A list of integers")
print("Output: Every index where the values left and right sum equally")
print("Example: [-7,1,5,2,-4,3,0] -> [3, 6]")
def equilibrium_indices(numbers: List[int]) -> List[int]:
    """
    At an equilibrium index, the sum before it equals the sum after it. The
    element itself counts as neither side.

    The obvious version re-sums both halves at every index, O(n^2). One running
    total and the grand total gets it to O(n).
    """
    # TODO: Write your code here
    pass

print("\n3. LONGEST INCREASING SUBSEQUENCE")
print("Input: A list of integers")
print("Output: The length of the longest strictly increasing subsequence")
print("Example: [3,2,6,4,5,1] -> 3  (2,4,5)")
def longest_increasing(numbers: List[int]) -> int:
    """
    A subsequence keeps order but need not be contiguous. Strictly increasing,
    so equal neighbours do not extend it.

    The length is all that is asked for, which makes the O(n log n) version
    with a patience-sorting tails array available to you.
    """
    # TODO: Write your code here
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n4. SPIRAL MATRIX")
print("Input: A size n")
print("Output: An n x n matrix filled 0..n*n-1 in inward clockwise order")
print("Example: n=3 -> [[0,1,2],[7,8,3],[6,5,4]]")
def spiral_matrix(n: int) -> List[List[int]]:
    """
    Start at the top-left going right, and turn clockwise whenever the next
    cell would leave the grid or is already filled.

    Shrinking boundaries work here, unlike the walk-off-the-grid variant in the
    DSA course -- worth comparing the two.
    """
    # TODO: Write your code here
    pass

print("\n5. ZIG-ZAG MATRIX")
print("Input: A size n")
print("Output: An n x n matrix filled 0..n*n-1 along the anti-diagonals")
print("Example: n=3 -> [[0,1,5],[2,4,6],[3,7,8]]")
def zigzag_matrix(n: int) -> List[List[int]]:
    """
    Walk the anti-diagonals (cells where row+col is constant), alternating
    direction on each one, and number the cells in the order you visit them.

    Sorting the coordinates by (row+col, then row or col depending on parity)
    is a tidy way in.
    """
    # TODO: Write your code here
    pass
