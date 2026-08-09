"""
Exercises: Binary Trees and BST

Practice tree operations and solve common problems.
"""

from typing import Optional, List

print("=" * 60)
print("EXERCISES: Binary Trees & BST")
print("=" * 60)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

print("\n1. INORDER TRAVERSAL")
print("Input: Binary tree")
print("Output: [Left → Root → Right] values")
def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    # TODO: Implement
    pass

print("\n2. MAXIMUM DEPTH")
print("Input: Binary tree")
print("Output: Maximum depth (height)")
def max_depth(root: Optional[TreeNode]) -> int:
    # TODO: Implement
    pass

print("\n3. INVERT BINARY TREE")
print("Input: Binary tree")
print("Output: Tree with left/right swapped")
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # TODO: Implement
    pass

print("\n4. VALIDATE BST")
print("Input: Binary tree")
print("Output: Is valid BST?")
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    # TODO: Implement
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

print("\n5. LEVEL ORDER TRAVERSAL")
print("Input: Binary tree")
print("Output: List of lists (each level)")
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    # TODO: Implement using queue
    pass

print("\n6. LOWEST COMMON ANCESTOR (BST)")
print("Input: BST, two nodes p and q")
print("Output: LCA value")
def lowest_common_ancestor(root: Optional[TreeNode], p: int, q: int) -> int:
    # TODO: Implement
    pass

print("\n7. PATH SUM")
print("Input: Tree, target sum")
print("Output: Is there root-to-leaf path with sum?")
def path_sum(root: Optional[TreeNode], target: int) -> bool:
    # TODO: Implement
    pass

print("\n8. ZIGZAG LEVEL ORDER")
print("Input: Binary tree")
print("Output: Levels alternating left-to-right and right-to-left")
def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    # TODO: Implement
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

print("\n9. BINARY TREE MAXIMUM PATH SUM")
print("Input: Binary tree")
print("Output: Maximum path sum (any two nodes)")
def max_path_sum(root: Optional[TreeNode]) -> int:
    # TODO: Implement
    pass

print("\n10. SERIALIZE/DESERIALIZE TREE")
print("Input: Binary tree or serialized string")
print("Output: String or reconstructed tree")
def serialize(root: Optional[TreeNode]) -> str:
    # TODO: Implement
    pass

def deserialize(data: str) -> Optional[TreeNode]:
    # TODO: Implement
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

print("\n11. VERTICAL ORDER TRAVERSAL")
print("Input: Binary tree")
print("Output: Nodes grouped by vertical position")
def vertical_order(root: Optional[TreeNode]) -> List[List[int]]:
    # TODO: Implement
    pass

print("\n12. RECONSTRUCT TREE FROM INORDER & PREORDER")
print("Input: Inorder and preorder traversals")
print("Output: Reconstructed binary tree")
def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    # TODO: Implement
    pass

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Tree Concepts:
- Inorder: Left → Root → Right (sorted for BST)
- Preorder: Root → Left → Right (useful for reconstruction)
- Postorder: Left → Right → Root (bottom-up processing)
- Level-order: BFS with queue

Key Problems:
- Max depth, invert tree, validate BST
- Level-order traversals (zigzag, vertical)
- LCA, path sum, max path sum
- Serialize/deserialize
- Tree reconstruction

Patterns:
- Recursion for DFS
- Queue for BFS
- In-order for sorted BST
- Two nodes/pointers for paths

Next: Complete project building real tree applications
""")
