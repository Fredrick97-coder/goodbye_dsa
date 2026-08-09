"""
Examples: Advanced Trees

Demonstrate AVL trees, Red-Black trees, Segment Trees, and Fenwick Trees.
"""

import math
import random
import time
from typing import List, Optional, Callable

print("=" * 70)
print("ADVANCED TREES")
print("=" * 70)

# ==================== (1) Why Plain BSTs Fail ====================
print("\n[1] Why a Plain BST Is Not Enough")
print("-" * 70)

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class PlainBST:
    """No balancing. Degenerates on sorted input."""

    def __init__(self):
        self.root = None
        self.comparisons = 0

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key) -> bool:
        self.comparisons = 0
        node = self.root
        while node:
            self.comparisons += 1
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def height(self) -> int:
        def h(node):
            return 1 + max(h(node.left), h(node.right)) if node else 0
        return h(self.root)


print("Inserting 1..15 in SORTED order into a plain BST:")
sorted_bst = PlainBST()
for i in range(1, 16):
    sorted_bst.insert(i)

print(f"  Items       : 15")
print(f"  Height      : {sorted_bst.height()}   (ideal would be 4)")
sorted_bst.search(15)
print(f"  Comparisons to find 15: {sorted_bst.comparisons}")
print("  -> The tree is a linked list. Search is O(n).")

print("\nInserting the SAME 15 items in RANDOM order:")
random.seed(42)
shuffled = list(range(1, 16))
random.shuffle(shuffled)
random_bst = PlainBST()
for i in shuffled:
    random_bst.insert(i)

print(f"  Insert order: {shuffled}")
print(f"  Height      : {random_bst.height()}")
random_bst.search(15)
print(f"  Comparisons to find 15: {random_bst.comparisons}")
print("  -> Random order happens to balance. But you cannot rely on luck.")

print("\n-> Sorted input is COMMON (timestamps, IDs, imports)")
print("-> We need a structure that guarantees balance")

# ==================== (2) AVL Rotations ====================
print("\n[2] AVL Rotations (the O(1) Rebalancing Primitive)")
print("-" * 70)

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1        # cached so balance checks are O(1)


def height(node: Optional[AVLNode]) -> int:
    return node.height if node else 0

def balance_factor(node: Optional[AVLNode]) -> int:
    return height(node.left) - height(node.right) if node else 0

def update_height(node: AVLNode) -> None:
    node.height = 1 + max(height(node.left), height(node.right))

def rotate_right(z: AVLNode) -> AVLNode:
    """z's left child becomes the new subtree root."""
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)       # z moved DOWN, fix it first
    update_height(y)
    return y

def rotate_left(z: AVLNode) -> AVLNode:
    """z's right child becomes the new subtree root."""
    y = z.right
    z.right = y.left
    y.left = z
    update_height(z)
    update_height(y)
    return y


def show_tree(node: Optional[AVLNode], prefix: str = "", is_left: bool = True) -> None:
    """Print a tree sideways, with balance factors."""
    if not node:
        return
    show_tree(node.right, prefix + ("│   " if is_left else "    "), False)
    bf = balance_factor(node)
    flag = "  <-- UNBALANCED" if abs(bf) > 1 else ""
    print(f"{prefix}{'└── ' if is_left else '┌── '}{node.key} "
          f"(h={node.height}, bf={bf:+d}){flag}")
    show_tree(node.left, prefix + ("    " if is_left else "│   "), True)


print("Case LL: insert 30, 20, 10 (left-left chain)")
root = AVLNode(30)
root.left = AVLNode(20)
root.left.left = AVLNode(10)
update_height(root.left)
update_height(root)
print("\nBefore (bf of root = +2, violates |bf| <= 1):")
show_tree(root)

root = rotate_right(root)
print("\nAfter rotate_right(30):")
show_tree(root)
print("-> Height dropped from 3 to 2. One O(1) rotation fixed it.")

print("\n\nCase LR: insert 30, 10, 20 (left-right zigzag)")
root = AVLNode(30)
root.left = AVLNode(10)
root.left.right = AVLNode(20)
update_height(root.left)
update_height(root)
print("\nBefore:")
show_tree(root)

