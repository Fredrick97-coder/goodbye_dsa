"""
Examples: Advanced Graph Algorithms

Demonstrate Dijkstra, Bellman-Ford, MST, and other advanced techniques.
"""

import heapq
from typing import Dict, List, Tuple
from collections import defaultdict

print("=" * 70)
print("ADVANCED GRAPH ALGORITHMS")
print("=" * 70)

# ==================== (1) Dijkstra's Algorithm ====================
print("\n[1] Dijkstra's Algorithm (Shortest Path, Non-Negative Weights)")
print("-" * 70)

def dijkstra(graph: Dict, start: int) -> Dict:
    """Find shortest paths from start to all vertices"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph[curr_node]:
            new_dist = curr_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances

# Test Dijkstra
graph = {
    1: [(2, 4), (3, 2)],
    2: [(3, 1), (4, 5)],
    3: [(4, 8), (5, 10)],
    4: [(5, 2)],
    5: []
}

distances = dijkstra(graph, 1)

print("Graph with weighted edges:")
for node, edges in graph.items():
    print(f"  Node {node}: {edges}")

print("\nShortest distances from node 1:")
for node, dist in sorted(distances.items()):
    print(f"  1 → {node}: {dist}")

print("→ Time: O((V + E) log V), Space: O(V)")
print("→ Greedy approach, guaranteed optimal for non-negative weights")

# ==================== (2) Bellman-Ford Algorithm ====================
print("\n[2] Bellman-Ford Algorithm (Handles Negative Weights)")
print("-" * 70)

def bellman_ford(edges: List[Tuple], vertices: int, start: int) -> Dict:
    """Find shortest paths, detect negative cycles"""
    distances = {i: float('inf') for i in range(vertices)}
    distances[start] = 0

    # Relax edges V-1 times
    for _ in range(vertices - 1):
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    # Check for negative cycles
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None  # Negative cycle detected

    return distances

# Test Bellman-Ford
edges = [(0, 1, 4), (0, 2, 2), (1, 2, -3), (2, 3, 2), (1, 3, 1)]
distances = bellman_ford(edges, 4, 0)

print("Edges: (u, v, weight)")
for u, v, w in edges:
    print(f"  {u} → {v}: {w}")

print("\nShortest distances from node 0:")
if distances:
    for node, dist in sorted(distances.items()):
        print(f"  0 → {node}: {dist}")
else:
    print("  Negative cycle detected!")

print("→ Time: O(V × E), Space: O(V)")
print("→ Slower but handles negative weights and detects cycles")

# ==================== (3) Floyd-Warshall Algorithm ====================
print("\n[3] Floyd-Warshall Algorithm (All-Pairs Shortest Path)")
print("-" * 70)

def floyd_warshall(graph: List[List[int]], vertices: int) -> List[List[int]]:
    """Find all-pairs shortest paths"""
    dist = [[float('inf')] * vertices for _ in range(vertices)]

    for i in range(vertices):
        dist[i][i] = 0

    # Initialize with direct edges
    for u in range(len(graph)):
        for v, weight in graph[u]:
            dist[u][v] = weight

    # DP: try each vertex as intermediate
    for k in range(vertices):
        for i in range(vertices):
            for j in range(vertices):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Test Floyd-Warshall
graph_fw = {
    0: [(1, 3), (3, 7)],
    1: [(2, 1)],
    2: [(3, 2)],
    3: []
}

# Convert to adjacency for Floyd-Warshall
adj = [[] for _ in range(4)]
for u in graph_fw:
    adj[u] = graph_fw[u]

dist_matrix = floyd_warshall(adj, 4)

print("All-pairs shortest path matrix:")
print(f"  {'To':>3}", end="")
for j in range(4):
    print(f"{j:>6}", end="")
print()

for i in range(4):
    print(f"{i:>3}", end="")
    for j in range(4):
        val = dist_matrix[i][j]
        if val == float('inf'):
            print(f"{'∞':>6}", end="")
        else:
            print(f"{int(val):>6}", end="")
    print()

print("→ Time: O(V³), Space: O(V²)")
print("→ Finds all-pairs shortest paths in one pass")

# ==================== (4) Kruskal's Algorithm (MST) ====================
print("\n[4] Kruskal's Algorithm (Minimum Spanning Tree)")
print("-" * 70)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

def kruskal(edges: List[Tuple], vertices: int) -> List[Tuple]:
    """Find minimum spanning tree"""
    edges.sort(key=lambda x: x[2])
    uf = UnionFind(vertices)
    mst = []
    total_weight = 0

    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight
            if len(mst) == vertices - 1:
                break

    return mst, total_weight

# Test Kruskal
edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
mst, total = kruskal(edges.copy(), 4)

print("Edges: (u, v, weight)")
for u, v, w in edges:
    print(f"  {u} - {v}: {w}")

print("\nMinimum spanning tree (Kruskal's):")
for u, v, w in mst:
    print(f"  {u} - {v}: {w}")
print(f"Total weight: {total}")

print("→ Time: O(E log E), Space: O(V)")
print("→ Edge-based approach with union-find")

# ==================== (5) Prim's Algorithm (MST) ====================
print("\n[5] Prim's Algorithm (Minimum Spanning Tree)")
print("-" * 70)

def prim(graph: Dict, start: int) -> Tuple[List, int]:
    """Find minimum spanning tree using Prim's"""
    visited = set()
    mst = []
    pq = [(0, start, start)]  # (weight, from, to)
    total_weight = 0

    while pq:
        weight, u, v = heapq.heappop(pq)

        if v in visited:
            continue

        visited.add(v)
        if u != v:
            mst.append((u, v, weight))
            total_weight += weight

        for neighbor, w in graph[v]:
            if neighbor not in visited:
                heapq.heappush(pq, (w, v, neighbor))

    return mst, total_weight

