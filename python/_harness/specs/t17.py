"""
Specs for Topic 17 -- Advanced Trees.

Three decisions shape this file.

**AVL results are graded on properties, not on shape.** `avl_insert`,
`avl_delete` and `merge_avl_trees` are checked with `norm`, which extracts
(in-order keys, is-balanced, heights-consistent) from BOTH the learner's tree
and the reference's. Any correct AVL implementation passes regardless of which
rotation-selection style it uses, while a plain BST insert fails on the
is-balanced component. Comparing raw tree shape would have failed correct code
that picks cases from the child's balance factor rather than a key comparison.

**Inputs that need a working data structure get a spec-local one.**
`fenwick_range_sum` takes a FenwickTree instance, and `validate_red_black`
takes a tree of colour-bearing nodes that this exercise file never defines.
Both are supplied by the spec, so those problems can be solved in any order.
Where the dependency is unavoidable -- `build_rmq` constructs the module's own
SegmentTree -- the note says so.

**Order-statistic problems get their `size` field pre-set.** `kth_smallest`
and `rank_of` need `node.size`, which the provided AVLNode does not carry, so
the builder sets it. The learner reads it; they do not have to maintain it to
be graded here.
"""

import operator
from typing import Optional

from ..spec import spec


# ------------------------------------------------------- tree introspection

def _inorder(node):
    """Keys, left to right. The canonical fingerprint of a BST's contents."""
    if node is None:
        return []
    return _inorder(node.left) + [node.key] + _inorder(node.right)


def _true_height(node):
    if node is None:
        return 0
    return 1 + max(_true_height(node.left), _true_height(node.right))


def _is_balanced(node) -> bool:
    if node is None:
        return True
    if abs(_true_height(node.left) - _true_height(node.right)) > 1:
        return False
    return _is_balanced(node.left) and _is_balanced(node.right)


def _heights_cached_ok(node) -> bool:
    """Are the cached `height` fields actually correct everywhere?"""
    if node is None:
        return True
    if getattr(node, "height", None) != _true_height(node):
        return False
    return _heights_cached_ok(node.left) and _heights_cached_ok(node.right)


def _avl_shape(node):
    """(in-order keys, balanced?, cached heights right?) -- see the docstring."""
    if node is None:
        return ([], True, True)
    return (_inorder(node), _is_balanced(node), _heights_cached_ok(node))


def _structure(node):
    """Exact shape as nested tuples. Used only where shape IS the answer."""
    if node is None:
        return None
    return (node.key, _structure(node.left), _structure(node.right))


# ------------------------------------------------------------- AVL builders

def _fix(node):
    """Recompute cached height and size bottom-up for a hand-built tree."""
    if node is None:
        return 0, 0
    lh, ls = _fix(node.left)
    rh, rs = _fix(node.right)
    node.height = 1 + max(lh, rh)
    node.size = 1 + ls + rs
    return node.height, node.size


