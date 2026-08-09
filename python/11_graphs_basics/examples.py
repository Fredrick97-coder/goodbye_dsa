"""
Examples: Graph Traversal & Basic Algorithms

Demonstrate DFS, BFS, connectivity, and cycle detection.
"""

from collections import deque, defaultdict
from typing import List, Set, Dict, Tuple

print("=" * 60)
print("GRAPHS - TRAVERSAL & BASIC ALGORITHMS")
print("=" * 60)

# ==================== (1) Graph Representations ====================
print("\n[1] Graph Representations")
print("-" * 40)

# Adjacency List (most common for sparse graphs)
graph_list = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# Adjacency Matrix
graph_matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

print("Graph structure:")
print("    0")
print("   / \\")
print("  1 - 2")
print("   \\ /")
print("    3")

print("\nAdjacency List:", graph_list)
print("Space: O(V + E)")

print("\nAdjacency Matrix:")
for row in graph_matrix:
    print(" ", row)
print("Space: O(V²)")

print("→ List: better for sparse graphs")
print("→ Matrix: better for dense graphs, O(1) edge check")

# ==================== (2) Depth-First Search (DFS) ====================
print("\n[2] Depth-First Search (DFS)")
print("-" * 40)

def dfs_recursive(graph: Dict, start: int, visited: Set = None) -> Set:
    """Recursive DFS traversal"""
    if visited is None:
        visited = set()

    visited.add(start)
    print(f"{start}", end=" ")

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    return visited

def dfs_iterative(graph: Dict, start: int) -> Set:
    """Iterative DFS using stack"""
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            print(f"{vertex}", end=" ")
            # Add neighbors in reverse to maintain order
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited

print("DFS (Recursive):", end=" ")
dfs_recursive(graph_list, 0)
print()

print("DFS (Iterative): ", end=" ")
dfs_iterative(graph_list, 0)
print()

print("→ Time: O(V + E), Space: O(V)")
print("→ Uses stack (recursion or explicit)")

# ==================== (3) Breadth-First Search (BFS) ====================
print("\n[3] Breadth-First Search (BFS)")
print("-" * 40)

def bfs(graph: Dict, start: int) -> Set:
    """BFS traversal using queue"""
    visited = {start}
    queue = deque([start])

    print(f"{start}", end=" ")

    while queue:
        vertex = queue.popleft()

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                print(f"{neighbor}", end=" ")

    return visited

print("BFS: ", end=" ")
bfs(graph_list, 0)
print()

print("→ Time: O(V + E), Space: O(V)")
print("→ Uses queue for level-order traversal")

# ==================== (4) Connected Components ====================
print("\n[4] Count Connected Components")
print("-" * 40)

def count_components(n: int, edges: List[Tuple]) -> int:
    """Count number of connected components"""
    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = 0

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            dfs(i)
            components += 1

    return components

# Graph with 2 components: {0,1,2} and {3,4}
edges = [(0, 1), (1, 2), (3, 4)]
n = 5
components = count_components(n, edges)

print(f"Nodes: {n}, Edges: {edges}")
print(f"Connected components: {components}")
print("→ Component 1: {0, 1, 2}")
print("→ Component 2: {3, 4}")

print("→ Time: O(V + E), Space: O(V)")

# ==================== (5) Cycle Detection (Undirected) ====================
print("\n[5] Cycle Detection in Undirected Graph")
print("-" * 40)

