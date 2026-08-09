"""
Exercises: Advanced Trees

Practice AVL rotations, Red-Black invariants, Segment Trees, and Fenwick Trees.
"""

from typing import List, Optional, Callable, Tuple

print("=" * 70)
print("EXERCISES: Advanced Trees")
print("=" * 70)


class AVLNode:
    """Provided for you. Note the cached `height` field."""
    def __init__(self, key):
        self.key = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1


# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. NODE HEIGHT AND BALANCE FACTOR")
print("Input: An AVLNode (or None)")
print("Output: Cached height, and balance factor = h(left) - h(right)")
print("Example: leaf node -> height 1, bf 0")
def height(node: Optional[AVLNode]) -> int:
    # TODO: Return the CACHED height. None has height 0.
    # Do not recompute recursively -- that defeats the whole point.
    pass

def balance_factor(node: Optional[AVLNode]) -> int:
    # TODO: height(left) - height(right). None has balance factor 0.
    pass

def update_height(node: AVLNode) -> None:
    # TODO: Recompute this node's cached height from its children:
    # 1 + max(height of children)
    pass

print("\n2. SINGLE ROTATIONS")
print("Input: The unbalanced subtree root z")
print("Output: The new subtree root after rotating")
print("Example: rotate_right on 30 -> 20 -> 10 gives 20 as root")
def rotate_right(z: AVLNode) -> AVLNode:
    # TODO: y = z.left. Move y.right to z.left, then z becomes y.right.
    # Update heights -- z FIRST (it moved down), then y. Return y.
    pass

def rotate_left(z: AVLNode) -> AVLNode:
    # TODO: Mirror image of rotate_right. y = z.right.
    pass

print("\n3. VALIDATE THE AVL INVARIANT")
print("Input: Root of a tree")
print("Output: True if |balance_factor| <= 1 at EVERY node")
print("Example: a 3-node left chain -> False")
def is_avl_balanced(root: Optional[AVLNode]) -> bool:
    # TODO: Recurse. A tree is AVL-balanced when this node satisfies
    # |bf| <= 1 AND both subtrees are themselves balanced.
    pass

print("\n4. IDENTIFY THE ROTATION CASE")
print("Input: An unbalanced node")
print("Output: One of 'LL', 'LR', 'RR', 'RL', or 'BALANCED'")
print("Example: bf=+2 with left child bf=-1 -> 'LR'")
def rotation_case(node: AVLNode) -> str:
    # TODO: bf > 1 means left-heavy -- then check the LEFT child's bf:
    #   left child bf >= 0 -> 'LL', else 'LR'
    # bf < -1 means right-heavy -- check the RIGHT child's bf:
    #   right child bf <= 0 -> 'RR', else 'RL'
    pass

print("\n5. FENWICK TREE: PREFIX SUM")
print("Input: Size n, then a sequence of updates and prefix queries")
print("Output: Prefix sums in O(log n)")
print("Example: [3,2,-1,6] -> prefix_sum(2) = 4")
class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)     # 1-indexed internally

    def update(self, i: int, delta: int) -> None:
        # TODO: Shift i to 1-indexed. While i <= n: add delta, then
        # advance with i += i & -i (jump to the next covering node).
        pass

    def prefix_sum(self, i: int) -> int:
        # TODO: Shift i to 1-indexed. While i > 0: accumulate tree[i],
        # then strip the lowest set bit with i -= i & -i.
        pass


# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n6. AVL INSERT")
print("Input: Subtree root, key to insert")
print("Output: New subtree root, rebalanced")
print("Example: inserting 1..7 in order gives height 3, not 7")
def avl_insert(node: Optional[AVLNode], key) -> AVLNode:
    # TODO: Three phases.
    # 1. Normal BST insert (recurse; ignore duplicates)
    # 2. update_height(node) on the way back up
    # 3. Check balance_factor and apply the right rotation.
    #    For insert you can pick the case by comparing `key` against
    #    the child's key -- there are exactly four cases.
    pass

