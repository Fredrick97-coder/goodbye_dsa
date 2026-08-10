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
]
