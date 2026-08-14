# Sequences — Prefix Sums, Subsequences, and Filling Grids

Five tasks that build or traverse a sequence. Two have a naive version that is
quadratic and a linear one that is barely longer.

## Build Iteratively, Not Recursively

**Fibonacci** is the standard example of recursion and the standard example of
why naive recursion is a trap:

```python
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)   # O(2^n)
```

`fib(35)` makes about 30 million calls to compute 35 numbers. The iterative form
is `O(n)` and needs two variables:

```python
a, b = 0, 1
for _ in range(n):
    out.append(a)
    a, b = b, a + b
```

Read the swap carefully: both right-hand values are evaluated *before* either
assignment, so it does the right thing. Written as two statements it does not,
and that is a real bug in a real language — JavaScript needs
`[a, b] = [b, a + b]` for the same reason.

`n` here is a **count**. `n = 0` is an empty list; `n = 1` is `[0]`.

## Prefix Sums

**Equilibrium index** asks for every position where the values to the left sum to
the same as the values to the right, with the element itself counting for neither
side.

The obvious version sums both halves at every index: `O(n²)`. But the left sum
grows by one element per step, and the right sum is `total - left - current`, so
one running variable plus the grand total does it in one pass:

```python
total = sum(numbers)
left = 0
for i, value in enumerate(numbers):
    if left == total - left - value:
        out.append(i)
    left += value
```

That is the prefix-sum idea in its smallest useful form, and it generalises: any
question about "everything before here" versus "everything after here" is one
running total away from linear.

Two edges: an empty list has no indices, and `[0]` has exactly one — index 0,
where both empty sides sum to 0.

## Subsequence Is Not Substring

**Longest increasing subsequence** turns on the definition:

- a **substring** is contiguous — `[2, 6, 4]` from `[3, 2, 6, 4, 5, 1]`
- a **subsequence** keeps order but may skip — `[2, 4, 5]` from the same list

So the answer for `[3, 2, 6, 4, 5, 1]` is 3, via `2, 4, 5`, which are not
adjacent. And *strictly* increasing means `[5, 5, 5]` has an answer of 1.

The `O(n²)` dynamic programme is the honest first solution: `best[i]` is the
longest run ending at `i`, found by looking at every earlier smaller element.
Because this task asks only for the **length**, the `O(n log n)` patience-sorting
version is also available — keep an array of the smallest possible tail for each
length and binary-search it. Reconstructing the actual subsequence that way is
harder, which is why the task asks for the length.

## Filling a Grid by Walking It

**Spiral matrix** and **zig-zag matrix** both number the cells of an `n × n` grid
in an unusual order, and they invite two different techniques.

Spiral is a **walk with turns**. Move in a direction until the next cell would
leave the grid or is already filled, then turn clockwise:

```python
dr, dc = dc, -dr        # the clockwise turn, in one line
```

Shrinking boundaries — track top, bottom, left, right and close them in — also
works here, and is often taught first. It works *because this spiral stays inside
the grid*. The variant in the DSA course walks off the grid and comes back, where
boundary-shrinking breaks completely and only the direction-walk survives. Worth
comparing the two.

Zig-zag is a **sort**. Every cell on an anti-diagonal shares the same `row + col`,
and the direction alternates by the parity of that sum:

```python
cells = sorted(((r, c) for r in range(n) for c in range(n)),
               key=lambda rc: (rc[0] + rc[1],
                               rc[1] if (rc[0] + rc[1]) % 2 == 0 else -rc[1]))
```

Then number them in that order. Choosing the right sort key is often easier than
simulating the movement, and this is the clearest small example of that.

Both tasks return `[]` for `n = 0` rather than `[[]]`.