print("\n7. AVL DELETE")
print("Input: Subtree root, key to delete")
print("Output: New subtree root, rebalanced")
print("Example: deleting the root of a 15-node AVL keeps height 4")
def avl_delete(node: Optional[AVLNode], key) -> Optional[AVLNode]:
    # TODO: BST delete first. Three child cases: 0 children, 1 child,
    # 2 children (replace the key with the in-order successor, then
    # delete that successor from the right subtree).
    # Then update_height and rebalance.
    # CAREFUL: pick the rotation case from the CHILD'S balance factor,
    # not a key comparison -- there is no inserted key here.
    pass

print("\n8. FENWICK RANGE SUM")
print("Input: A built FenwickTree, indices left and right (inclusive)")
print("Output: Sum over data[left..right]")
print("Example: prefix_sum(right) - prefix_sum(left-1)")
def fenwick_range_sum(ft: FenwickTree, left: int, right: int) -> int:
    # TODO: Difference of two prefix sums. Guard left == 0 (there is no
    # prefix_sum(-1)).
    pass

print("\n9. SEGMENT TREE: BUILD AND POINT QUERY")
print("Input: An array and an associative combine function")
print("Output: A tree supporting query(left, right) on the half-open range")
print("Example: SegmentTree([1,3,5,7]).query(1, 3) = 8")
class SegmentTree:
    def __init__(self, data: List, combine: Callable = None, identity=0):
        # TODO: Allocate tree = [identity] * (2 * n). Copy data into the
        # leaves at positions [n, 2n). Then fill internal nodes bottom-up:
        # for i from n-1 down to 1: tree[i] = combine(tree[2i], tree[2i+1])
        pass

    def query(self, left: int, right: int):
        # TODO: Iterative bottom-up over [left, right).
        # Shift both to leaf positions. While left < right:
        #   if left is odd, absorb tree[left] and left += 1
        #   if right is odd, right -= 1 and absorb tree[right]
        #   halve both
        pass

    def update(self, i: int, value) -> None:
        # TODO: Set the leaf, then walk to the root recombining as you go.
        pass

print("\n10. RANGE MINIMUM QUERY")
print("Input: An array")
print("Output: A structure answering min over any range in O(log n)")
print("Example: rmq([5,2,8,1,9]).query(0, 3) = 2")
def build_rmq(data: List[int]) -> SegmentTree:
    # TODO: This is one line -- the segment tree is already generic.
    # Pass min as combine and float('inf') as the identity.
    pass

print("\n11. COUNT INVERSIONS WITH A FENWICK TREE")
print("Input: Array of integers")
print("Output: Number of pairs (i, j) with i < j and nums[i] > nums[j]")
print("Example: [5, 4, 3, 2, 1] -> 10")
def count_inversions(nums: List[int]) -> int:
    # TODO: Compress values to ranks (sorted unique index). Sweep RIGHT to
    # LEFT: for each element, the answer gains prefix_sum(rank - 1) --
    # how many already-seen elements are strictly smaller. Then mark it.
    # O(n log n), matching the merge-sort approach from Topic 13.
    pass


# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n12. VALIDATE A RED-BLACK TREE")
print("Input: Root of a tree whose nodes have a .color attribute")
print("Output: True if all Red-Black invariants hold")
print("Example: a red root -> False (property 2)")
def validate_red_black(root) -> bool:
    # TODO: Check three things.
    #   Property 2: root is BLACK
    #   Property 4: no red node has a red child
    #   Property 5: every root->leaf path has the same black count
    # Trick: write a helper returning the black-height, or -1 for invalid.
    # A node is invalid if either child is invalid OR the two black-heights
    # disagree.
    pass

print("\n13. LAZY PROPAGATION: RANGE ADD, RANGE SUM")
print("Input: An array")
print("Output: range_add(l, r, delta) and range_sum(l, r), both O(log n)")
print("Example: add +10 to [2,5], then sum [0,7] reflects it")
class LazySegmentTree:
    def __init__(self, data: List[int]):
        # TODO: tree and lazy arrays of size 4n. Recursive build.
        pass

    def _push(self, node: int, lo: int, hi: int) -> None:
        # TODO: If lazy[node] is 0, return. Otherwise apply it to tree[node]
        # (delta * range length), hand it to both children if not a leaf,
        # then clear lazy[node].
        # This MUST be called before reading tree[node].
        pass

    def range_add(self, left: int, right: int, delta: int) -> None:
        # TODO: Push first. Three cases: disjoint (return), fully covered
        # (record the delta, push, return), partial (recurse both children,
        # then recombine).
        pass

    def range_sum(self, left: int, right: int) -> int:
        # TODO: Push first. Disjoint -> 0. Fully covered -> tree[node].
        # Partial -> sum of both recursive calls.
        pass