def has_cycle_undirected(n: int, edges: List[Tuple]) -> bool:
    """Detect cycle in undirected graph"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    def dfs(node, parent):
        visited[node] = True

        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Found back edge (cycle)
                return True

        return False

    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True

    return False

# Test with cycle
print("Graph with cycle (1-2-3-1):")
edges_cycle = [(0, 1), (1, 2), (2, 3), (3, 1)]
result = has_cycle_undirected(4, edges_cycle)
print(f"  Has cycle: {result}")

# Test without cycle
print("Graph without cycle (0-1-2):")
edges_no_cycle = [(0, 1), (1, 2)]
result = has_cycle_undirected(3, edges_no_cycle)
print(f"  Has cycle: {result}")

print("→ Time: O(V + E), Space: O(V)")
print("→ Checks for back edges (edge to non-parent visited node)")

# ==================== (6) Topological Sort ====================
print("\n[6] Topological Sort (Directed Acyclic Graph)")
print("-" * 40)

def topological_sort(n: int, edges: List[Tuple]) -> List[int]:
    """Topological sort using DFS"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = [False] * n
    stack = []

    def dfs(node):
        visited[node] = True

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

        stack.append(node)

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return stack[::-1]

# Tasks with dependencies: 0→1, 0→2, 1→3, 2→3
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
order = topological_sort(4, edges)

print("Task dependencies: 0→1, 0→2, 1→3, 2→3")
print(f"Topological order: {order}")
print("→ Do task 0 first, then 1 and 2 (in any order), then 3")

print("→ Time: O(V + E), Space: O(V)")
print("→ Only valid for DAGs (Directed Acyclic Graphs)")

# ==================== (7) Shortest Path (Unweighted) ====================
print("\n[7] Shortest Path (Unweighted Graph)")
print("-" * 40)

def shortest_path(graph: Dict, start: int, end: int) -> List[int]:
    """Find shortest path using BFS"""
    if start == end:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return path + [neighbor]

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

# Find path from 0 to 3
path = shortest_path(graph_list, 0, 3)
print(f"Graph: 0-1-2-3 (square)")
print(f"Shortest path from 0 to 3: {path}")
print(f"Distance: {len(path) - 1} edges")

print("→ Time: O(V + E), Space: O(V)")
print("→ BFS guarantees shortest path in unweighted graphs")

# ==================== (8) Bipartite Check ====================
print("\n[8] Check if Graph is Bipartite")
print("-" * 40)

def is_bipartite(n: int, edges: List[Tuple]) -> bool:
    """Check if graph can be 2-colored"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n  # -1: unvisited, 0: color A, 1: color B

    def bfs_color(start):
        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False

        return True

    for i in range(n):
        if color[i] == -1:
            if not bfs_color(i):
                return False

    return True

# Test bipartite
print("Graph: 0-1-2 (line)")
edges = [(0, 1), (1, 2)]
result = is_bipartite(3, edges)
print(f"  Bipartite: {result}")
print(f"  Colors: 0→A, 1→B, 2→A")

print("Graph: 0-1-2-0 (triangle, odd cycle)")
edges_odd = [(0, 1), (1, 2), (2, 0)]
result = is_bipartite(3, edges_odd)
print(f"  Bipartite: {result}")

print("→ Time: O(V + E), Space: O(V)")
print("→ A graph is bipartite iff it has no odd-length cycles")

# ==================== (9) Complexity Summary ====================
print("\n[9] Graph Algorithm Complexity Summary")
print("-" * 40)

algorithms = {
    "DFS": ("O(V+E)", "O(V)", "Path, cycle, topological"),
    "BFS": ("O(V+E)", "O(V)", "Shortest path, levels"),
    "Components": ("O(V+E)", "O(V)", "Count/identify components"),
    "Cycle detect": ("O(V+E)", "O(V)", "Check for cycles"),
    "Topological": ("O(V+E)", "O(V)", "DAG ordering"),
    "Bipartite": ("O(V+E)", "O(V)", "2-coloring check"),
}

print(f"{'Algorithm':<20} {'Time':<12} {'Space':<12} {'Use':<25}")
print("-" * 69)
for algo, (time, space, use) in algorithms.items():
    print(f"{algo:<20} {time:<12} {space:<12} {use:<25}")

print("\n" + "=" * 60)
print("Next: Solve graph problems and build applications!")
print("=" * 60)