root.left = rotate_left(root.left)
print("\nAfter step 1 -- rotate_left(10) turns LR into LL:")
show_tree(root)

root = rotate_right(root)
print("\nAfter step 2 -- rotate_right(30):")
show_tree(root)
print("-> LR needs TWO rotations. The first converts it to the LL shape.")

# ==================== (3) Full AVL Tree ====================
print("\n[3] Complete AVL Tree (Insert, Delete, Search)")
print("-" * 70)

class AVLTree:
    """Self-balancing BST. All operations O(log n) worst case."""

    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.rotations = 0
        self.comparisons = 0

    # ---------- insert ----------
    def insert(self, key) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[AVLNode], key) -> AVLNode:
        # 1. Standard BST insert
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node                      # duplicate: ignore

        # 2. Fix cached height on the way back up
        update_height(node)

        # 3. Rebalance
        bf = balance_factor(node)

        if bf > 1 and key < node.left.key:            # LL
            self.rotations += 1
            return rotate_right(node)
        if bf < -1 and key > node.right.key:          # RR
            self.rotations += 1
            return rotate_left(node)
        if bf > 1 and key > node.left.key:            # LR
            self.rotations += 2
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if bf < -1 and key < node.right.key:          # RL
            self.rotations += 2
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    # ---------- delete ----------
    def delete(self, key) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[AVLNode], key) -> Optional[AVLNode]:
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Two children: swap in the in-order successor
            succ = node.right
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)

        update_height(node)
        bf = balance_factor(node)

        # Case chosen from the CHILD's balance factor, not a key comparison
        if bf > 1 and balance_factor(node.left) >= 0:
            self.rotations += 1
            return rotate_right(node)
        if bf > 1:
            self.rotations += 2
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if bf < -1 and balance_factor(node.right) <= 0:
            self.rotations += 1
            return rotate_left(node)
        if bf < -1:
            self.rotations += 2
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    # ---------- queries ----------
    def search(self, key) -> bool:
        self.comparisons = 0
        node = self.root
        while node:
            self.comparisons += 1
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def height(self) -> int:
        return height(self.root)

    def inorder(self) -> List:
        result = []
        def walk(node):
            if node:
                walk(node.left)
                result.append(node.key)
                walk(node.right)
        walk(self.root)
        return result

    def is_balanced(self) -> bool:
        """Verify the AVL invariant everywhere."""
        def check(node):
            if not node:
                return True
            return (abs(balance_factor(node)) <= 1
                    and check(node.left) and check(node.right))
        return check(self.root)


print("Inserting 1..15 in SORTED order into an AVL tree:")
avl = AVLTree()
for i in range(1, 16):
    avl.insert(i)

print(f"  Items         : 15")
print(f"  Height        : {avl.height()}   (perfectly balanced!)")
print(f"  Rotations used: {avl.rotations}")
print(f"  Invariant ok  : {avl.is_balanced()}")
avl.search(15)
print(f"  Comparisons to find 15: {avl.comparisons}")

print("\nResulting structure:")
show_tree(avl.root)

print(f"\nIn-order traversal (must be sorted): {avl.inorder()}")

print("\nDeleting 8 (the root) and 4:")
avl.delete(8)
avl.delete(4)
print(f"  Height       : {avl.height()}")
print(f"  Invariant ok : {avl.is_balanced()}")
print(f"  In-order     : {avl.inorder()}")

print("\nHead-to-head, both fed 1..15 in sorted order:")
fresh_avl = AVLTree()
for i in range(1, 16):
    fresh_avl.insert(i)
fresh_avl.search(15)
avl_cmp_count = fresh_avl.comparisons
sorted_bst.search(15)

print(f"  {'Structure':<14} {'Height':>8} {'Cmp for max':>13}")
print("  " + "-" * 38)
print(f"  {'Plain BST':<14} {sorted_bst.height():>8} {sorted_bst.comparisons:>13}")
print(f"  {'AVL Tree':<14} {fresh_avl.height():>8} {avl_cmp_count:>13}")
print("  -> AVL height is logarithmic, BST height is linear")

# ==================== (4) AVL vs BST Benchmark ====================
print("\n[4] AVL vs Plain BST: Measured Impact")
print("-" * 70)

