"""
Specs for Topic 08 -- Trees (Basics).

Inputs are built from the learner's own TreeNode class via `build`, using
level-order lists with None for absent children (the LeetCode convention).
"""

from collections import deque

from ..spec import spec


# --------------------------------------------------------------- scaffolding

def _make(module, level_order):
    """Build a tree from a level-order list; None means 'no node'."""
    TreeNode = module.TreeNode
    if not level_order or level_order[0] is None:
        return None
    root = TreeNode(level_order[0])
    q = deque([root])
    i = 1
    while q and i < len(level_order):
        node = q.popleft()
        if i < len(level_order):
            v = level_order[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                q.append(node.left)
        if i < len(level_order):
            v = level_order[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                q.append(node.right)
    return root


def _inorder(node):
    return (_inorder(node.left) + [node.value] + _inorder(node.right)
            if node else [])


def _depth(node):
    return 1 + max(_depth(node.left), _depth(node.right)) if node else 0


def _levels(node):
    out = []
    q = deque([node] if node else [])
    while q:
        out.append([n.value for n in q])
        nxt = deque()
        for n in q:
            if n.left:
                nxt.append(n.left)
            if n.right:
                nxt.append(n.right)
        q = nxt
    return out


def _mirror_values(node):
    """In-order traversal of the MIRRORED tree, without mutating anything."""
    if not node:
        return []
    return _mirror_values(node.right) + [node.value] + _mirror_values(node.left)


def _is_bst(node, lo=float("-inf"), hi=float("inf")):
    if not node:
        return True
    if not lo < node.value < hi:
        return False
    return (_is_bst(node.left, lo, node.value)
            and _is_bst(node.right, node.value, hi))


def _has_path_sum(node, target):
    if not node:
        return False
    if not node.left and not node.right:
        return node.value == target
    rest = target - node.value
    return _has_path_sum(node.left, rest) or _has_path_sum(node.right, rest)


def _zigzag(node):
    lv = _levels(node)
    return [row if i % 2 == 0 else row[::-1] for i, row in enumerate(lv)]


def _max_path_sum(node):
    """Any-node-to-any-node maximum path sum."""
    best = float("-inf")

    def down(n):
        nonlocal best
        if not n:
            return 0
        l = max(0, down(n.left))
        r = max(0, down(n.right))
        best = max(best, n.value + l + r)
        return n.value + max(l, r)

    down(node)
    return best


def _lca(node, p, q):
    if not node:
        return None
    if node.value in (p, q):
        return node.value
    left = _lca(node.left, p, q)
    right = _lca(node.right, p, q)
    if left is not None and right is not None:
        return node.value
    return left if left is not None else right


# ------------------------------------------------------------------ builders

def _random_level_order(rng, n_max=12, lo=1, hi=20, allow_none=True):
    n = rng.randint(0, n_max)
    vals = []
    for _ in range(n):
        if allow_none and vals and rng.random() < 0.25:
            vals.append(None)
        else:
            vals.append(rng.randint(lo, hi))
    return vals


def b_tree(module, rng):
    return (_make(module, _random_level_order(rng)),)


def b_bst_or_not(module, rng):
    """Half genuine BSTs, half random -- so is_valid_bst sees both."""
    if rng.random() < 0.5:
        vals = sorted(rng.sample(range(1, 60), rng.randint(0, 7)))
        # build a balanced BST from the sorted values
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            node = module.TreeNode(vals[mid])
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node
        return (build(0, len(vals) - 1),)
    return (_make(module, _random_level_order(rng)),)


def b_tree_target(module, rng):
    vals = _random_level_order(rng, 10, 1, 9)
    root = _make(module, vals)
    return (root, rng.randint(1, 25))


def b_signed_tree(module, rng):
    return (_make(module, _random_level_order(rng, 10, -9, 9)),)


# --------------------------------------------------------------------- cases

SAMPLE = [3, 9, 20, None, None, 15, 7]


def c_inorder(module):
    return [((_make(module, [1, None, 2, 3]),), [1, 3, 2]),
            ((None,), [])]


def c_depth(module):
    return [((_make(module, SAMPLE),), 3), ((None,), 0),
            ((_make(module, [1]),), 1)]


def c_levels(module):
    return [((_make(module, SAMPLE),), [[3], [9, 20], [15, 7]]),
            ((None,), [])]


def c_bst(module):
    return [((_make(module, [2, 1, 3]),), True),
            ((_make(module, [5, 1, 4, None, None, 3, 6]),), False),
            ((None,), True)]


def c_path_sum(module):
    return [((_make(module, [5, 4, 8, 11, None, 13, 4,
                             7, 2, None, None, None, 1]), 22), True),
            ((_make(module, [1, 2, 3]), 5), False),
            ((None, 0), False)]


def c_zigzag(module):
    return [((_make(module, SAMPLE),), [[3], [20, 9], [15, 7]]),
            ((None,), [])]


def c_invert(module):
    return [((_make(module, [4, 2, 7, 1, 3, 6, 9]),), [9, 7, 6, 4, 3, 2, 1]),
            ((None,), [])]


def c_max_path(module):
    return [((_make(module, [1, 2, 3]),), 6),
            ((_make(module, [-10, 9, 20, None, None, 15, 7]),), 42)]


def c_lca(module):
    t = [3, 5, 1, 6, 2, 0, 8]
    return [((_make(module, t), 5, 1), 3),
            ((_make(module, t), 6, 2), 5),
            ((_make(module, t), 5, 5), 5)]


def _shape(node):
    """Exact structure as nested tuples -- None for an absent child."""
    if node is None:
        return None
    return (node.value, _shape(node.left), _shape(node.right))


def _ref_vertical(root):
    """
    Columns left to right; within a column, top to bottom in BFS order.

    Ties at the same (row, column) keep BFS insertion order, which is the
    LeetCode 314 convention. LeetCode 987 instead sorts tied values, so the
    note says which one applies.
    """
    if root is None:
        return []
    from collections import defaultdict, deque
    cols = defaultdict(list)
    q = deque([(root, 0)])
    while q:
        node, col = q.popleft()
        cols[col].append(node.value)
        if node.left:
            q.append((node.left, col - 1))
        if node.right:
            q.append((node.right, col + 1))
    return [cols[c] for c in sorted(cols)]


class _TN:
    """A node the reference can allocate without reaching into the module."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def _ref_build_tree(preorder, inorder):
    if not preorder:
        return None
    root = _TN(preorder[0])
    cut = inorder.index(preorder[0])
    root.left = _ref_build_tree(preorder[1:cut + 1], inorder[:cut])
    root.right = _ref_build_tree(preorder[cut + 1:], inorder[cut + 1:])
    return root


def _random_tree(TreeNode, rng, n):
    """A random-shaped tree with distinct values."""
    if n == 0:
        return None
    values = rng.sample(range(1, 100), n)
    root = TreeNode(values[0])
    nodes = [root]
    for v in values[1:]:
        parent = rng.choice(nodes)
        while parent.left is not None and parent.right is not None:
            parent = rng.choice(nodes)
        child = TreeNode(v)
        if parent.left is None and (parent.right is not None or rng.random() < 0.5):
            parent.left = child
        else:
            parent.right = child
        nodes.append(child)
    return root


def _preorder_vals(node):
    return [] if node is None else [node.value] + _preorder_vals(node.left) + _preorder_vals(node.right)


def _inorder_vals(node):
    return [] if node is None else _inorder_vals(node.left) + [node.value] + _inorder_vals(node.right)


def b_traversals(module, rng):
    tree = _random_tree(module.TreeNode, rng, rng.randint(0, 10))
    return (_preorder_vals(tree), _inorder_vals(tree))


def c_build_tree(module):
    """
    Expected values are TREES, not shapes.

    This spec compares with `norm`, which transforms both sides -- so handing
    over a pre-computed shape tuple would have `norm` try to read `.val` off a
    tuple. The expectation has to be the same kind of thing as the answer.
    """
    return [(([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]),
             _ref_build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])),
            (([], []), None)]


def b_vertical(module, rng):
    return (_random_tree(module.TreeNode, rng, rng.randint(0, 10)),)


def c_vertical(module):
    TreeNode = module.TreeNode
    root = TreeNode(3)
    root.left, root.right = TreeNode(9), TreeNode(20)
    root.right.left, root.right.right = TreeNode(15), TreeNode(7)
    return [((root,), [[9], [3, 15], [20], [7]]), ((None,), [])]


def c_serialize_roundtrip(module):
    """
    Cases for `deserialize`, built by calling the learner's own `serialize`.

    The serialized FORMAT is the learner's choice, so comparing strings would
    be wrong. What must hold is that their pair round-trips: deserialize of
    serialize rebuilds the same tree. `build_cases` gets the module, which is
    the only place a spec can reach their serialize to set this up.
    """
    import random as _random
    rng = _random.Random(20250811)
    out = []
    for n in (0, 1, 5, 9):
        tree = _random_tree(module.TreeNode, rng, n)
        out.append(((module.serialize(tree),), _shape(tree)))
    return out


def c_serialize_is_text(module):
    rng = __import__("random").Random(7)
    tree = _random_tree(module.TreeNode, rng, 6)
    return [((tree,), True), ((None,), True)]


SPECS = [
    spec(1, "inorder_traversal", ref=_inorder, build=b_tree,
         build_cases=c_inorder),
    spec(2, "max_depth", ref=_depth, build=b_tree, build_cases=c_depth),
    spec(3, "invert_tree", prop=_inorder, ref=_mirror_values, build=b_tree,
         build_cases=c_invert,
         note="the inverted tree's in-order traversal is compared"),
    spec(4, "is_valid_bst", ref=_is_bst, build=b_bst_or_not,
         build_cases=c_bst),
    spec(5, "level_order", ref=_levels, build=b_tree, build_cases=c_levels),
    spec(6, "lowest_common_ancestor", ref=_lca, build_cases=c_lca,
         note="returns the ancestor's VALUE"),
    spec(7, "path_sum", ref=_has_path_sum, build=b_tree_target,
         build_cases=c_path_sum,
         note="root-to-LEAF paths only"),
    spec(8, "zigzag_level_order", ref=_zigzag, build=b_tree,
         build_cases=c_zigzag),
    spec(9, "max_path_sum", ref=_max_path_sum, build=b_signed_tree,
         build_cases=c_max_path,
         note="any node to any node; at least one node must be used"),

    spec(10, "serialize", prop=lambda s: isinstance(s, str) and len(s) >= 0,
         build_cases=c_serialize_is_text,
         note="any text format is fine -- correctness is checked by whether "
              "your deserialize can rebuild the tree from it"),
    spec(10, "deserialize", prop=_shape, build_cases=c_serialize_roundtrip,
         note="graded as a ROUND TRIP against your own serialize, so the "
              "format is entirely your choice"),

    spec(11, "vertical_order", ref=_ref_vertical, build=b_vertical,
         build_cases=c_vertical,
         note="columns left to right; within a column, BFS (top-down) order, "
              "which is the LeetCode 314 convention"),

    spec(12, "build_tree", ref=_ref_build_tree, build=b_traversals,
         norm=_shape, build_cases=c_build_tree,
         note="values are distinct; returns the reconstructed root"),
]
