"""
Examples: Binary Trees and Binary Search Trees
"""

from collections import deque
from typing import Optional, List

print("=" * 60)
print("BINARY TREES & TRAVERSALS - EXAMPLES")
print("=" * 60)

class TreeNode:
    """Binary tree node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ==================== (1) Tree Traversals ====================
print("\n[1] DFS Traversals - Recursion")
print("-" * 40)

def inorder(node, result=None):
    """Left → Root → Right"""
    if result is None:
        result = []
    if not node:
        return result
    inorder(node.left, result)
    result.append(node.value)
    inorder(node.right, result)
    return result

def preorder(node, result=None):
    """Root → Left → Right"""
    if result is None:
        result = []
    if not node:
        return result
    result.append(node.value)
    preorder(node.left, result)
    preorder(node.right, result)
    return result

def postorder(node, result=None):
    """Left → Right → Root"""
    if result is None:
        result = []
    if not node:
        return result
    postorder(node.left, result)
    postorder(node.right, result)
    result.append(node.value)
    return result

# Build example tree:
#      1
#     / \
#    2   3
#   / \
#  4   5

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print(f"Tree structure:")
print(f"      1")
print(f"     / \\")
print(f"    2   3")
print(f"   / \\")
print(f"  4   5")
print(f"\nInorder (Left-Root-Right):   {inorder(root)}")
print(f"Preorder (Root-Left-Right):  {preorder(root)}")
print(f"Postorder (Left-Right-Root): {postorder(root)}")

# ==================== (2) BFS - Level Order ====================
print("\n[2] BFS - Level Order Traversal")
print("-" * 40)

def level_order(root):
    """Visit nodes level by level"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.value)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result

print(f"Level-order: {level_order(root)}")
print("→ Time: O(n), Space: O(w) where w = max width")

# ==================== (3) Tree Height ====================
print("\n[3] Find Tree Height")
print("-" * 40)

def max_depth(node):
    """Maximum depth from node to leaf"""
    if not node:
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))

height = max_depth(root)
print(f"Tree height: {height}")
print("→ Time: O(n), Space: O(h) recursion stack")

# ==================== (4) Invert Tree ====================
print("\n[4] Invert Binary Tree")
print("-" * 40)

def invert_tree(node):
    """Swap left and right children"""
    if not node:
        return None

    node.left, node.right = node.right, node.left
    invert_tree(node.left)
    invert_tree(node.right)
    return node

# Create copy to invert
root2 = TreeNode(1)
root2.left = TreeNode(2)
root2.right = TreeNode(3)
root2.left.left = TreeNode(4)
root2.left.right = TreeNode(5)

print(f"Before: {inorder(root2)}")
invert_tree(root2)
print(f"After:  {inorder(root2)}")

# ==================== (5) Binary Search Tree ====================
print("\n[5] Binary Search Tree Operations")
print("-" * 40)

class BST:
    """Binary Search Tree"""
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert value in BST"""
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left:
                self._insert_recursive(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert_recursive(node.right, value)
            else:
                node.right = TreeNode(value)

    def search(self, value):
        """Search for value"""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if not node:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

bst = BST()
values = [5, 3, 7, 1, 4, 6, 8]
for val in values:
    bst.insert(val)

print(f"BST (in-order): {inorder(bst.root)}")
print(f"Search for 4: {bst.search(4)}")
print(f"Search for 10: {bst.search(10)}")
print("→ In-order traversal gives sorted order!")

# ==================== (6) Lowest Common Ancestor ====================
print("\n[6] Lowest Common Ancestor (BST)")
print("-" * 40)

def lca_bst(node, p, q):
    """Find LCA in BST"""
    if not node:
        return None

    if p < node.value and q < node.value:
        return lca_bst(node.left, p, q)
    elif p > node.value and q > node.value:
        return lca_bst(node.right, p, q)
    else:
        return node.value  # Found LCA

lca = lca_bst(bst.root, 1, 4)
print(f"LCA of 1 and 4: {lca}")
lca = lca_bst(bst.root, 6, 8)
print(f"LCA of 6 and 8: {lca}")

# ==================== (7) Complexity Comparison ====================
print("\n[7] Complexity Summary")
print("-" * 40)

operations = {
    "Traverse": "O(n)",
    "Search (balanced)": "O(log n)",
    "Search (unbalanced)": "O(n)",
    "Insert": "O(log n) avg",
    "Delete": "O(log n) avg",
}

print(f"{'Operation':<25} {'Time':<15}")
print("-" * 40)
for op, time in operations.items():
    print(f"{op:<25} {time:<15}")

print("\n" + "=" * 60)
print("Next: Solve tree problems and build real applications!")
print("=" * 60)
