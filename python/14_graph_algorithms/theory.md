# Graph Algorithms - Advanced Techniques

Master weighted graphs, shortest paths, minimum spanning trees, and complex connectivity.

---

## 1. Weighted Graphs

**Weighted graph**: Edge has associated cost/distance/weight.

```
Graph:  1 --5--> 2
        |        |
        2       3
        |        |
        3 --1--> 3

Weights represent: distance, cost, time, capacity, etc.
```

### Representations:

```python
# Adjacency List with Weights
graph = {
    1: [(2, 5), (3, 2)],    # Node 1: to 2 (cost 5), to 3 (cost 2)
    2: [(3, 3)],            # Node 2: to 3 (cost 3)
    3: []                    # Node 3: no outgoing edges
}

# Edge List
edges = [(1, 2, 5), (1, 3, 2), (2, 3, 3)]  # (from, to, weight)
```

---

## 2. Dijkstra's Algorithm (Shortest Path)

**Algorithm**: Greedy approach using priority queue. Works with non-negative weights.

```python
import heapq

def dijkstra(graph, start):
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
```

**Characteristics**:
- **Time**: O((V + E) log V) with min-heap
- **Space**: O(V)
- **Works with**: Non-negative weights only
- **Best for**: Single-source shortest path in sparse graphs
- **Greedy**: Always picks minimum distance node

**Dijkstra vs BFS**:
- BFS: unweighted shortest path
- Dijkstra: weighted shortest path

---

## 3. Bellman-Ford Algorithm

**Algorithm**: Relaxes edges V-1 times. Works with negative weights, detects negative cycles.

```python
def bellman_ford(graph, start, vertices):
    distances = {v: float('inf') for v in range(vertices)}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(vertices - 1):
        for u in graph:
            for v, weight in graph[u]:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
    
    # Check for negative cycles
    for u in graph:
        for v, weight in graph[u]:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                return None  # Negative cycle exists
    
    return distances
```

**Characteristics**:
- **Time**: O(V × E)
- **Space**: O(V)
- **Works with**: Negative weights, detects negative cycles
- **Slower than**: Dijkstra, but more general
- **Use case**: Currency exchange, arbitrage detection

---

## 4. Floyd-Warshall Algorithm (All-Pairs Shortest Path)

**Algorithm**: Dynamic programming for all-pairs shortest paths.

```python
def floyd_warshall(graph, vertices):
    # Initialize distance matrix
    dist = [[float('inf')] * vertices for _ in range(vertices)]
    
    for i in range(vertices):
        dist[i][i] = 0
    
    for u in graph:
        for v, weight in graph[u]:
            dist[u][v] = weight
    
    # DP: try each vertex as intermediate
    for k in range(vertices):
        for i in range(vertices):
            for j in range(vertices):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist
```

**Characteristics**:
- **Time**: O(V³)
- **Space**: O(V²)
- **Works with**: Negative weights (but no negative cycles)
- **Best for**: All-pairs shortest paths in small dense graphs
- **Better than**: Running Dijkstra V times on small graphs

---

## 5. Minimum Spanning Tree (MST)

**MST**: Subset of edges connecting all vertices with minimum total weight, no cycles.

### Kruskal's Algorithm (Edge-sorting approach)

```python
def kruskal(edges, vertices):
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    parent = list(range(vertices))
    rank = [0] * vertices
    mst = []
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True
    
    for u, v, weight in edges:
        if union(u, v):
            mst.append((u, v, weight))
            if len(mst) == vertices - 1:
                break
    
    return mst
```

**Characteristics**:
- **Time**: O(E log E) for sorting
- **Space**: O(V) for union-find
- **Approach**: Greedy edge-sorting
- **Good for**: Dense graphs

### Prim's Algorithm (Vertex-expansion approach)

```python
import heapq

def prim(graph, start):
    visited = set()
    mst = []
    pq = [(0, start, start)]  # (weight, from, to)
    
    while pq:
        weight, u, v = heapq.heappop(pq)
        
        if v in visited:
            continue
        
        visited.add(v)
        if u != v:
            mst.append((u, v, weight))
        
        for neighbor, w in graph[v]:
            if neighbor not in visited:
                heapq.heappush(pq, (w, v, neighbor))
    
    return mst
```

**Characteristics**:
- **Time**: O(E log V) with heap
- **Space**: O(V)
- **Approach**: Grows tree from vertex
- **Good for**: Dense graphs

---

## 6. Strongly Connected Components (Kosaraju)

