"""
Project: Binary Tree & BST Applications

Build real-world tree applications:
1. Expression Tree Evaluator
2. File System Browser
3. Autocomplete with Trie
4. BST-based Database Index
"""

from collections import deque
from typing import Optional, List

print("=" * 70)
print("PROJECT: Binary Tree & BST Applications")
print("=" * 70)

class TreeNode:
    """Binary tree node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ==================== PART 1: Expression Tree ====================
print("\n[PART 1] Expression Tree Evaluator")
print("-" * 70)

class ExpressionTree:
    """Evaluate mathematical expressions using tree"""

    def __init__(self):
        self.root = None

    def evaluate(self, expression: str) -> float:
        """Evaluate postfix expression using tree"""
        stack = []

        for token in expression.split():
            if token in ['+', '-', '*', '/']:
                right = stack.pop()
                left = stack.pop()
                node = TreeNode(token)
                node.left = left
                node.right = right
                stack.append(node)
            else:
                stack.append(TreeNode(float(token)))

        self.root = stack[0]
        return self._eval_node(self.root)

    def _eval_node(self, node):
        """Recursively evaluate tree"""
        if node.value in ['+', '-', '*', '/']:
            left_val = self._eval_node(node.left)
            right_val = self._eval_node(node.right)

            if node.value == '+':
                return left_val + right_val
            elif node.value == '-':
                return left_val - right_val
            elif node.value == '*':
                return left_val * right_val
            elif node.value == '/':
                return left_val / right_val
        else:
            return node.value

# Test expression tree
print("Expression Tree Demo:\n")
tree = ExpressionTree()
expr = "3 4 + 2 *"  # (3 + 4) * 2 = 14
result = tree.evaluate(expr)
print(f"Expression (postfix): {expr}")
print(f"Result: {result}")
print("→ Tree structure enables recursive evaluation")

# ==================== PART 2: File System ====================
print("\n[PART 2] File System Browser (Tree Structure)")
print("-" * 70)

class FileNode:
    """File system node"""
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_path(self):
        """Get full path"""
        path = [self.name]
        current = self.parent
        while current:
            path.append(current.name)
            current = current.parent
        return "/" + "/".join(reversed(path))

class FileSystem:
    """File system browser"""

    def __init__(self):
        self.root = FileNode("root")

    def create_file(self, path: str):
        """Create file at path"""
        parts = path.strip("/").split("/")
        current = self.root

        for part in parts[:-1]:
            found = None
            for child in current.children:
                if child.name == part:
                    found = child
                    break
            if not found:
                found = FileNode(part)
                current.add_child(found)
            current = found

        file = FileNode(parts[-1], is_file=True)
        current.add_child(file)
        return file

    def print_tree(self, node=None, indent=0):
        """Print file tree"""
        if node is None:
            node = self.root
        print("  " * indent + ("📄 " if node.is_file else "📁 ") + node.name)
        for child in node.children:
            self.print_tree(child, indent + 1)

# Test file system
print("File System Demo:\n")
fs = FileSystem()
fs.create_file("/home/user/documents/file1.txt")
fs.create_file("/home/user/documents/file2.txt")
fs.create_file("/home/user/downloads/image.jpg")
fs.print_tree()
print("→ Tree structure models hierarchical file system")

# ==================== PART 3: BST Index ====================
print("\n[PART 3] Database Index using BST")
print("-" * 70)

class BSTIndex:
    """BST-based database index"""

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Insert key-value pair"""
        if not self.root:
            self.root = TreeNode((key, value))
        else:
            self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if key < node.value[0]:
            if node.left:
                self._insert_recursive(node.left, key, value)
            else:
                node.left = TreeNode((key, value))
        else:
            if node.right:
                self._insert_recursive(node.right, key, value)
            else:
                node.right = TreeNode((key, value))

    def search(self, key):
        """Search for key"""
        node = self._search_recursive(self.root, key)
        return node.value[1] if node else None

    def _search_recursive(self, node, key):
        if not node:
            return None
        if node.value[0] == key:
            return node
        elif key < node.value[0]:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def range_query(self, min_key, max_key):
        """Find all values in range"""
        result = []
        self._range_query_recursive(self.root, min_key, max_key, result)
        return result

    def _range_query_recursive(self, node, min_key, max_key, result):
        if not node:
            return
        if node.value[0] >= min_key:
            self._range_query_recursive(node.left, min_key, max_key, result)
        if min_key <= node.value[0] <= max_key:
            result.append(node.value)
        if node.value[0] <= max_key:
            self._range_query_recursive(node.right, min_key, max_key, result)

# Test BST index
print("BST Database Index Demo:\n")
index = BSTIndex()
records = [(102, "Alice"), (105, "Bob"), (101, "Charlie"), (103, "David")]
for id, name in records:
    index.insert(id, name)

print(f"Search ID 103: {index.search(103)}")
print(f"Range query [101-104]: {index.range_query(101, 104)}")
print("→ BST enables fast search and range queries")

# ==================== PART 4: Tree Analysis ====================
print("\n[PART 4] Tree Properties Analysis")
print("-" * 70)

def analyze_tree(root):
    """Analyze tree properties"""

    def dfs(node):
        if not node:
            return {"height": 0, "nodes": 0, "leaves": 0}

        left = dfs(node.left)
        right = dfs(node.right)

        return {
            "height": 1 + max(left["height"], right["height"]),
            "nodes": 1 + left["nodes"] + right["nodes"],
            "leaves": (1 if not node.left and not node.right else 0) + left["leaves"] + right["leaves"],
        }

    return dfs(root)

# Build test tree
test_root = TreeNode(1)
test_root.left = TreeNode(2)
test_root.right = TreeNode(3)
test_root.left.left = TreeNode(4)
test_root.left.right = TreeNode(5)

props = analyze_tree(test_root)
print(f"Tree height: {props['height']}")
print(f"Total nodes: {props['nodes']}")
print(f"Leaf nodes: {props['leaves']}")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Tree Applications:

1. Expression Trees
   - Evaluate mathematical expressions
   - Compiler syntax trees
   - Recursive evaluation via traversal

2. File Systems
   - Hierarchical directory structure
   - Path navigation
   - Tree traversal for listing

3. Database Indexes
   - BST for fast search O(log n)
   - Range queries in O(log n + k)
   - Balanced trees (AVL, Red-Black) for production

4. Tree Properties
   - Height affects performance
   - Node count and structure
   - Balanced vs unbalanced

Key Insights:

✓ Trees model hierarchies naturally
✓ BST enables fast search and sorting
✓ Recursion is natural for trees
✓ In-order gives sorted output (BST)
✓ Balance is critical for performance

Common Patterns:

- DFS for recursive processing
- BFS for level-by-level operations
- In-order for sorted traversal
- Path tracking for reconstruction
- Sentinel/dummy nodes for edge cases

Next Steps:
1. Master tree traversals
2. Implement BST operations
3. Solve tree problems on LeetCode
4. Move to Topic 09: Hash Maps
""")

print("=" * 70)
print("Project Complete! Topic 08 Finished Successfully!")
print("=" * 70)