def _balanced_from_sorted(AVLNode, keys):
    """A perfectly balanced BST, with heights and sizes filled in."""
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = AVLNode(keys[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    root = build(0, len(keys) - 1)
    _fix(root)
    return root


def b_avl(module, rng):
    keys = sorted(rng.sample(range(0, 200), rng.randint(0, 15)))
    return (_balanced_from_sorted(module.AVLNode, keys),)


def b_avl_nonempty(module, rng):
    keys = sorted(rng.sample(range(0, 200), rng.randint(1, 15)))
    return (_balanced_from_sorted(module.AVLNode, keys),)


def b_avl_stale_height(module, rng):
    """
    A tree whose ROOT carries a deliberately wrong cached height.

    Handing over an already-correct tree made `update_height` untestable: doing
    nothing produced the right answer, so an unwritten stub passed. Only the
    root is corrupted -- the function is specified to read its children's
    cached heights, which therefore have to be right.
    """
    keys = sorted(rng.sample(range(0, 200), rng.randint(1, 15)))
    root = _balanced_from_sorted(module.AVLNode, keys)
    root.height = rng.choice([0, 1, 99])
    return (root,)


def b_avl_insert(module, rng):
    keys = sorted(rng.sample(range(0, 200), rng.randint(0, 14)))
    tree = _balanced_from_sorted(module.AVLNode, keys)
    # Sometimes insert a key that is already present, to exercise the
    # "ignore duplicates" rule the exercise states.
    key = rng.choice(keys) if keys and rng.random() < 0.2 \
        else rng.randint(200, 400)
    return (tree, key)


def b_avl_delete(module, rng):
    keys = sorted(rng.sample(range(0, 200), rng.randint(1, 15)))
    tree = _balanced_from_sorted(module.AVLNode, keys)
    # Deleting an absent key must be a no-op, so test that too.
    key = rng.choice(keys) if rng.random() < 0.85 else 999
    return (tree, key)


def b_two_avls(module, rng):
    a = sorted(rng.sample(range(0, 100), rng.randint(0, 8)))
    b = sorted(rng.sample(range(100, 200), rng.randint(0, 8)))
    return (_balanced_from_sorted(module.AVLNode, a),
            _balanced_from_sorted(module.AVLNode, b))


def b_kth(module, rng):
    n = rng.randint(1, 15)
    keys = list(range(1, n + 1))
    return (_balanced_from_sorted(module.AVLNode, keys), rng.randint(1, n))


def b_rank(module, rng):
    keys = sorted(rng.sample(range(0, 60), rng.randint(0, 15)))
    tree = _balanced_from_sorted(module.AVLNode, keys)
    key = rng.choice(keys) if keys and rng.random() < 0.6 else rng.randint(0, 60)
    return (tree, key)


def b_rotatable(module, rng):
    """A subtree that definitely has the child the rotation needs."""
    AVLNode = module.AVLNode
    keys = sorted(rng.sample(range(0, 100), rng.randint(3, 9)))
    root = _balanced_from_sorted(AVLNode, keys)
    return (root,)


def b_left_chain(module, rng):
    """z -> z.left -> z.left.left, the classic LL case."""
    AVLNode = module.AVLNode
    c, b, a = sorted(rng.sample(range(0, 100), 3), reverse=True)
    z = AVLNode(c)
    z.left = AVLNode(b)
    z.left.left = AVLNode(a)
    _fix(z)
    return (z,)


def b_right_chain(module, rng):
    a, b, c = sorted(rng.sample(range(0, 100), 3))
    AVLNode = module.AVLNode
    z = AVLNode(a)
    z.right = AVLNode(b)
    z.right.right = AVLNode(c)
    _fix(z)
    return (z,)


# --------------------------------------------------------- AVL references

def _ref_height(node):
    return 0 if node is None else node.height


def _ref_balance_factor(node):
    if node is None:
        return 0
    return _ref_height(node.left) - _ref_height(node.right)


def _ref_update_height(node):
    node.height = 1 + max(_ref_height(node.left), _ref_height(node.right))


def _ref_rotate_right(z):
    y = z.left
    z.left = y.right
    y.right = z
    _ref_update_height(z)
    _ref_update_height(y)
    return y


def _ref_rotate_left(z):
    y = z.right
    z.right = y.left
    y.left = z
    _ref_update_height(z)
    _ref_update_height(y)
    return y


def _ref_rotation_case(node):
    bf = _ref_balance_factor(node)
    if bf > 1:
        return "LL" if _ref_balance_factor(node.left) >= 0 else "LR"
    if bf < -1:
        return "RR" if _ref_balance_factor(node.right) <= 0 else "RL"
    return "BALANCED"


def _ref_avl_insert(node, key):
    if node is None:
        new = _NodeProxy(key)
        return new
    if key < node.key:
        node.left = _ref_avl_insert(node.left, key)
    elif key > node.key:
        node.right = _ref_avl_insert(node.right, key)
    else:
        return node                      # duplicates ignored, as specified
    _ref_update_height(node)
    bf = _ref_balance_factor(node)
    if bf > 1:
        if key > node.left.key:
            node.left = _ref_rotate_left(node.left)
        return _ref_rotate_right(node)
    if bf < -1:
        if key < node.right.key:
            node.right = _ref_rotate_right(node.right)
        return _ref_rotate_left(node)
    return node


class _NodeProxy:
    """
    A node the reference can create on its own.

    The reference receives the learner's nodes but sometimes has to allocate a
    new one, and it cannot reach into their module to do it. Duck typing makes
    a local class interchangeable -- everything downstream only touches
    `.key`, `.left`, `.right`, `.height` and `.size`.
    """

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1


def _ref_avl_delete(node, key):
    if node is None:
        return None
    if key < node.key:
        node.left = _ref_avl_delete(node.left, key)
    elif key > node.key:
        node.right = _ref_avl_delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        succ = node.right
        while succ.left:
            succ = succ.left
        node.key = succ.key
        node.right = _ref_avl_delete(node.right, succ.key)
    _ref_update_height(node)
    bf = _ref_balance_factor(node)
    if bf > 1:
        # Case picked from the CHILD's balance factor: there is no inserted
        # key to compare against on a delete.
        if _ref_balance_factor(node.left) < 0:
            node.left = _ref_rotate_left(node.left)
        return _ref_rotate_right(node)
    if bf < -1:
        if _ref_balance_factor(node.right) > 0:
            node.right = _ref_rotate_right(node.right)
        return _ref_rotate_left(node)
    return node


def _ref_merge(root_a, root_b):
    keys = sorted(_inorder(root_a) + _inorder(root_b))
    return _balanced_from_sorted(_NodeProxy, keys)


def _ref_kth(root, k):
    keys = _inorder(root)
    return keys[k - 1] if 1 <= k <= len(keys) else None


def _ref_rank(root, key):
    return sum(1 for v in _inorder(root) if v < key)


def _ref_is_avl_balanced(root):
    return _is_balanced(root)


# ------------------------------------------------------------- Fenwick etc.

class _Fenwick:
    """A working Fenwick tree, so problem 8 does not depend on problem 5."""

    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total


def _fenwick_of(values):
    ft = _Fenwick(len(values))
    for i, v in enumerate(values):
        ft.update(i, v)
    return ft


def _ref_range_sum(ft, left, right):
    return ft.prefix_sum(right) - (ft.prefix_sum(left - 1) if left > 0 else 0)


def g_range_sum(rng):
    values = [rng.randint(-20, 20) for _ in range(rng.randint(1, 12))]
    left = rng.randint(0, len(values) - 1)
    right = rng.randint(left, len(values) - 1)
    return (_fenwick_of(values), left, right)


def _ref_count_inversions(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums))
               if nums[i] > nums[j])