**SCC**: Maximal subgraph where every vertex is reachable from every other vertex.

```python
def kosaraju(graph, vertices):
    # Step 1: DFS on original, record finish times
    visited = [False] * vertices
    stack = []
    
    def dfs1(v):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs1(neighbor)
        stack.append(v)
    
    for i in range(vertices):
        if not visited[i]:
            dfs1(i)
    
    # Step 2: DFS on transpose
    reverse_graph = [[] for _ in range(vertices)]
    for u in graph:
        for v in graph[u]:
            reverse_graph[v].append(u)
    
    visited = [False] * vertices
    sccs = []
    
    def dfs2(v, scc):
        visited[v] = True
        scc.append(v)
        for neighbor in reverse_graph[v]:
            if not visited[neighbor]:
                dfs2(neighbor, scc)
    
    while stack:
        v = stack.pop()
        if not visited[v]:
            scc = []
            dfs2(v, scc)
            sccs.append(scc)
    
    return sccs
```

**Characteristics**:
- **Time**: O(V + E)
- **Space**: O(V)
- **Algorithm**: Two DFS passes (original + transpose)
- **Use case**: Detecting cycles, condensation graph

---

## 7. Topological Sort (Advanced)

For DAG (Directed Acyclic Graph), order vertices respecting dependencies.

```python
def topological_sort_dfs(graph, vertices):
    visited = [False] * vertices
    stack = []
    
    def dfs(v):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs(neighbor)
        stack.append(v)
    
    for i in range(vertices):
        if not visited[i]:
            dfs(i)
    
    return stack[::-1]
```

Also Kahn's algorithm (BFS with in-degrees):

```python
def topological_sort_kahn(graph, vertices):
    in_degree = [0] * vertices
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    
    queue = [v for v in range(vertices) if in_degree[v] == 0]
    order = []
    
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return order if len(order) == vertices else None
```

---

## 8. Complexity Comparison

| Algorithm | Time | Space | Works With | Use Case |
|-----------|------|-------|-----------|----------|
| Dijkstra | O((V+E) log V) | O(V) | Non-negative | Single-source shortest |
| Bellman-Ford | O(V×E) | O(V) | Any weights | Negative cycle detection |
| Floyd-Warshall | O(V³) | O(V²) | Any weights | All-pairs shortest |
| Kruskal's MST | O(E log E) | O(V) | Weighted | Minimum spanning tree |
| Prim's MST | O(E log V) | O(V) | Weighted | Minimum spanning tree |
| Kosaraju SCC | O(V+E) | O(V) | Directed | Strong connectivity |
| Topological Sort | O(V+E) | O(V) | DAG | Dependency ordering |

---

## 9. Graph Problem Patterns

### Pattern 1: Shortest Path
- **Unweighted**: BFS
- **Non-negative weights**: Dijkstra
- **Negative weights**: Bellman-Ford
- **All-pairs**: Floyd-Warshall

### Pattern 2: Minimum Spanning Tree
- **Sparse graphs**: Kruskal's (better with sorting)
- **Dense graphs**: Prim's (better with heap)

### Pattern 3: Connectivity
- **Strongly connected**: Kosaraju or Tarjan
- **Biconnected components**: Articulation points

### Pattern 4: Cycle Detection
- **Undirected**: DFS with parent tracking
- **Directed**: DFS with colors (3-coloring)
- **With negatives**: Bellman-Ford

---

## 10. Union-Find (Disjoint Set Union)

Essential for MST and connectivity problems.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # Union by rank
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True
```

**Time**: O(α(n)) ≈ O(1) amortized with path compression and union by rank

---

## 11. Key Takeaways

✅ **Dijkstra**: Non-negative weights, single-source, greedy  
✅ **Bellman-Ford**: Any weights, detects negative cycles  
✅ **Floyd-Warshall**: All-pairs, O(V³), any weights  
✅ **Kruskal's**: MST, edge-sorting, union-find  
✅ **Prim's**: MST, vertex-expansion, priority queue  
✅ **Kosaraju**: Strongly connected components, two DFS  
✅ **Union-Find**: Path compression + union by rank = O(α(n))  
✅ **Topological Sort**: DAG ordering, both DFS and BFS approaches  

**For Interview**:
- Dijkstra most common
- Know Bellman-Ford for negative weights
- Floyd-Warshall for small all-pairs
- Kruskal's/Prim's for MST
- Union-Find essential for efficiency

Next: Implement and apply advanced graph algorithms!