SIZE = 3000
print(f"Inserting {SIZE:,} SORTED keys, then searching all of them.\n")

# Plain BST -- must raise the recursion limit; a degenerate tree recurses n deep
import sys
old_limit = sys.getrecursionlimit()
sys.setrecursionlimit(SIZE * 3)

bst = PlainBST()
start = time.perf_counter()
for i in range(SIZE):
    bst.insert(i)
bst_insert_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for i in range(SIZE):
    bst.search(i)
bst_search_ms = (time.perf_counter() - start) * 1000
bst_height = bst.height()

sys.setrecursionlimit(old_limit)

avl2 = AVLTree()
start = time.perf_counter()
for i in range(SIZE):
    avl2.insert(i)
avl_insert_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for i in range(SIZE):
    avl2.search(i)
avl_search_ms = (time.perf_counter() - start) * 1000

print(f"{'Structure':<14} {'Height':>8} {'Insert':>12} {'Search all':>13}")
print("-" * 52)
print(f"{'Plain BST':<14} {bst_height:>8} {bst_insert_ms:>10.1f}ms {bst_search_ms:>11.1f}ms")
print(f"{'AVL Tree':<14} {avl2.height():>8} {avl_insert_ms:>10.1f}ms {avl_search_ms:>11.1f}ms")

print(f"\nHeight reduction : {bst_height} -> {avl2.height()} "
      f"({bst_height / avl2.height():.0f}x shallower)")
print(f"Search speedup   : {bst_search_ms / avl_search_ms:.1f}x faster")
print(f"Insert speedup   : {bst_insert_ms / avl_insert_ms:.1f}x faster "
      f"({avl2.rotations:,} rotations)")
print(f"Theoretical bound: 1.44 * log2({SIZE}) = "
      f"{1.44 * math.log2(SIZE):.1f}, actual = {avl2.height()}")

print("\n-> AVL won on BOTH insert and search here. On sorted input the plain")
print("   BST costs O(n) per insert (O(n^2) total), so rebalancing is not")
print("   overhead -- it is what makes the inserts cheap in the first place.")
print("-> On RANDOM input the plain BST would insert slightly faster, since")
print("   it stays roughly balanced by luck and skips the rotation work.")

# ==================== (5) Red-Black Tree ====================
print("\n[5] Red-Black Tree (What Real Libraries Ship)")
print("-" * 70)

RED, BLACK = True, False

class RBNode:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left: Optional["RBNode"] = None
        self.right: Optional["RBNode"] = None
        self.parent: Optional["RBNode"] = None


class RedBlackTree:
    """
    Invariants:
      1. Every node is red or black
      2. Root is black
      3. NIL leaves are black
      4. A red node has no red child
      5. Every root->leaf path has the same black count
    """

    def __init__(self):
        self.root: Optional[RBNode] = None
        self.rotations = 0

    def _rotate_left(self, x: RBNode) -> None:
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.rotations += 1

    def _rotate_right(self, x: RBNode) -> None:
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self.rotations += 1

    def insert(self, key) -> None:
        # Standard BST insert, new node is RED
        node = RBNode(key)
        parent = None
        cur = self.root
        while cur:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return                       # duplicate
        node.parent = parent
        if not parent:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self._fix_insert(node)

    def _fix_insert(self, node: RBNode) -> None:
        """Repair the possible red-red violation (property 4)."""
        while node.parent and node.parent.color == RED:
            parent = node.parent
            grand = parent.parent
            if not grand:
                break

            if parent is grand.left:
                uncle = grand.right
                if uncle and uncle.color == RED:
                    # Case 1: recolor and move up two levels
                    parent.color = BLACK
                    uncle.color = BLACK
                    grand.color = RED
                    node = grand
                else:
                    if node is parent.right:
                        # Case 2: inner child -> rotate into Case 3
                        node = parent
                        self._rotate_left(node)
                        parent = node.parent
                    # Case 3: outer child
                    parent.color = BLACK
                    grand.color = RED
                    self._rotate_right(grand)
            else:
                uncle = grand.left
                if uncle and uncle.color == RED:
                    parent.color = BLACK
                    uncle.color = BLACK
                    grand.color = RED
                    node = grand
                else:
                    if node is parent.left:
                        node = parent
                        self._rotate_right(node)
                        parent = node.parent
                    parent.color = BLACK
                    grand.color = RED
                    self._rotate_left(grand)

        self.root.color = BLACK              # property 2

    def search(self, key) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def height(self) -> int:
        def h(node):
            return 1 + max(h(node.left), h(node.right)) if node else 0
        return h(self.root)

    def black_height(self) -> int:
        """Black nodes from root to any leaf (property 5 means it is unique)."""
        count = 0
        node = self.root
        while node:
            if node.color == BLACK:
                count += 1
            node = node.left
        return count + 1                     # +1 for the NIL leaf

    def inorder(self) -> List:
        result = []
        def walk(node):
            if node:
                walk(node.left)
                result.append(node.key)
                walk(node.right)
        walk(self.root)
        return result

    def validate(self) -> bool:
        """Check properties 2, 4, and 5."""
        if self.root and self.root.color == RED:
            return False

        def check(node) -> int:
            """Return black-height, or -1 if invalid."""
            if not node:
                return 1
            if node.color == RED:
                if ((node.left and node.left.color == RED) or
                        (node.right and node.right.color == RED)):
                    return -1                # property 4 violated
            left = check(node.left)
            right = check(node.right)
            if left == -1 or right == -1 or left != right:
                return -1                    # property 5 violated
            return left + (1 if node.color == BLACK else 0)

        return check(self.root) != -1


