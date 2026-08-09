# Advanced Trees - Self-Balancing and Range Queries

Master AVL trees, Red-Black trees, Segment Trees, and Fenwick Trees — the
structures that guarantee O(log n) when a plain BST cannot.

---

## 1. Why a Plain BST Is Not Enough

A binary search tree gives O(log n) search *only if it stays balanced*. Insert
sorted data and it degenerates into a linked list:

```
Insert 1, 2, 3, 4, 5 into a plain BST:

1
 \
  2
   \
    3
     \
      4
       \
        5

Height = n, so search = O(n). The tree is now a worse linked list.
```

This is not a rare edge case — sorted or nearly-sorted input is extremely
common (timestamps, IDs, imported data).

**The fix**: enforce a height bound after every mutation. Two classic
approaches:

| Approach | Invariant | Height bound |
|----------|-----------|--------------|
| **AVL** | heights of subtrees differ by ≤ 1 | ≤ 1.44 log n |
| **Red-Black** | every root→leaf path has equal black count | ≤ 2 log n |

Both give O(log n) worst-case search, insert, and delete.

---

## 2. AVL Trees

**Invariant**: for every node, `|height(left) - height(right)| ≤ 1`.

That difference is the **balance factor**.

```python
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1        # cached, so balance checks are O(1)

def height(node):
    return node.height if node else 0

def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0

def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))
```

Caching height on the node is the whole trick — recomputing it would cost
O(n) per check.

### The Four Rotation Cases

An insert can only unbalance nodes on the path back to the root, and only by
one. There are exactly four shapes:

```
LEFT-LEFT (LL) -> single right rotation

      z                     y
     / \                  /   \
    y   d     ==>        x     z
   / \                  / \   / \
  x   c                a   b c   d
 / \
a   b

RIGHT-RIGHT (RR) -> single left rotation  (mirror of LL)

LEFT-RIGHT (LR) -> left-rotate child, then right-rotate node

    z              z              x
   / \            / \           /   \
  y   d   ==>    x   d   ==>   y     z
 / \            / \           / \   / \
a   x          y   c         a   b c   d
   / \        / \
  b   c      a   b

RIGHT-LEFT (RL) -> right-rotate child, then left-rotate node  (mirror of LR)
```

### Rotations

```python
def rotate_right(z):
    """z's left child becomes the new root of this subtree."""
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)      # order matters: z first, it is now lower
    update_height(y)
    return y

def rotate_left(z):
    """z's right child becomes the new root of this subtree."""
    y = z.right
    z.right = y.left
    y.left = z
    update_height(z)
    update_height(y)
    return y
```

A rotation is O(1): it rewires three pointers and fixes two heights. It also
**preserves the BST ordering** — that is why it is safe.

### Insertion

```python
def avl_insert(node, key):
    # 1. Normal BST insert
    if not node:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    elif key > node.key:
        node.right = avl_insert(node.right, key)
    else:
        return node                      # no duplicates

    # 2. Fix the height on the way back up
    update_height(node)

    # 3. Rebalance if needed
    bf = balance_factor(node)

    if bf > 1 and key < node.left.key:          # LL
        return rotate_right(node)
    if bf < -1 and key > node.right.key:        # RR
        return rotate_left(node)
    if bf > 1 and key > node.left.key:          # LR
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1 and key < node.right.key:        # RL
        node.right = rotate_right(node.right)
        return rotate_left(node)

    return node
```

**Time**: O(log n) — one descent, then at most O(log n) height updates and
**at most one rotation** (or one double rotation).

### Deletion

Same three phases, but two differences: use the in-order successor to replace
a two-child node, and decide the rotation case from the *child's* balance
factor rather than the inserted key.

```python
def avl_delete(node, key):
    if not node:
        return None

    if key < node.key:
        node.left = avl_delete(node.left, key)
    elif key > node.key:
        node.right = avl_delete(node.right, key)
    else:
        # Found it: 0 or 1 child is easy
        if not node.left:
            return node.right
        if not node.right:
            return node.left
        # 2 children: replace with in-order successor
        succ = node.right
        while succ.left:
            succ = succ.left
        node.key = succ.key
        node.right = avl_delete(node.right, succ.key)

    update_height(node)
    bf = balance_factor(node)

    if bf > 1 and balance_factor(node.left) >= 0:
        return rotate_right(node)
    if bf > 1:
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1 and balance_factor(node.right) <= 0:
        return rotate_left(node)
    if bf < -1:
        node.right = rotate_right(node.right)
        return rotate_left(node)

    return node
```