# Test Prim
graph_prim = {
    0: [(1, 10), (2, 6), (3, 5)],
    1: [(0, 10), (3, 15)],
    2: [(0, 6), (3, 4)],
    3: [(0, 5), (1, 15), (2, 4)]
}

mst_prim, total_prim = prim(graph_prim, 0)

print("Minimum spanning tree (Prim's):")
for u, v, w in mst_prim:
    print(f"  {u} - {v}: {w}")
print(f"Total weight: {total_prim}")

print("→ Time: O(E log V), Space: O(V)")
print("→ Vertex-based approach with priority queue")
print("→ Same result as Kruskal's, different approach")

# ==================== (6) Kosaraju's Algorithm (SCC) ====================
print("\n[6] Kosaraju's Algorithm (Strongly Connected Components)")
print("-" * 70)

def kosaraju(graph: Dict, vertices: int) -> List[List[int]]:
    """Find all strongly connected components"""
    # Step 1: DFS on original, record finish times
    visited = [False] * vertices
    stack = []

    def dfs1(v):
        visited[v] = True
        for neighbor in graph.get(v, []):
            if not visited[neighbor]:
                dfs1(neighbor)
        stack.append(v)

    for i in range(vertices):
        if not visited[i]:
            dfs1(i)

    # Step 2: DFS on transpose
    transpose = [[] for _ in range(vertices)]
    for u in graph:
        for v in graph[u]:
            transpose[v].append(u)

    visited = [False] * vertices
    sccs = []

    def dfs2(v, scc):
        visited[v] = True
        scc.append(v)
        for neighbor in transpose[v]:
            if not visited[neighbor]:
                dfs2(neighbor, scc)

    while stack:
        v = stack.pop()
        if not visited[v]:
            scc = []
            dfs2(v, scc)
            sccs.append(sorted(scc))

    return sccs

# Test Kosaraju
graph_scc = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [1]
}

sccs = kosaraju(graph_scc, 4)

print("Directed graph edges:")
for u in graph_scc:
    for v in graph_scc[u]:
        print(f"  {u} → {v}")

print("\nStrongly connected components:")
for i, scc in enumerate(sccs):
    print(f"  SCC {i}: {scc}")

print("→ Time: O(V + E), Space: O(V)")
print("→ Two DFS passes: original and transpose")

# ==================== (7) Topological Sort ====================
print("\n[7] Topological Sort (DAG Ordering)")
print("-" * 70)

def topological_sort(graph: Dict, vertices: int) -> List[int]:
    """Sort DAG vertices respecting dependencies"""
    visited = [False] * vertices
    stack = []

    def dfs(v):
        visited[v] = True
        for neighbor in graph.get(v, []):
            if not visited[neighbor]:
                dfs(neighbor)
        stack.append(v)

    for i in range(vertices):
        if not visited[i]:
            dfs(i)

    return stack[::-1]

# Test topological sort
graph_topo = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: []
}

order = topological_sort(graph_topo, 4)

print("DAG edges (dependency: u → v means u before v):")
for u in graph_topo:
    for v in graph_topo[u]:
        print(f"  {u} → {v}")

print(f"\nTopological order: {order}")
print("→ Time: O(V + E), Space: O(V)")
print("→ Used for: task scheduling, dependency resolution")

# ==================== (8) Complexity Comparison ====================
print("\n[8] Algorithm Complexity Comparison")
print("-" * 70)

algorithms = {
    "Dijkstra": ("O((V+E) log V)", "O(V)", "Non-negative", "Single-source"),
    "Bellman-Ford": ("O(V×E)", "O(V)", "Any", "Negative detection"),
    "Floyd-Warshall": ("O(V³)", "O(V²)", "Any", "All-pairs"),
    "Kruskal's MST": ("O(E log E)", "O(V)", "Weighted", "MST"),
    "Prim's MST": ("O(E log V)", "O(V)", "Weighted", "MST"),
    "Kosaraju SCC": ("O(V+E)", "O(V)", "Directed", "Connectivity"),
}

print(f"{'Algorithm':<20} {'Time':<18} {'Space':<12} {'Weights':<12} {'Use':<15}")
print("-" * 77)

for algo, (time, space, weights, use) in algorithms.items():
    print(f"{algo:<20} {time:<18} {space:<12} {weights:<12} {use:<15}")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