def g_inversions(rng):
    return ([rng.randint(0, 20) for _ in range(rng.randint(0, 14))],)


# ------------------------------------------------------------- Red-Black

class _RB:
    """
    Nodes for problem 12, with the colour convention the note states.

    The exercise file defines no red-black node type, so the spec supplies
    one. `color` is the string "RED" or "BLACK".
    """

    def __init__(self, key, color, left=None, right=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right


def _ref_validate_rb(root) -> bool:
    if root is None:
        return True
    if root.color != "BLACK":
        return False                                  # property 2

    def black_height(node):
        if node is None:
            return 1
        if node.color == "RED":
            for child in (node.left, node.right):
                if child is not None and child.color == "RED":
                    return -1                         # property 4
        lh = black_height(node.left)
        rh = black_height(node.right)
        if lh == -1 or rh == -1 or lh != rh:
            return -1                                 # property 5
        return lh + (1 if node.color == "BLACK" else 0)

    return black_height(root) != -1


def g_rb(rng):
    """Mostly valid trees, with deliberate violations mixed in."""
    def make(depth):
        if depth == 0 or rng.random() < 0.3:
            return None
        color = "RED" if rng.random() < 0.35 else "BLACK"
        return _RB(rng.randint(0, 99), color, make(depth - 1), make(depth - 1))

    root = _RB(rng.randint(0, 99),
               "RED" if rng.random() < 0.2 else "BLACK",
               make(3), make(3))
    return (root,)


# ------------------------------------------------------------- matrices

def _matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def _ref_matrix_product(matrices, left, right):
    """Half-open [left, right), matching SegmentTree.query in problem 9."""
    result = [[1, 0], [0, 1]]
    for m in matrices[left:right]:
        result = _matmul(result, m)
    return result


def g_matrices(rng):
    n = rng.randint(1, 8)
    mats = [[[rng.randint(-3, 3) for _ in range(2)] for _ in range(2)]
            for _ in range(n)]
    left = rng.randint(0, n - 1)
    right = rng.randint(left + 1, n)
    return (mats, left, right)


# ------------------------------------------------------------------- specs

SPECS = [
    spec(1, "height", ref=_ref_height, build=b_avl,
         note="return the CACHED height field; None has height 0"),
    spec(1, "balance_factor", ref=_ref_balance_factor, build=b_avl,
         note="height(left) - height(right); None has balance factor 0"),
    # `norm`, not `prop`: with a `ref` in play the expected side is the
    # reference's own mutated node, and `prop` only transforms the actual --
    # so the comparison was node-vs-int and every correct answer failed.
    spec(1, "update_height", inplace=True, norm=lambda n: n.height,
         ref=_ref_update_height, build=b_avl_stale_height,
         note="sets node.height in place and returns None"),

    spec(2, "rotate_right", ref=_ref_rotate_right, build=b_left_chain,
         norm=_structure,
         note="returns the NEW subtree root; heights updated (z first, then "
              "y). Graded on exact shape -- rotation is a structural answer"),
    spec(2, "rotate_left", ref=_ref_rotate_left, build=b_right_chain,
         norm=_structure,
         note="mirror of rotate_right; returns the new subtree root"),

    spec(3, "is_avl_balanced", ref=_ref_is_avl_balanced, build=b_avl,
         note="|balance factor| <= 1 at EVERY node, not just the root"),

    spec(4, "rotation_case", ref=_ref_rotation_case, build=b_rotatable,
         note="one of 'LL', 'LR', 'RR', 'RL', 'BALANCED'"),

    spec(5, "FenwickTree",
         script=lambda cls: (lambda ft: [
             [ft.update(i, v) for i, v in enumerate([3, 2, -1, 6])],
             ft.prefix_sum(0), ft.prefix_sum(2), ft.prefix_sum(3),
         ][1:])(cls(4)),
         ref_script=lambda: [3, 4, 10],
         note="indices are 0-based from the outside and prefix_sum(i) is "
              "INCLUSIVE, as in the exercise's own example: [3,2,-1,6] -> "
              "prefix_sum(2) = 4"),

    spec(6, "avl_insert", ref=_ref_avl_insert, build=b_avl_insert,
         norm=_avl_shape,
         note="graded on (in-order keys, balanced, cached heights correct), "
              "so any correct rotation style passes; duplicates are ignored"),

    spec(7, "avl_delete", ref=_ref_avl_delete, build=b_avl_delete,
         norm=_avl_shape,
         note="graded on (in-order keys, balanced, cached heights correct); "
              "deleting an absent key is a no-op"),

    spec(8, "fenwick_range_sum", ref=_ref_range_sum, gen=g_range_sum,
         note="inclusive on both ends; the FenwickTree you are handed already "
              "works, so this does not depend on problem 5"),

    spec(9, "SegmentTree",
         script=lambda cls: (lambda st: [
             st.query(1, 3), st.query(0, 4),
             (st.update(0, 10), st.query(0, 2))[1],
         ])(cls([1, 3, 5, 7])),
         ref_script=lambda: [8, 16, 13],
         note="query is HALF-OPEN [left, right), as in the exercise's example "
              "query(1,3)=8. A combine of None means addition"),

    spec(10, "build_rmq",
         prop=lambda st: [st.query(0, 3), st.query(2, 5), st.query(0, 5)],
         cases=[(([5, 2, 8, 1, 9],), [2, 1, 1])],
         note="returns a SegmentTree configured for min, so this needs "
              "problem 9 working first. Ranges are half-open"),

    spec(11, "count_inversions", ref=_ref_count_inversions, gen=g_inversions,
         cases=[(([5, 4, 3, 2, 1],), 10), (([1, 2, 3],), 0), (([],), 0)]),

    spec(12, "validate_red_black", ref=_ref_validate_rb, gen=g_rb,
         cases=[((_RB(1, "RED"),), False),
                ((_RB(1, "BLACK"),), True),
                ((None,), True),
                ((_RB(2, "BLACK", _RB(1, "RED", _RB(0, "RED")), None),),
                 False)],
         note="node.color is the string 'RED' or 'BLACK'; an empty tree is "
              "valid. Checks properties 2, 4 and 5"),

    spec(13, "LazySegmentTree",
         script=lambda cls: (lambda t: [
             t.range_sum(0, 7),
             (t.range_add(2, 5, 10), t.range_sum(0, 7))[1],
             t.range_sum(2, 5), t.range_sum(0, 1),
         ])(cls([1, 2, 3, 4, 5, 6, 7, 8])),
         ref_script=lambda: [36, 76, 58, 3],
         note="ranges are INCLUSIVE on both ends here, matching range_add"
              "(l, r, delta) in the exercise's example"),

    spec(14, "kth_smallest", ref=_ref_kth, build=b_kth,
         note="k is 1-indexed; the tree you are handed already carries a "
              "correct node.size on every node"),

    spec(15, "merge_avl_trees", ref=_ref_merge, build=b_two_avls,
         norm=_avl_shape,
         note="graded on (in-order keys, balanced, cached heights correct)"),

    spec(16, "RangeFenwick",
         script=lambda cls: (lambda rf: [
             rf.range_add(1, 3, 5),
             rf.prefix_sum(0), rf.prefix_sum(1), rf.prefix_sum(3),
             rf.prefix_sum(4),
         ][1:])(cls(5)),
         ref_script=lambda: [0, 5, 15, 15],
         note="0-based, prefix_sum inclusive. After range_add(1,3,+5) the "
              "array is [0,5,5,5,0]"),

    spec(17, "matrix_range_product", ref=_ref_matrix_product, gen=g_matrices,
         cases=[(([[[1, 1], [1, 0]], [[1, 1], [1, 0]]], 0, 2),
                 [[2, 1], [1, 1]]),
                (([[[1, 2], [3, 4]]], 0, 1), [[1, 2], [3, 4]])],
         note="half-open [left, right), and the product must respect ORDER -- "
              "matrix multiplication does not commute"),

    spec(18, "PersistentSegmentTree",
         script=lambda cls: (lambda t: [
             t.query(0, 0, 4),
             t.update(0, 1, 100),
             t.query(1, 0, 4), t.query(0, 0, 4),
         ])(cls([1, 2, 3, 4])),
         ref_script=lambda: [10, 1, 108, 10],
         note="version 0 is the original; update returns the NEW version "
              "number; query ranges are half-open. The point is that "
              "querying version 0 still returns the old answer"),

    spec(19, "rank_of", ref=_ref_rank, build=b_rank,
         note="how many keys are STRICTLY less than `key`, so rank of the "
              "smallest key is 0. node.size is already correct"),
]