print("Inserting 1..15 in SORTED order into a Red-Black tree:")
rb = RedBlackTree()
for i in range(1, 16):
    rb.insert(i)

print(f"  Items         : 15")
print(f"  Height        : {rb.height()}")
print(f"  Black height  : {rb.black_height()}")
print(f"  Rotations used: {rb.rotations}")
print(f"  Valid RB tree : {rb.validate()}")
print(f"  In-order      : {rb.inorder()}")

print("\nStructure (R = red, B = black):")
def show_rb(node, prefix="", is_left=True):
    if not node:
        return
    show_rb(node.right, prefix + ("│   " if is_left else "    "), False)
    color = "R" if node.color == RED else "B"
    print(f"{prefix}{'└── ' if is_left else '┌── '}{node.key}({color})")
    show_rb(node.left, prefix + ("    " if is_left else "│   "), True)

show_rb(rb.root)

# AVL vs RB rotation count on the same workload
print("\n\nAVL vs Red-Black on identical sorted input:")
SIZE_CMP = 2000
avl_cmp = AVLTree()
for i in range(SIZE_CMP):
    avl_cmp.insert(i)
rb_cmp = RedBlackTree()
for i in range(SIZE_CMP):
    rb_cmp.insert(i)

print(f"  {'':<16} {'Height':>8} {'Rotations':>11} {'log2(n)':>9}")
print("  " + "-" * 48)
print(f"  {'AVL':<16} {avl_cmp.height():>8} {avl_cmp.rotations:>11,} "
      f"{math.log2(SIZE_CMP):>9.1f}")
print(f"  {'Red-Black':<16} {rb_cmp.height():>8} {rb_cmp.rotations:>11,} "
      f"{math.log2(SIZE_CMP):>9.1f}")
print(f"  AVL bound  : 1.44 * log2(n) = {1.44 * math.log2(SIZE_CMP):.1f}")
print(f"  RB bound   : 2.00 * log2(n) = {2.0 * math.log2(SIZE_CMP):.1f}")
print("  -> AVL is shallower (faster reads); RB rotates less (faster writes)")
print("  -> Java TreeMap, C++ std::map, and the Linux scheduler all use RB")

# ==================== (6) Segment Tree ====================
print("\n[6] Segment Tree (Any Associative Range Query)")
print("-" * 70)

