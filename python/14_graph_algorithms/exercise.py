"""
Exercises: Advanced Graph Algorithms

Practice Dijkstra, Bellman-Ford, MST, and advanced techniques.
"""

from typing import List, Tuple

print("=" * 70)
print("EXERCISES: Advanced Graph Algorithms")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. DIJKSTRA'S SHORTEST PATH")
print("Input: Graph (adjacency list), start node")
print("Output: Dictionary of shortest distances from start")
def dijkstra_shortest_path(graph: dict, start: int) -> dict:
    # TODO: Implement Dijkstra's algorithm using priority queue
    pass

print("\n2. MINIMUM SPANNING TREE (Kruskal's)")
print("Input: Edges list with weights, number of vertices")
print("Output: MST edges list and total weight")
def kruskal_mst(edges: List[Tuple], vertices: int) -> Tuple[List, int]:
    # TODO: Implement Kruskal's with union-find
    pass

print("\n3. TOPOLOGICAL SORT")
print("Input: DAG as adjacency list, number of vertices")
print("Output: Valid topological ordering")
def topological_sort(graph: dict, vertices: int) -> List[int]:
    # TODO: Implement using DFS
    pass

print("\n4. SHORTEST PATH IN GRID")
print("Input: 2D grid with weights")
print("Output: Shortest distance from top-left to bottom-right")
def shortest_path_grid(grid: List[List[int]]) -> int:
    # TODO: Apply Dijkstra to grid
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. BELLMAN-FORD SHORTEST PATH")
print("Input: Edges list, vertices count, start node")
print("Output: Shortest distances (or None if negative cycle)")
def bellman_ford(edges: List[Tuple], vertices: int, start: int) -> dict:
    # TODO: Implement Bellman-Ford with negative cycle detection
    pass

print("\n6. FLOYD-WARSHALL ALL-PAIRS SHORTEST PATH")
print("Input: Graph adjacency list, vertices count")
print("Output: 2D matrix of all-pairs shortest distances")
def floyd_warshall(graph: dict, vertices: int) -> List[List[int]]:
    # TODO: Implement DP approach for all-pairs
    pass

print("\n7. MINIMUM SPANNING TREE (Prim's)")
print("Input: Graph (adjacency list), start vertex")
print("Output: MST edges list and total weight")
def prims_mst(graph: dict, start: int) -> Tuple[List, int]:
    # TODO: Implement Prim's using priority queue
    pass

print("\n8. NETWORK DELAY TIME")
print("Input: Edges, number of nodes, start node")
print("Output: Time until all nodes receive signal (or -1 if unreachable)")
def network_delay_time(edges: List[Tuple], n: int, k: int) -> int:
    # TODO: Use Dijkstra and find max distance
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n9. STRONGLY CONNECTED COMPONENTS")
print("Input: Directed graph, vertices count")
print("Output: List of SCCs")
def find_scc(graph: dict, vertices: int) -> List[List[int]]:
    # TODO: Implement Kosaraju's or Tarjan's algorithm
    pass

print("\n10. CHEAPEST FLIGHTS WITHIN K STOPS")
print("Input: Flights (u, v, price), n cities, src, dst, k stops")
print("Output: Minimum cost from src to dst with at most k stops")
def cheapest_flights_k_stops(flights: List[Tuple], n: int, src: int, dst: int, k: int) -> int:
    # TODO: Use modified Dijkstra or Bellman-Ford with stop limit
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n11. MINIMUM COST TO CONNECT ALL CITIES")
print("Input: Cost matrix for connecting cities")
print("Output: Minimum total cost to connect all (MST weight)")
def minimum_cost_connect_cities(cost: List[List[int]]) -> int:
    # TODO: Convert to MST problem and use Prim's/Kruskal's
    pass

print("\n12. CRITICAL CONNECTIONS (BRIDGES)")
print("Input: n nodes, connections list (undirected)")
print("Output: List of critical edges whose removal disconnects graph")
def find_critical_connections(n: int, connections: List[Tuple]) -> List[List[int]]:
    # TODO: Use DFS to find bridges (articulation edges)
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Advanced Graph Algorithm Categories:

Shortest Path:
- Dijkstra: O((V+E) log V), non-negative weights
- Bellman-Ford: O(V*E), any weights, detects negatives
- Floyd-Warshall: O(V³), all-pairs, any weights

Minimum Spanning Tree:
- Kruskal's: O(E log E), edge-based, union-find
- Prim's: O(E log V), vertex-based, priority queue

Connectivity:
- Kosaraju: O(V+E), strongly connected components
- Tarjan: O(V+E), SCCs with single DFS
- Bridges: O(V+E), critical edges

Topological Ordering:
- DFS-based: O(V+E), intuitive
- Kahn's algorithm: O(V+E), queue-based

Key Concepts:

1. Priority Queue (Min-Heap):
   - For Dijkstra: extract minimum distance
   - For Prim's: grow MST efficiently
   - Reduces time complexity significantly

2. Union-Find (Disjoint Set Union):
   - Path compression: find becomes O(α(n))
   - Union by rank: faster merging
   - Essential for Kruskal's MST

3. DFS Variations:
   - Finish times (topological sort)
   - Colors (cycle detection)
   - Transpose graph (SCCs)

4. Dynamic Programming:
   - Floyd-Warshall: k-intermediate approach
   - Bellman-Ford: relaxation iterations
   - Both have optimal substructure

Common Mistakes:

1. Using Dijkstra with negative weights (wrong answer)
2. Not detecting negative cycles (Bellman-Ford)
3. Inefficient union-find (without path compression)
4. Wrong MST on disconnected graphs
5. Assuming all nodes reachable (check before)
6. Not handling edge cases (single node, no edges)

Algorithm Selection Guide:

For Single-Source Shortest Path:
✓ Non-negative weights: Dijkstra
✓ Any weights: Bellman-Ford
✓ DAG: Topological sort + relaxation

For All-Pairs Shortest Path:
✓ Small graph (V < 500): Floyd-Warshall
✓ Dijkstra V times: for sparse graphs
✓ Bellman-Ford V times: if negative weights

For Minimum Spanning Tree:
✓ Dense graph (E ≈ V²): Prim's
✓ Sparse graph: Kruskal's
✓ Tie-breaking matters: specify order

For Connectivity:
✓ Strongly connected: Kosaraju or Tarjan
✓ Bridges/Articulation: DFS with discovery time
✓ Biconnected: DFS with low-time values

Interview Tips:

1. Clarify graph properties:
   - Weighted or unweighted?
   - Directed or undirected?
   - Negative weights?
   - Need all-pairs or single-source?

2. Choose algorithm based on:
   - Graph size and density
   - Weight properties
   - Time/space constraints
   - Problem-specific requirements

3. Optimize implementations:
   - Use appropriate data structures
   - Consider constant factors
   - Trade space for time if needed

4. Test edge cases:
   - Single node
   - Disconnected components
   - Negative cycles
   - Large weights
   - Self-loops

Complexity Reference:

Algorithm              Time        Space   Prerequisites
─────────────────────────────────────────────────────────
Dijkstra              O((V+E)logV) O(V)   Priority queue
Bellman-Ford          O(V*E)       O(V)   Edge list
Floyd-Warshall       O(V³)        O(V²)  2D array
Kruskal's MST        O(E logE)    O(V)   Union-find
Prim's MST           O(E logV)    O(V)   Priority queue
Kosaraju SCC         O(V+E)       O(V)   DFS, graph transpose
Tarjan SCC           O(V+E)       O(V)   DFS with stack
Topological Sort     O(V+E)       O(V)   DFS or queue

Real-World Applications:

✓ Google Maps: Dijkstra for fastest route
✓ Financial networks: Bellman-Ford for arbitrage
✓ Network design: MST for minimum cable cost
✓ Compiler: Topological sort for dependency order
✓ Social networks: SCCs for community detection
✓ Power grids: Critical edges (bridges) for vulnerabilities

Practice strategy:

1. Start with Dijkstra (most common)
2. Understand priority queue role
3. Learn Bellman-Ford variations
4. Master union-find for MST
5. Practice graph modeling
6. Solve mixed problem types

Next: Implement graph algorithms and solve real-world problems!
""")