**Deletion may cascade**: unlike insertion, a delete can require O(log n)
rotations, one at each level back to the root.

---

## 3. Red-Black Trees

**Invariants**:
1. Every node is red or black.
2. The root is black.
3. Every leaf (NIL) is black.
4. A red node has no red child (no two reds in a row).
5. Every root→leaf path contains the same number of black nodes.

Property 5 is the balance guarantee; property 4 is what keeps it enforceable
with O(1) amortized restructuring.

```python
RED, BLACK = True, False

class RBNode:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = self.right = self.parent = None
```

### Insertion Fixup

A new node is inserted red (this cannot break property 5, only property 4).
Then fix the possible red-red violation:

```
Case 1: uncle is RED
  -> recolor parent and uncle BLACK, grandparent RED, recurse upward

Case 2: uncle is BLACK, new node is an "inner" child
  -> rotate to convert into Case 3

Case 3: uncle is BLACK, new node is an "outer" child
  -> rotate grandparent, swap parent/grandparent colors, done
```

Only Case 1 recurses, and it moves two levels up each time, so the fixup is
O(log n) with **O(1) amortized rotations**.

### AVL vs Red-Black

| | AVL | Red-Black |
|---|-----|-----------|
| Height bound | ≤ 1.44 log n | ≤ 2 log n |
| Balance | stricter | looser |
| Search | **faster** (shallower) | slightly slower |
| Insert/delete | more rotations | **fewer rotations** |
| Delete rotations | O(log n) | O(1) amortized |
| Memory per node | height (int) | color (1 bit) |
| Best for | read-heavy | write-heavy |

**Real-world**: Red-Black wins in practice for general-purpose containers
because writes are cheaper and the code is more uniform.

- **Red-Black**: Java `TreeMap`/`TreeSet`, C++ `std::map`/`std::set`,
  Linux kernel CFS scheduler, `epoll` internals
- **AVL**: in-memory database indexes, anywhere lookups dominate writes

Python's `dict` and `set` are hash tables, not trees — Python has no
built-in balanced BST. Use `sortedcontainers` (B-tree-like) when you need one.

---

## 4. Segment Trees

**Problem**: given an array, answer *range queries* (sum, min, max, gcd) and
*point updates*, both fast.

| Approach | Range query | Point update |
|----------|-------------|--------------|
| Plain array | O(n) | O(1) |
| Prefix sums | O(1) | **O(n)** |
| **Segment tree** | **O(log n)** | **O(log n)** |

A segment tree stores an aggregate for every contiguous range, arranged as a
binary tree over the array.

```
Array: [1, 3, 5, 7, 9, 11]   (sums)

                 36            [0..5]
               /    \
            9         27       [0..2] [3..5]
          /   \      /   \
         4     5   16    11    [0..1] [2..2] [3..4] [5..5]
        / \        /  \
       1   3      7    9
```

### Array-Based Implementation

```python
class SegmentTree:
    """Iterative, array-backed. tree[1] is the root; leaves live at [n, 2n)."""

    def __init__(self, data, combine=lambda a, b: a + b, identity=0):
        self.n = len(data)
        self.combine = combine
        self.identity = identity
        self.tree = [identity] * (2 * self.n)

        # Leaves
        for i, value in enumerate(data):
            self.tree[self.n + i] = value
        # Internal nodes, built bottom-up
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = combine(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        """Point update: set data[i] = value. O(log n)"""
        i += self.n
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, left, right):
        """Aggregate over [left, right). O(log n)"""
        result = self.identity
        left += self.n
        right += self.n
        while left < right:
            if left & 1:                 # left is a right child -> take it
                result = self.combine(result, self.tree[left])
                left += 1
            if right & 1:                # right is a right child -> take left sibling
                right -= 1
                result = self.combine(result, self.tree[right])
            left //= 2
            right //= 2
        return result
```

**The key insight**: any range decomposes into at most 2·log n precomputed
nodes. The iterative version walks up from both ends, grabbing siblings.

**Space**: O(n). **Build**: O(n). **Query/update**: O(log n).

### Generality

The same structure answers any **associative** operation by swapping
`combine` and `identity`:

```python
SegmentTree(data, lambda a, b: a + b,        0)              # range sum
SegmentTree(data, min,                       float('inf'))   # range min
SegmentTree(data, max,                       float('-inf'))  # range max
SegmentTree(data, math.gcd,                  0)              # range gcd
```

The operation must be associative. It need not be commutative, but a
non-commutative op (like matrix multiply) requires care about argument order.

### Lazy Propagation (Range Updates)

To support "add 5 to every element in [l, r]" in O(log n), defer the work:
store a pending delta at each node and push it down only when you descend.

```python
class LazySegmentTree:
    """Range-add, range-sum. Recursive, 1-indexed tree over [0, n)."""

    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, lo, hi):
        if lo == hi:
            self.tree[node] = data[lo]
            return
        mid = (lo + hi) // 2
        self._build(data, 2 * node, lo, mid)
        self._build(data, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node, lo, hi):
        """Apply this node's pending delta, then hand it to the children."""
        if self.lazy[node] == 0:
            return
        self.tree[node] += self.lazy[node] * (hi - lo + 1)
        if lo != hi:
            self.lazy[2 * node] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
        self.lazy[node] = 0

    def range_add(self, left, right, delta, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        self._push(node, lo, hi)
        if right < lo or hi < left:          # disjoint
            return
        if left <= lo and hi <= right:       # fully covered -> defer
            self.lazy[node] += delta
            self._push(node, lo, hi)
            return
        mid = (lo + hi) // 2
        self.range_add(left, right, delta, 2 * node, lo, mid)
        self.range_add(left, right, delta, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def range_sum(self, left, right, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        self._push(node, lo, hi)
        if right < lo or hi < left:
            return 0
        if left <= lo and hi <= right:
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self.range_sum(left, right, 2 * node, lo, mid) +
                self.range_sum(left, right, 2 * node + 1, mid + 1, hi))
```

**Without lazy propagation**, a range update is O(n log n) — you would update
each element individually. **With it**, O(log n).

---

## 5. Fenwick Tree (Binary Indexed Tree)

A Fenwick tree does prefix sums with point updates in O(log n), using **half
the space and far less code** than a segment tree. It is the right tool when
you only need prefix/range *sums*.

```python
class FenwickTree:
    """1-indexed internally. Uses i & -i to walk the implicit tree."""

    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        """Add delta at index i (0-indexed). O(log n)"""
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i            # move to the next node that covers i

    def prefix_sum(self, i):
        """Sum of data[0..i] inclusive. O(log n)"""
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i            # strip the lowest set bit
        return total

    def range_sum(self, left, right):
        """Sum of data[left..right] inclusive."""
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left else 0)
```

**How it works**: `tree[i]` stores the sum of a block of size `i & -i` ending
at `i`. That is the same lowest-set-bit trick from bit manipulation —
`i -= i & -i` jumps to the parent, `i += i & -i` to the next covering node.
Each jump clears or adds one bit, so both loops run O(log n) times.

### Segment Tree vs Fenwick Tree

| | Segment Tree | Fenwick Tree |
|---|--------------|--------------|
| Space | 2n–4n | **n** |
| Prefix/range sum | O(log n) | O(log n) |
| Point update | O(log n) | O(log n) |
| Range update | O(log n) (lazy) | O(log n) (two BITs) |
| Range min/max | **yes** | no (not invertible) |
| Arbitrary associative op | **yes** | sums only |
| Code size | ~40 lines | **~15 lines** |
| Constant factor | higher | **lower** |

**Rule**: sums only → Fenwick. Min, max, gcd, or anything needing lazy
propagation → segment tree.

---

## 6. B-Trees (Brief)

AVL and Red-Black trees assume memory access is uniform. On disk it is not —
one seek costs as much as thousands of comparisons. B-trees minimize *depth*
by making each node hold many keys.

```
A B-tree of order m:
  - each node holds up to m-1 keys and m children
  - all leaves are at the same depth
  - a node (except root) is at least half full

Height = O(log_m n), so m = 100 gives depth ~3 for a million keys.
```

- **B-tree**: keys and values in every node
- **B+ tree**: values only in leaves, leaves linked — better for range scans

**Real-world**: essentially every database index and filesystem — PostgreSQL,
MySQL InnoDB, SQLite, MongoDB, NTFS, ext4, HFS+.

