"""
Exercises: Graph Traversal & Basic Algorithms

Practice DFS, BFS, connectivity, and graph problems.
"""

from typing import List, Tuple

print("=" * 60)
print("EXERCISES: Graph Traversal & Algorithms")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

print("\n1. GRAPH TRAVERSAL (DFS)")
print("Input: Graph (adjacency list), starting node")
print("Output: List of visited nodes in DFS order")
def dfs_traversal(graph: dict, start: int) -> List[int]:
    # TODO: Implement DFS traversal
    pass

print("\n2. GRAPH TRAVERSAL (BFS)")
print("Input: Graph (adjacency list), starting node")
print("Output: List of visited nodes in BFS order")
def bfs_traversal(graph: dict, start: int) -> List[int]:
    # TODO: Implement BFS traversal
    pass

print("\n3. NUMBER OF CONNECTED COMPONENTS")
print("Input: n (nodes), edges list")
print("Output: Number of connected components")
def num_connected_components(n: int, edges: List[Tuple]) -> int:
    # TODO: Implement using DFS/BFS
    pass

print("\n4. FIND CONNECTED COMPONENT")
print("Input: Graph, node n")
print("Output: All nodes in same component as n")
def find_component(graph: dict, n: int) -> List[int]:
    # TODO: Implement DFS to find all connected nodes
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

print("\n5. CYCLE DETECTION (UNDIRECTED)")
print("Input: n (nodes), edges list")
print("Output: Is there a cycle?")
def has_cycle_undirected(n: int, edges: List[Tuple]) -> bool:
    # TODO: Implement cycle detection with DFS
    pass

print("\n6. CYCLE DETECTION (DIRECTED)")
print("Input: n (nodes), edges list (directed)")
print("Output: Is there a cycle?")
def has_cycle_directed(n: int, edges: List[Tuple]) -> bool:
    # TODO: Implement with color marking (white/gray/black)
    pass

print("\n7. SHORTEST PATH (UNWEIGHTED)")
print("Input: Graph, start, end")
print("Output: Shortest path list")
def shortest_path(graph: dict, start: int, end: int) -> List[int]:
    # TODO: Implement using BFS
    pass

print("\n8. TOPOLOGICAL SORT")
print("Input: n (nodes), edges (DAG)")
print("Output: Valid topological ordering")
def topological_sort(n: int, edges: List[Tuple]) -> List[int]:
    # TODO: Implement DFS-based topological sort
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

print("\n9. WORD LADDER")
print("Input: beginWord, endWord, wordList")
print("Output: Shortest transformation sequence length")
def ladder_length(begin: str, end: str, word_list: List[str]) -> int:
    # TODO: Implement as graph shortest path problem
    pass

print("\n10. BIPARTITE GRAPH CHECK")
print("Input: n (nodes), edges")
print("Output: Is graph bipartite (2-colorable)?")
def is_bipartite(n: int, edges: List[Tuple]) -> bool:
    # TODO: Implement graph 2-coloring with BFS
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

print("\n11. ALIEN DICTIONARY")
print("Input: List of words in alien language order")
print("Output: Character order in alien dictionary")
def alien_order(words: List[str]) -> str:
    # TODO: Build graph from word comparisons, topological sort
    pass

print("\n12. COURSE SCHEDULE (WITH DETECTION)")
print("Input: numCourses, prerequisites (edges)")
print("Output: Valid course order, or None if cycle exists")
def find_order(num_courses: int, prereqs: List[Tuple]) -> List[int]:
    # TODO: Topological sort with cycle detection
    pass

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Graph Fundamentals:
- Vertices and edges
- Directed vs undirected
- Adjacency list vs matrix
- Connected components

Graph Traversals:
- DFS (recursive/iterative): O(V+E)
- BFS (queue-based): O(V+E)
- Both find all reachable nodes

Key Problems:
- Connected components (DFS/BFS)
- Cycle detection (DFS with colors)
- Shortest path unweighted (BFS)
- Topological sort (DFS, DAG only)
- Bipartite check (2-coloring)
- Path existence (DFS)

Patterns:
- Build adjacency list from edges
- Use visited set to track processed nodes
- DFS for recursion/backtracking
- BFS for shortest path
- Color marking for directed cycles
- Convert problem to graph problem

Time Complexity:
- All basic algorithms: O(V + E)
- Where V = vertices, E = edges

Space Complexity:
- DFS: O(V) for recursion stack
- BFS: O(V) for queue
- Storage: O(V + E) for adjacency list

Common Pitfalls:
- Forgetting to mark visited (infinite loop)
- Not handling disconnected components
- Mixing parent with visited in undirected cycle
- Assuming all nodes reachable from start
- Not converting problem to graph format

Next: Complete project with real graph applications
""")
