"""Runnable demonstrations for the Sequences module."""

import time

print("=" * 60)
print("1. Naive Fibonacci recursion, measured")
print("=" * 60)

calls = 0


def fib_recursive(n):
    global calls
    calls += 1
    return n if n < 2 else fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


for n in (10, 20, 28):
    calls = 0
    started = time.perf_counter()
    value = fib_recursive(n)
    took = (time.perf_counter() - started) * 1000
    print(f"  fib({n}) = {value:<8} recursion: {calls:>9,} calls, {took:7.1f} ms")
started = time.perf_counter()
fib_iterative(28)
print(f"  fib(28) iteratively: 28 steps, {(time.perf_counter() - started) * 1000:.4f} ms")

print("\n" + "=" * 60)
print("2. Equilibrium indices: quadratic versus one pass")
print("=" * 60)
numbers = [-7, 1, 5, 2, -4, 3, 0]
print(f"  {numbers}")
for i, value in enumerate(numbers):
    left, right = sum(numbers[:i]), sum(numbers[i + 1:])
    mark = "  <-- equilibrium" if left == right else ""
    print(f"    index {i}: left={left:>3} right={right:>3}{mark}")
print("  The one-pass version keeps `left` as a running total and derives")
print("  `right` as total - left - current. Same answer, O(n).")

print("\n" + "=" * 60)
print("3. Subsequence is not substring")
print("=" * 60)
numbers = [3, 2, 6, 4, 5, 1]
print(f"  {numbers}")
print("    longest increasing SUBSTRING   (contiguous): [2, 6] -> 2")
print("    longest increasing SUBSEQUENCE (may skip) : [2, 4, 5] -> 3")
print("  The answer is 3, and those elements are not adjacent.")

print("\n" + "=" * 60)
print("4. Two orders of filling the same grid")
print("=" * 60)


def spiral(n):
    grid = [[None] * n for _ in range(n)]
    r = c = 0
    dr, dc = 0, 1
    for v in range(n * n):
        grid[r][c] = v
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc] is not None:
            dr, dc = dc, -dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return grid


def zigzag(n):
    cells = sorted(((r, c) for r in range(n) for c in range(n)),
                   key=lambda rc: (rc[0] + rc[1],
                                   rc[1] if (rc[0] + rc[1]) % 2 == 0 else -rc[1]))
    grid = [[0] * n for _ in range(n)]
    for v, (r, c) in enumerate(cells):
        grid[r][c] = v
    return grid


for name, grid in (("spiral", spiral(5)), ("zig-zag", zigzag(5))):
    print(f"  {name} (n=5):")
    for row in grid:
        print("    " + " ".join(f"{v:2}" for v in row))
print("  Spiral is a walk that turns. Zig-zag is a sort by (row+col, then")
print("  row or col depending on parity). Picking the right key beats simulating.")
