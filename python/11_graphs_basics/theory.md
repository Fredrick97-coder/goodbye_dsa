# Graphs - Traversal & Connectivity

Master fundamental graph concepts, representations, and traversal algorithms.

---

## 1. What is a Graph?

A **graph** is a data structure consisting of:
- **Vertices (Nodes)**: Entities in the graph
- **Edges**: Connections between vertices

### Graph Components:
```
Graph: 1 — 2 — 4
       |   |   /
       3 —— /

Vertices: {1, 2, 3, 4}
Edges: {(1,2), (1,3), (2,3), (2,4), (3,4)}
```

### Graph Types:

| Type | Direction | Weights | Example |
|------|-----------|---------|---------|
| Undirected | Both ways | None | Friendship |
| Directed | One way | None | Following |
| Weighted | One way | Yes | Road distance |
| Mixed | Both | Yes | Flight cost |

---

## 2. Graph Representations

### Representation 1: Adjacency List
Store neighbors for each vertex.

```python
# Using dictionary
graph = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3]
}
```

**Pros**:
- ✓ Memory efficient O(V + E)
- ✓ Fast neighbor lookup O(1)
- ✓ Good for sparse graphs

**Cons**:
- ✗ Checking edge existence O(degree)

### Representation 2: Adjacency Matrix
2D array where matrix[i][j] = edge from i to j.

```python
# Using 2D list
graph = [
    [0, 1, 1, 0],  # Node 0: connected to 1, 2
    [1, 0, 0, 1],  # Node 1: connected to 0, 3
    [1, 0, 0, 1],  # Node 2: connected to 0, 3
    [0, 1, 1, 0]   # Node 3: connected to 1, 2
]
```

**Pros**:
- ✓ Edge lookup O(1)
- ✓ Good for dense graphs
- ✓ Efficient for some algorithms

**Cons**:
- ✗ Memory O(V²) even for sparse graphs
- ✗ Slow neighbor iteration

---

## 3. Graph Traversals

### Depth-First Search (DFS)
Explore as far as possible before backtracking.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited
```

**Characteristics**:
- **Time**: O(V + E)
- **Space**: O(V) recursion stack
- **Use**: Path finding, cycle detection, topological sort

### Breadth-First Search (BFS)
Explore level by level.

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=' ')
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
```

**Characteristics**:
- **Time**: O(V + E)
- **Space**: O(V) queue size
- **Use**: Shortest path (unweighted), level-order, connected components

---

## 4. Connected Components

**Connected component**: Set of vertices reachable from each other.

```python
def count_components(graph, n):
    visited = set()
    count = 0
    
    for i in range(n):
        if i not in visited:
            dfs(graph, i, visited)
            count += 1
    
    return count
```

**Time**: O(V + E), **Space**: O(V)

---

## 5. Cycle Detection

### Undirected Graph:
A cycle exists if we revisit a vertex (except parent in DFS).

```python
def has_cycle(graph, n):
    visited = [False] * n
    
    def dfs(node, parent):
        visited[node] = True
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    
    return False
```

### Directed Graph:
Use color marking: white (unvisited), gray (in progress), black (finished).

```python
def has_cycle_directed(graph, n):
    color = [0] * n  # 0=white, 1=gray, 2=black
    
    def dfs(node):
        color[node] = 1  # Mark gray
        
        for neighbor in graph[node]:
            if color[neighbor] == 1:  # Back edge
                return True
            if color[neighbor] == 0 and dfs(neighbor):
                return True
        
        color[node] = 2  # Mark black
        return False
    
    for i in range(n):
        if color[i] == 0:
            if dfs(i):
                return True
    
    return False
```

---

## 6. Topological Sort (Directed Acyclic Graph)

Order vertices such that for every edge (u, v), u comes before v.

```python
def topological_sort(graph, n):
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
    
    return stack[::-1]  # Reverse to get correct order
```

**Time**: O(V + E), **Space**: O(V)

---

## 7. Shortest Path (Unweighted)

Use BFS to find shortest path.

```python
def shortest_path(graph, start, end, n):
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
    
    return None  # No path exists
```

**Time**: O(V + E), **Space**: O(V)

---

## 8. Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| DFS | O(V+E) | O(V) | Recursion stack |
| BFS | O(V+E) | O(V) | Queue size |
| Cycle detect | O(V+E) | O(V) | DFS with color |
| Components | O(V+E) | O(V) | Multiple DFS |
| Topological sort | O(V+E) | O(V) | DAG only |

**V** = number of vertices, **E** = number of edges

---

## 9. When to Use DFS vs BFS

### Use DFS:
- ✓ Path existence (any path)
- ✓ Cycle detection
- ✓ Topological sorting
- ✓ Strongly connected components
- ✓ Backtracking problems

### Use BFS:
- ✓ Shortest path (unweighted)
- ✓ Level-order traversal
- ✓ Connected components
- ✓ Bipartite checking
- ✓ All nodes at distance K

---

## 10. Graph Patterns

### Pattern 1: Connected Components
Count or identify separate graphs.

### Pattern 2: Cycle Detection
Check if graph has cycles (important for DAGs, dependency resolution).

### Pattern 3: Shortest Path
Find minimum edges/distance between nodes (BFS for unweighted).

### Pattern 4: Topological Order
Arrange nodes respecting dependencies (DAG only).

### Pattern 5: Bipartite Check
Color graph with 2 colors, no adjacent same color.

---

## 11. Key Takeaways

✅ **Graph**: Vertices + Edges structure  
✅ **Adjacency List**: O(V+E) space, good for sparse graphs  
✅ **Adjacency Matrix**: O(1) edge check, good for dense graphs  
✅ **DFS**: Recursive, path/cycle detection, topological sort  
✅ **BFS**: Iterative, shortest path, level-order  
✅ **Connected Components**: Multiple DFS/BFS from unvisited nodes  
✅ **Time Complexity**: Both DFS/BFS are O(V+E)  

**Best for**: Network analysis, social graphs, routing, dependency resolution  
**Not for**: Weighted shortest paths (use Dijkstra instead - advanced)

Next: Implement graph algorithms and solve connectivity problems!