print("\n14. KTH SMALLEST ELEMENT VIA AUGMENTED AVL")
print("Input: An AVL tree whose nodes cache subtree size, and k (1-indexed)")
print("Output: The kth smallest key, in O(log n)")
print("Example: kth_smallest(tree_of_1_to_15, 4) -> 4")
def kth_smallest(root, k: int):
    # TODO: Requires a `size` field per node (size = 1 + sizes of children),
    # maintained alongside height. Then at each node:
    #   left_size = size(node.left)
    #   k == left_size + 1 -> this node is the answer
    #   k <= left_size     -> recurse left
    #   otherwise          -> recurse right with k - left_size - 1
    # This is why augmented trees exist: order statistics in O(log n)
    # instead of an O(n) in-order walk.
    pass

print("\n15. MERGE TWO BALANCED BSTS")
print("Input: Two AVL tree roots")
print("Output: One balanced AVL tree containing all keys")
print("Example: merge trees of [1,3,5] and [2,4,6] -> balanced tree of 1..6")
def merge_avl_trees(root_a, root_b):
    # TODO: Do NOT insert one tree into the other (that is O(n log n) with
    # heavy rotation churn). Instead:
    #   1. In-order traverse both into sorted lists       O(n + m)
    #   2. Merge the two sorted lists                     O(n + m)
    #   3. Build a balanced tree from the sorted result   O(n + m)
    #      by recursively taking the midpoint as the root
    # Total O(n + m), which beats repeated insertion.
    pass


# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n16. RANGE UPDATE WITH TWO FENWICK TREES")
print("Input: Size n")
print("Output: range_add(l, r, delta) and prefix_sum(i), both O(log n)")
print("Example: no segment tree needed -- two BITs suffice")
class RangeFenwick:
    def __init__(self, n: int):
        # TODO: Keep TWO Fenwick trees, B1 and B2.
        pass

    def range_add(self, left: int, right: int, delta: int) -> None:
        # TODO: The standard trick. Update B1 with +delta at left and
        # -delta at right+1. Update B2 with -delta*(left-1) at left and
        # +delta*right at right+1.
        pass

    def prefix_sum(self, i: int) -> int:
        # TODO: B1.prefix_sum(i) * i + B2.prefix_sum(i)
        # Work through why this telescopes correctly -- that is the exercise.
        pass

print("\n17. SEGMENT TREE ON A NON-COMMUTATIVE OPERATION")
print("Input: An array of 2x2 matrices")
print("Output: Range product, respecting order")
print("Example: matrix chains for linear recurrences")
def matrix_range_product(matrices: List[List[List[int]]], left: int, right: int):
    # TODO: Segment trees need ASSOCIATIVITY, not commutativity -- so this
    # works. But the iterative bottom-up query absorbs nodes out of order,
    # which breaks non-commutative combines. Accumulate a LEFT result and a
    # RIGHT result separately, then join them at the end.
    # Identity is the 2x2 identity matrix.
    pass

print("\n18. PERSISTENT SEGMENT TREE")
print("Input: An array, then a series of updates")
print("Output: Query any HISTORICAL version in O(log n)")
print("Example: version 0 is the original, version 5 is after 5 updates")
class PersistentSegmentTree:
    def __init__(self, data: List[int]):
        # TODO: Nodes are immutable. Keep a list of version roots.
        pass

    def update(self, version: int, i: int, value: int) -> int:
        # TODO: Path copying. Clone only the O(log n) nodes along the root->leaf
        # path; every other node is SHARED with the previous version. Append
        # the new root and return its version number.
        pass

    def query(self, version: int, left: int, right: int) -> int:
        # TODO: Ordinary range query, starting from that version's root.
        pass

