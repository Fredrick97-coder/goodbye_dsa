# Trees - Hierarchical Data Structures

Master binary trees, binary search trees, and tree traversals.

---

## 1. What is a Tree?

A **tree** is a hierarchical data structure with:
- **Root**: Top node (no parent)
- **Nodes**: Connected entities
- **Edges**: Links between nodes
- **Parent/Child**: Hierarchical relationships
- **Leaf**: Node with no children

```
       1 (root)
      / \
     2   3
    / \
   4   5
  (leaf nodes)
```

---

## 2. Binary Tree

A tree where each node has **at most 2 children** (left and right).

### Properties:
- **Height**: Longest path from root to leaf
- **Depth**: Distance from root to node
- **Balanced**: Left and right subtrees roughly equal height

### Types:
- **Full Binary Tree**: Every node has 0 or 2 children
- **Complete Binary Tree**: Filled level by level
- **Perfect Binary Tree**: All levels completely filled
- **Skewed Tree**: Like a linked list (worst case)

---

## 3. Node Structure

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```

---

## 4. Tree Traversals

### Depth-First (DFS):

**In-Order** (Left → Root → Right): 4 2 5 1 3
```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    print(node.value)
    inorder(node.right)
```

**Pre-Order** (Root → Left → Right): 1 2 4 5 3
```python
def preorder(node):
    if not node:
        return
    print(node.value)
    preorder(node.left)
    preorder(node.right)
```

**Post-Order** (Left → Right → Root): 4 5 2 3 1
```python
def postorder(node):
    if not node:
        return
    postorder(node.left)
    postorder(node.right)
    print(node.value)
```

### Breadth-First (BFS):

**Level-Order**: 1 2 3 4 5 (uses queue)
```python
def level_order(root):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

---

## 5. Binary Search Tree (BST)

A binary tree where:
- **Left child < Parent**
- **Right child > Parent**
- **Enables fast searching**

### Operations:

| Operation | Time | Description |
|-----------|------|-------------|
| Search | O(log n) avg | Binary search-like |
| Insert | O(log n) avg | Find position, add |
| Delete | O(log n) avg | Find, remove node |
| Traverse | O(n) | Visit all nodes |

### Properties:
- In-order traversal gives **sorted order**
- Can become unbalanced (linked list worst case)
- Height can be O(log n) optimal or O(n) worst case

---

## 6. Common Tree Problems

### Problem 1: Max Depth
Find the height of the tree.
```
Time: O(n), Space: O(h) where h = height
```

### Problem 2: Invert Tree
Flip left and right children.
```
    1              1
   / \    →       / \
  2   3          3   2
```

### Problem 3: Lowest Common Ancestor (LCA)
Find deepest node that's ancestor of both target nodes.

### Problem 4: Path Sum
Check if path from root to leaf sums to target.

---

## 7. Tree Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Traversal | O(n) | O(h) |
| Search (BST) | O(log n) avg | O(1) |
| Insert (BST) | O(log n) avg | O(1) |
| Delete (BST) | O(log n) avg | O(1) |

**Worst case (unbalanced)**: All operations O(n)

---

## 8. Key Patterns

### Pattern 1: Recursion
Trees are naturally recursive.
```python
def dfs(node):
    if not node:
        return
    # Process node
    dfs(node.left)
    dfs(node.right)
```

### Pattern 2: Queue for Level-Order
Use deque for efficient BFS.

### Pattern 3: In-Order for Sorted
In-order traversal of BST gives sorted sequence.

---

## 9. Key Takeaways

✅ **Tree**: Hierarchical structure with root and children  
✅ **Binary Tree**: Each node has ≤2 children  
✅ **BST**: Left < Parent < Right  
✅ **Traversals**: DFS (in/pre/post-order), BFS (level-order)  
✅ **Complexity**: O(log n) for balanced, O(n) for skewed  
✅ **Recursion**: Natural fit for tree problems  

Next: Implement trees and solve common problems!