class SegmentTree:
    """Iterative, array-backed. tree[1] is root; leaves at [n, 2n)."""

    def __init__(self, data: List, combine: Callable = None, identity=0):
        self.n = len(data)
        self.combine = combine or (lambda a, b: a + b)
        self.identity = identity
        self.tree = [identity] * (2 * self.n)

        for i, value in enumerate(data):
            self.tree[self.n + i] = value
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i: int, value) -> None:
        """Point update. O(log n)"""
        i += self.n
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, left: int, right: int):
        """Aggregate over [left, right). O(log n)"""
        result = self.identity
        left += self.n
        right += self.n
        while left < right:
            if left & 1:
                result = self.combine(result, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                result = self.combine(result, self.tree[right])
            left //= 2
            right //= 2
        return result


data = [1, 3, 5, 7, 9, 11]
print(f"Array: {data}\n")

seg_sum = SegmentTree(data, lambda a, b: a + b, 0)
print("Range SUM queries on [left, right):")
for l, r in [(0, 6), (1, 4), (2, 5), (0, 3), (3, 6)]:
    expected = sum(data[l:r])
    got = seg_sum.query(l, r)
    print(f"  query({l}, {r}) = {got:>3}   (verify: {expected:>3})  "
          f"{'ok' if got == expected else 'MISMATCH'}")

print("\nPoint update: data[2] = 5 -> 100")
seg_sum.update(2, 100)
data[2] = 100
print(f"  Array now: {data}")
for l, r in [(0, 6), (2, 5), (0, 2)]:
    print(f"  query({l}, {r}) = {seg_sum.query(l, r):>4}   "
          f"(verify: {sum(data[l:r]):>4})")

print("\nSame structure, different operation -- just swap combine + identity:")
data2 = [5, 2, 8, 1, 9, 3]
print(f"  Array: {data2}")

seg_min = SegmentTree(data2, min, float("inf"))
seg_max = SegmentTree(data2, max, float("-inf"))
seg_gcd = SegmentTree([12, 18, 24, 6, 30, 15], math.gcd, 0)

print(f"\n  {'Range':<10} {'MIN':>6} {'MAX':>6}")
print("  " + "-" * 24)
for l, r in [(0, 6), (1, 4), (2, 5), (3, 6)]:
    print(f"  [{l}, {r}){'':<4} {seg_min.query(l, r):>6} {seg_max.query(l, r):>6}")

print(f"\n  GCD over [12, 18, 24, 6, 30, 15]:")
for l, r in [(0, 3), (0, 6), (2, 5)]:
    print(f"    query({l}, {r}) = {seg_gcd.query(l, r)}")

print("\n-> Build O(n), query O(log n), update O(log n), space O(n)")
print("-> Works for ANY associative operation")

# ==================== (7) Lazy Propagation ====================
print("\n[7] Lazy Propagation (Range Updates in O(log n))")
print("-" * 70)

class LazySegmentTree:
    """Range-add, range-sum. Defers updates until a descent forces them."""

    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)
        self.pushes = 0

    def _build(self, data, node, lo, hi):
        if lo == hi:
            self.tree[node] = data[lo]
            return
        mid = (lo + hi) // 2
        self._build(data, 2 * node, lo, mid)
        self._build(data, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node, lo, hi):
        """Apply the pending delta here, then hand it down."""
        if self.lazy[node] == 0:
            return
        self.tree[node] += self.lazy[node] * (hi - lo + 1)
        if lo != hi:
            self.lazy[2 * node] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
        self.lazy[node] = 0

    def range_add(self, left, right, delta, node=1, lo=0, hi=None):
        """Add delta to every element in [left, right]. O(log n)"""
        if hi is None:
            hi = self.n - 1
        self._push(node, lo, hi)
        if right < lo or hi < left:
            return
        if left <= lo and hi <= right:
            self.lazy[node] += delta
            self._push(node, lo, hi)
            return
        mid = (lo + hi) // 2
        self.range_add(left, right, delta, 2 * node, lo, mid)
        self.range_add(left, right, delta, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def range_sum(self, left, right, node=1, lo=0, hi=None):
        """Sum over [left, right]. O(log n)"""
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


values = [1, 2, 3, 4, 5, 6, 7, 8]
lazy = LazySegmentTree(values)
plain = list(values)

print(f"Array: {values}")
print(f"Initial sum [0, 7] = {lazy.range_sum(0, 7)}  (verify: {sum(plain)})")

print("\nrange_add(2, 5, +10)  -- add 10 to indices 2..5:")
lazy.range_add(2, 5, 10)
for i in range(2, 6):
    plain[i] += 10
print(f"  Conceptual array: {plain}")
print(f"  sum [0, 7] = {lazy.range_sum(0, 7):>3}  (verify: {sum(plain):>3})")
print(f"  sum [2, 5] = {lazy.range_sum(2, 5):>3}  (verify: {sum(plain[2:6]):>3})")
print(f"  sum [0, 1] = {lazy.range_sum(0, 1):>3}  (verify: {sum(plain[0:2]):>3})")

print("\nrange_add(0, 3, -5)  -- overlapping update:")
lazy.range_add(0, 3, -5)
for i in range(0, 4):
    plain[i] -= 5
print(f"  Conceptual array: {plain}")
for l, r in [(0, 7), (0, 3), (2, 5), (4, 6)]:
    got = lazy.range_sum(l, r)
    exp = sum(plain[l:r + 1])
    print(f"  sum [{l}, {r}] = {got:>3}  (verify: {exp:>3})  "
          f"{'ok' if got == exp else 'MISMATCH'}")

# Show the cost difference
N_LAZY = 4000
UPDATES = 400
print(f"\nCost of {UPDATES} range updates on {N_LAZY:,} elements:")

big = list(range(N_LAZY))
lazy_tree = LazySegmentTree(big)
start = time.perf_counter()
for k in range(UPDATES):
    lazy_tree.range_add(0, N_LAZY - 1, 1)
lazy_ms = (time.perf_counter() - start) * 1000

naive_tree = SegmentTree(list(big))
start = time.perf_counter()
for k in range(5):                        # only 5 -- the full 400 is too slow
    for i in range(N_LAZY):
        naive_tree.update(i, naive_tree.tree[naive_tree.n + i] + 1)
naive_5_ms = (time.perf_counter() - start) * 1000
naive_projected = naive_5_ms / 5 * UPDATES

print(f"  Lazy propagation      : {lazy_ms:>10.1f}ms  (O(log n) per update)")
print(f"  Point-by-point (x5)   : {naive_5_ms:>10.1f}ms")
print(f"  Point-by-point (x{UPDATES}, projected): {naive_projected:>10.1f}ms"
      f"  (O(n log n) per update)")
print(f"  -> Lazy is ~{naive_projected / lazy_ms:.0f}x faster")

print("\n  Caveat: these updates span the WHOLE array, which is lazy")
print("  propagation's best case -- each one stops at the root. Partial")
print("  ranges cost more (a real O(log n) descent), so treat this number")
print("  as the upper bound on the win, not the typical one.")

# Same comparison with partial ranges, for an honest middle case
lazy_partial = LazySegmentTree(list(big))
random.seed(11)
spans = [(random.randrange(N_LAZY // 2), random.randrange(N_LAZY // 2, N_LAZY))
         for _ in range(UPDATES)]
start = time.perf_counter()
for l, r in spans:
    lazy_partial.range_add(l, r, 1)
lazy_partial_ms = (time.perf_counter() - start) * 1000

print(f"\n  Lazy, {UPDATES} PARTIAL ranges : {lazy_partial_ms:>8.1f}ms"
      f"  (still ~{naive_projected / lazy_partial_ms:.0f}x faster)")

print("\n-> Without lazy propagation, a range update is O(n log n)")

# ==================== (8) Fenwick Tree ====================
print("\n[8] Fenwick Tree / BIT (Prefix Sums in 15 Lines)")
print("-" * 70)

class FenwickTree:
    """Prefix sums with point updates. Uses i & -i from bit manipulation."""

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)      # 1-indexed internally

    @classmethod
    def from_list(cls, data: List[int]) -> "FenwickTree":
        ft = cls(len(data))
        for i, v in enumerate(data):
            ft.update(i, v)
        return ft

    def update(self, i: int, delta: int) -> None:
        """Add delta at index i (0-indexed). O(log n)"""
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i                # jump to the next covering node

    def prefix_sum(self, i: int) -> int:
        """Sum of data[0..i] inclusive. O(log n)"""
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i                # strip the lowest set bit
        return total

    def range_sum(self, left: int, right: int) -> int:
        """Sum of data[left..right] inclusive."""
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left else 0)


fdata = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
ft = FenwickTree.from_list(fdata)

print(f"Array: {fdata}\n")
print(f"{'Query':<22} {'Result':>8} {'Verify':>8}")
print("-" * 40)
for i in [0, 4, 7, 10]:
    print(f"prefix_sum(0..{i}){'':<6} {ft.prefix_sum(i):>8} {sum(fdata[:i+1]):>8}")
for l, r in [(2, 5), (3, 8), (0, 10), (7, 7)]:
    print(f"range_sum({l}, {r}){'':<9} {ft.range_sum(l, r):>8} "
          f"{sum(fdata[l:r+1]):>8}")

print("\nPoint update: add +10 at index 3")
ft.update(3, 10)
fdata[3] += 10
print(f"  Array now: {fdata}")
print(f"  range_sum(2, 5) = {ft.range_sum(2, 5)}  (verify: {sum(fdata[2:6])})")

print("\nThe i & -i mechanism (why the loops are O(log n)):")
print(f"  {'i':>4}  {'binary':>8}  {'i & -i':>7}  covers")
print("  " + "-" * 40)
for i in [1, 2, 3, 4, 6, 8, 12, 16]:
    print(f"  {i:>4}  {i:>8b}  {i & -i:>7}  {i & -i} element(s) ending at {i}")

print("\nFenwick vs Segment Tree on the same workload:")
N_CMP = 20_000
OPS = 20_000
base = [random.randint(1, 100) for _ in range(N_CMP)]

start = time.perf_counter()
ft_bench = FenwickTree.from_list(base)
ft_build_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
seg_bench = SegmentTree(list(base), lambda a, b: a + b, 0)
seg_build_ms = (time.perf_counter() - start) * 1000

random.seed(7)
queries = [(random.randint(0, N_CMP - 2), random.randint(0, N_CMP - 1))
           for _ in range(OPS)]
queries = [(min(a, b), max(a, b)) for a, b in queries]

start = time.perf_counter()
for l, r in queries:
    ft_bench.range_sum(l, r)
ft_query_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for l, r in queries:
    seg_bench.query(l, r + 1)
seg_query_ms = (time.perf_counter() - start) * 1000

print(f"  {'':<16} {'Build':>11} {'20k queries':>14} {'Space':>10}")
print("  " + "-" * 55)
print(f"  {'Fenwick Tree':<16} {ft_build_ms:>9.1f}ms {ft_query_ms:>12.1f}ms "
      f"{N_CMP + 1:>9,}")
print(f"  {'Segment Tree':<16} {seg_build_ms:>9.1f}ms {seg_query_ms:>12.1f}ms "
      f"{2 * N_CMP:>9,}")

# Verify they agree
mismatches = sum(1 for l, r in queries[:500]
                 if ft_bench.range_sum(l, r) != seg_bench.query(l, r + 1))
print(f"\n  Results agree on 500 sampled queries: {mismatches == 0}")
print(f"  -> Fenwick: half the space, less code, sums only")
print(f"  -> Segment tree: any associative op, plus lazy range updates")

# ==================== (9) Structure Selection ====================
print("\n[9] Choosing the Right Structure")
print("-" * 70)

structures = [
    ("Hash table (dict)", "O(1)*", "O(1)*", "O(n)", "no", "pure key lookup"),
    ("Plain BST", "O(n)", "O(n)", "O(n)", "yes", "never (use balanced)"),
    ("AVL Tree", "O(log n)", "O(log n)", "O(k+log n)", "yes", "read-heavy ordered map"),
    ("Red-Black Tree", "O(log n)", "O(log n)", "O(k+log n)", "yes", "write-heavy ordered map"),
    ("Segment Tree", "O(log n)", "O(log n)", "O(log n)", "n/a", "range min/max/gcd, lazy"),
    ("Fenwick Tree", "-", "O(log n)", "O(log n)", "n/a", "prefix/range sums"),
    ("B+ Tree", "O(log n)", "O(log n)", "O(k+log n)", "yes", "disk-backed indexes"),
]

print(f"{'Structure':<19} {'Search':>10} {'Insert':>10} {'Range':>12} "
      f"{'Ord':>5}  Best for")
print("-" * 95)
for name, search, insert, rng, ordered, best in structures:
    print(f"{name:<19} {search:>10} {insert:>10} {rng:>12} {ordered:>5}  {best}")

print("\n* amortized average; worst case O(n)")

print("""
Decision path:

  Need sorted order?
  ├── NO  -> dict / set. Done. Nothing beats O(1).
  └── YES
      ├── Need range aggregates over [l, r]?
      │   ├── sums only, point updates -> Fenwick Tree
      │   └── min/max/gcd or range updates -> Segment Tree
      ├── Data on disk / very large -> B+ Tree
      └── In-memory ordered map:
          ├── read-heavy  -> AVL
          └── write-heavy -> Red-Black
""")

print("Python note: dict and set are hash tables. There is no built-in")
print("balanced BST -- use the `sortedcontainers` package when you need one.")

# ==================== (10) Verification Suite ====================
print("\n[10] Invariant Verification Under Random Workloads")
print("-" * 70)

random.seed(123)

print("Running 1,000 random inserts + 300 random deletes on the AVL tree,")
print("checking the |bf| <= 1 invariant and sortedness after every batch.\n")

verify_avl = AVLTree()
keys = random.sample(range(10_000), 1000)
for k in keys:
    verify_avl.insert(k)

balanced_after_insert = verify_avl.is_balanced()
sorted_after_insert = verify_avl.inorder() == sorted(keys)

to_delete = random.sample(keys, 300)
for k in to_delete:
    verify_avl.delete(k)

remaining = sorted(set(keys) - set(to_delete))
balanced_after_delete = verify_avl.is_balanced()
sorted_after_delete = verify_avl.inorder() == remaining

print(f"  {'Check':<38} {'Result':>8}")
print("  " + "-" * 48)
print(f"  {'AVL balanced after 1000 inserts':<38} {str(balanced_after_insert):>8}")
print(f"  {'AVL sorted after 1000 inserts':<38} {str(sorted_after_insert):>8}")
print(f"  {'AVL balanced after 300 deletes':<38} {str(balanced_after_delete):>8}")
print(f"  {'AVL sorted after 300 deletes':<38} {str(sorted_after_delete):>8}")
print(f"  {'AVL height (n=700)':<38} {verify_avl.height():>8}")
print(f"  {'AVL bound 1.44*log2(700)':<38} {1.44 * math.log2(700):>8.1f}")

verify_rb = RedBlackTree()
rb_keys = random.sample(range(10_000), 1000)
for k in rb_keys:
    verify_rb.insert(k)

print(f"\n  {'RB tree valid after 1000 inserts':<38} {str(verify_rb.validate()):>8}")
print(f"  {'RB sorted after 1000 inserts':<38} "
      f"{str(verify_rb.inorder() == sorted(rb_keys)):>8}")
print(f"  {'RB height (n=1000)':<38} {verify_rb.height():>8}")
print(f"  {'RB bound 2.00*log2(1000)':<38} {2.0 * math.log2(1000):>8.1f}")

# Segment tree vs brute force on random ops
print("\n  Segment tree cross-checked against brute force:")
arr = [random.randint(-50, 50) for _ in range(200)]
st = SegmentTree(list(arr), lambda a, b: a + b, 0)
seg_ok = True
for _ in range(500):
    if random.random() < 0.3:
        idx = random.randrange(200)
        val = random.randint(-50, 50)
        arr[idx] = val
        st.update(idx, val)
    else:
        l = random.randrange(200)
        r = random.randint(l + 1, 200)
        if st.query(l, r) != sum(arr[l:r]):
            seg_ok = False
            break

print(f"  {'500 mixed query/update ops match':<38} {str(seg_ok):>8}")

ft_arr = [random.randint(-50, 50) for _ in range(200)]
ftv = FenwickTree.from_list(ft_arr)
ft_ok = True
for _ in range(500):
    if random.random() < 0.3:
        idx = random.randrange(200)
        delta = random.randint(-20, 20)
        ft_arr[idx] += delta
        ftv.update(idx, delta)
    else:
        l = random.randrange(200)
        r = random.randint(l, 199)
        if ftv.range_sum(l, r) != sum(ft_arr[l:r + 1]):
            ft_ok = False
            break

print(f"  {'Fenwick: 500 mixed ops match':<38} {str(ft_ok):>8}")

print("\n-> All four structures verified against brute-force references")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