---

## 7. Complexity Summary

| Structure | Search | Insert | Delete | Range query | Space |
|-----------|--------|--------|--------|-------------|-------|
| Plain BST (worst) | O(n) | O(n) | O(n) | O(n) | O(n) |
| Plain BST (avg) | O(log n) | O(log n) | O(log n) | O(k + log n) | O(n) |
| **AVL** | O(log n) | O(log n) | O(log n) | O(k + log n) | O(n) |
| **Red-Black** | O(log n) | O(log n) | O(log n) | O(k + log n) | O(n) |
| **Segment Tree** | O(log n) | O(log n) | — | **O(log n)** | O(n) |
| **Fenwick Tree** | — | O(log n) | — | **O(log n)** (sums) | **O(n)** |
| B-Tree | O(log n) | O(log n) | O(log n) | O(k + log n) | O(n) |
| Hash table | **O(1)** avg | **O(1)** avg | **O(1)** avg | **O(n)** | O(n) |

`k` = number of results returned.

Note the last row: a hash table beats every tree on single-key lookup. Trees
win when you need **order** — range queries, successor/predecessor, sorted
iteration, or min/max.

---

## 8. Choosing a Structure

```
Do you need keys in sorted order?
├── NO  -> hash table (dict / set). Stop here.
└── YES
    ├── Do you need range aggregates (sum/min/max over [l, r])?
    │   ├── YES, sums only, point updates -> Fenwick Tree
    │   ├── YES, min/max/gcd or range updates -> Segment Tree
    │   └── NO -> continue
    ├── Is the data on disk or very large?
    │   └── YES -> B-tree / B+ tree
    └── In-memory ordered map:
        ├── read-heavy  -> AVL (shallower, faster lookups)
        └── write-heavy -> Red-Black (fewer rotations)
```

---

## 9. Common Pitfalls

1. **Updating heights in the wrong order** during a rotation. Update the node
   that moved *down* first — its children are already correct.
2. **Forgetting to reassign the subtree root.** Rotations return a new root;
   `node.left = rotate_left(node.left)` is required. Dropping the assignment
   silently corrupts the tree.
3. **Deletion rebalancing differs from insertion.** Choose the case from the
   child's balance factor, not from a key comparison — there is no inserted
   key to compare.
4. **Segment tree off-by-one.** Decide once whether ranges are `[l, r)` or
   `[l, r]` and stay consistent. Mixing them is the #1 bug.
5. **Non-associative combine.** Segment trees require associativity. "Average"
   is not associative — store (sum, count) instead.
6. **Fenwick trees are 1-indexed internally.** `i & -i` on index 0 is 0, so
   the update loop would never advance. Always shift by one.
7. **Forgetting `_push` before reading** a lazy segment tree node. The stored
   aggregate is stale until pending deltas are applied.
8. **Recursion depth.** A recursive segment tree on n = 10⁶ nests ~20 deep —
   fine. But recursive AVL operations on adversarial input can approach
   Python's default 1000-frame limit; iterative is safer for huge trees.

---

## 10. Key Takeaways

✅ **A plain BST degenerates to O(n)** on sorted input — balance is not optional
✅ **AVL**: `|bf| ≤ 1`, four rotation cases, ≤ 1.44 log n tall, read-optimized
✅ **Red-Black**: equal black-heights, ≤ 2 log n tall, write-optimized, what
   real libraries ship
✅ **Rotations are O(1)** and preserve BST order — that is the whole mechanism
✅ **Cache the height** on each AVL node; recomputing defeats the purpose
✅ **Segment Tree**: any associative range query in O(log n), lazy propagation
   for range updates
✅ **Fenwick Tree**: prefix sums in 15 lines and O(n) space via `i & -i`
✅ **B-Trees**: high fan-out to minimize disk seeks — every database index
✅ **Hash tables beat trees** for pure lookup; use a tree when order matters

**Interview Focus**:
- Draw the rotation. Do not try to explain LR from memory without a diagram.
- Know *why* insertion needs ≤ 1 rotation but deletion may need O(log n).
- Recognize "range query + updates" as a segment tree / Fenwick problem.
- Justify AVL vs Red-Black by read/write ratio, not by "AVL is better."
- State what a hash table would cost, and why order rules it out.

Next: Implement AVL rotations, then segment trees, then measure the
difference against an unbalanced BST!