print("\n19. AVL TREE WITH ORDER STATISTICS AND RANK")
print("Input: A size-augmented AVL tree")
print("Output: select(k) -> kth smallest, and rank(key) -> how many are smaller")
print("Example: rank and select are inverses of each other")
def rank_of(root, key) -> int:
    # TODO: Count keys strictly less than `key`. Descend from the root:
    # going right past a node adds (left subtree size + 1) to the rank.
    # Verify against select(): rank(select(k)) should equal k - 1.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Advanced Trees Cheat Sheet:

1. Why Balance Matters:
   A plain BST fed sorted input becomes a linked list -- height n, search
   O(n). Sorted input is COMMON (timestamps, auto-increment IDs, imports),
   so this is not a corner case. Balancing turns the worst case into the
   guaranteed case.

2. AVL Trees:
   Invariant : |height(left) - height(right)| <= 1 at every node
   Height    : <= 1.44 * log2(n)
   Cache the height on each node -- recomputing it is O(n) and defeats
   the purpose.

   The four cases (pick by bf sign, then the child's bf sign):
     LL  bf > 1,  left child left-heavy   -> rotate_right(node)
     LR  bf > 1,  left child right-heavy  -> rotate_left(left), rotate_right(node)
     RR  bf < -1, right child right-heavy -> rotate_left(node)
     RL  bf < -1, right child left-heavy  -> rotate_right(right), rotate_left(node)

   Insert : at most ONE rotation (or one double) fixes the whole tree
   Delete : may cascade -- up to O(log n) rotations back to the root

3. Rotations:
   O(1). Rewire three pointers, fix two heights. They PRESERVE the BST
   ordering, which is exactly why they are safe to apply.
   Update the node that moved DOWN first -- its children are already correct.
   ALWAYS reassign the result: node.left = rotate_left(node.left)

4. Red-Black Trees:
   1. Every node is red or black
   2. The root is black
   3. NIL leaves are black
   4. A red node has no red child
   5. Every root->leaf path has the same black count

   Height <= 2 * log2(n). New nodes are inserted RED (cannot break
   property 5, only property 4), then fixed up:
     uncle RED   -> recolor, recurse two levels up
     uncle BLACK -> rotate (possibly twice), recolor, done

5. AVL vs Red-Black:

   Dimension          AVL              Red-Black
   ─────────────────────────────────────────────────────
   Height bound       1.44 log n       2.00 log n
   Search             faster           slightly slower
   Insert/delete      more rotations   fewer rotations
   Delete rotations   O(log n)         O(1) amortized
   Per-node overhead  height (int)     color (1 bit)
   Choose when        read-heavy       write-heavy

   Real libraries ship Red-Black: Java TreeMap/TreeSet, C++ std::map/set,
   the Linux CFS scheduler, epoll internals.

6. Segment Trees:
   Answers ANY associative range query in O(log n), with O(log n) point
   updates and O(n) space. Build is O(n).

     combine=add, identity=0            -> range sum
     combine=min, identity=+inf         -> range minimum
     combine=max, identity=-inf         -> range maximum
     combine=gcd, identity=0            -> range gcd

   The key fact: any range decomposes into at most 2*log n stored nodes.
   Associativity is required. Commutativity is NOT -- but non-commutative
   combines need the left/right accumulators kept separate.

7. Lazy Propagation:
   Turns range UPDATES from O(n log n) into O(log n) by storing a pending
   delta per node and pushing it down only on descent.
   Rule: call _push before you read a node's aggregate. Every time.

8. Fenwick Tree (BIT):
   Prefix sums with point updates, in ~15 lines and O(n) space.
   tree[i] covers a block of size (i & -i) ending at i.
     i += i & -i   walks to the next covering node   (update)
     i -= i & -i   strips the lowest set bit         (query)
   Both loops run O(log n) times because each step changes one bit.
   1-INDEXED internally -- index 0 would make i & -i == 0 and hang.

9. Segment Tree vs Fenwick Tree:

   Need                          Use
   ─────────────────────────────────────────────
   Prefix / range sums only      Fenwick (half the space, less code)
   Range min / max / gcd         Segment tree (not invertible)
   Range updates                 Segment tree + lazy (or two Fenwicks)
   Smallest possible code        Fenwick
   Arbitrary associative op      Segment tree

10. B-Trees:
    High fan-out to minimize DISK SEEKS. Height O(log_m n), so m=100 puts
    a million keys three levels deep. B+ trees keep values only in linked
    leaves, which makes range scans fast.
    Used by: PostgreSQL, MySQL InnoDB, SQLite, MongoDB, NTFS, ext4.

Complexity Reference:

Structure        Search      Insert      Delete      Range       Space
──────────────────────────────────────────────────────────────────────
Plain BST worst  O(n)        O(n)        O(n)        O(n)        O(n)
Plain BST avg    O(log n)    O(log n)    O(log n)    O(k+log n)  O(n)
AVL              O(log n)    O(log n)    O(log n)    O(k+log n)  O(n)
Red-Black        O(log n)    O(log n)    O(log n)    O(k+log n)  O(n)
Segment Tree     O(log n)    O(log n)    -           O(log n)    O(n)
Fenwick Tree     -           O(log n)    -           O(log n)    O(n)
B+ Tree          O(log n)    O(log n)    O(log n)    O(k+log n)  O(n)
Hash table       O(1) avg    O(1) avg    O(1) avg    O(n)        O(n)

k = number of results returned.

Note that last row. A hash table beats every tree on single-key lookup.
Trees earn their keep when you need ORDER: ranges, successor/predecessor,
sorted iteration, min/max. If you do not need order, use a dict.

Common Pitfalls:

1. Recomputing height instead of reading the cached field -- O(n) per check.
2. Dropping the rotation's return value. `rotate_left(node.left)` without
   the assignment silently corrupts the tree.
3. Updating heights in the wrong order during a rotation. Lower node first.
4. Using a key comparison to pick the delete rotation case. Use the child's
   balance factor -- there is no inserted key during a delete.
5. Mixing [l, r) and [l, r] conventions in one segment tree. Pick one.
6. Forgetting _push before reading a lazy node. The value is stale.
7. Feeding a non-associative op (like "average") to a segment tree.
   Store (sum, count) and divide at the end instead.
8. Passing index 0 to a Fenwick update. i & -i on 0 is 0 -- infinite loop.
9. Assuming a segment tree query is commutative-safe. Matrix products are
   associative but not commutative; keep left/right accumulators separate.

Problem Recognition Guide:

"range sum / min / max with updates"    -> segment tree or Fenwick
"prefix sums with updates"              -> Fenwick tree
"add X to every element in [l, r]"      -> lazy propagation
"kth smallest / rank of an element"     -> size-augmented BST
"count inversions"                      -> Fenwick (or merge sort)
"keep a sorted structure under inserts" -> AVL / Red-Black
"successor / predecessor queries"       -> any balanced BST
"index on disk"                         -> B+ tree
"just look up by key"                   -> dict. Not a tree.

Interview Tips:

1. DRAW the rotation. Nobody explains the LR case correctly from memory
   without a diagram -- and interviewers know that.
2. Know why insert needs <= 1 rotation but delete may need O(log n).
   It shows you understand the invariant, not just the code.
3. Justify AVL vs Red-Black with the read/write ratio. "AVL is better"
   is a wrong answer; "AVL for read-heavy" is a right one.
4. State the hash-table alternative and why order rules it out. Reaching
   for a tree when a dict would do is a red flag.
5. For range problems, say the O(n) and prefix-sum approaches first, then
   explain what the tree buys you. It proves you know the trade-off.
6. Mention lazy propagation the moment range updates appear.

Learning Progression:

1. Basic: heights, balance factors, the four rotation cases
2. Intermediate: full AVL insert and delete, Fenwick prefix sums
3. Advanced: Red-Black fixup, segment trees, lazy propagation
4. Expert: persistent structures, order statistics, two-BIT range updates

Next: Implement each stub, then run project.py to see these structures
running a database index, a leaderboard, and a time-series store!
""")
