"""
Project: BFS & Queue Applications

Build practical applications using queues:
1. Graph connectivity analysis (BFS)
2. Shortest path finder (BFS)
3. Social network analyzer (degree tracking)
4. Puzzle solver (BFS state exploration)
5. Maze solver (grid-based BFS)
6. Performance comparison

This project applies:
- Queue operations
- Breadth-First Search
- Graph algorithms
- Problem solving with BFS
"""

from collections import deque
from typing import List, Dict, Set, Tuple, Optional

print("=" * 70)
print("PROJECT: BFS & Queue Applications")
print("=" * 70)

# ==================== PART 1: Graph Traversal ====================
print("\n[PART 1] Graph BFS Traversal & Connectivity")
print("-" * 70)

class Graph:
    """Graph representation with BFS"""

    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        """Add edge from u to v (undirected)"""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bfs(self, start):
        """BFS traversal from start node"""
        visited = set([start])
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in sorted(self.graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def is_connected(self):
        """Check if graph is connected"""
        if not self.graph:
            return True

        start = next(iter(self.graph))
        visited = set(self.bfs(start))

        return len(visited) == len(self.graph)

    def find_connected_components(self):
        """Find all connected components"""
        visited = set()
        components = []

        for node in self.graph:
            if node not in visited:
                component = []
                queue = deque([node])
                visited.add(node)

                while queue:
                    current = queue.popleft()
                    component.append(current)

                    for neighbor in self.graph[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components

# Test graph
print("Building Graph:")
g = Graph()
edges = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('D', 'E'), ('F', 'G')]

for u, v in edges:
    g.add_edge(u, v)
    print(f"  Added edge: {u} -- {v}")

print(f"\nBFS from A: {g.bfs('A')}")
print(f"Is connected: {g.is_connected()}")
print(f"Connected components: {g.find_connected_components()}")
print("→ BFS finds all reachable nodes and components")

# ==================== PART 2: Shortest Path ====================
print("\n[PART 2] Shortest Path Finder (BFS)")
print("-" * 70)

class ShortestPath:
    """Find shortest path in unweighted graph"""

    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start, end):
        """Find shortest path from start to end"""
        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()

            if node == end:
                return path

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def shortest_path_length(self, start, end):
        """Get length of shortest path"""
        path = self.find_shortest_path(start, end)
        return len(path) - 1 if path else -1

    def find_all_shortest_paths(self, start, end):
        """Find all shortest paths (in case of ties)"""
        visited = {start}
        queue = deque([(start, [start])])
        shortest_length = float('inf')
        all_paths = []

        while queue:
            node, path = queue.popleft()

            if len(path) - 1 > shortest_length:
                continue

            if node == end:
                if len(path) - 1 < shortest_length:
                    shortest_length = len(path) - 1
                    all_paths = [path]
                elif len(path) - 1 == shortest_length:
                    all_paths.append(path)
                continue

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited or len(path) < shortest_length:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return all_paths

# Test shortest path
graph_dict = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}

sp = ShortestPath(graph_dict)
print("Graph:", graph_dict)
print(f"\nShortest path A → F: {sp.find_shortest_path('A', 'F')}")
print(f"Path length: {sp.shortest_path_length('A', 'F')}")
print("→ BFS guarantees shortest path in unweighted graphs")

# ==================== PART 3: Social Network Analysis ====================
print("\n[PART 3] Social Network Analysis")
print("-" * 70)

class SocialNetwork:
    """Analyze social network connections"""

    def __init__(self):
        self.connections = {}

    def add_friendship(self, person1, person2):
        """Add friendship (undirected)"""
        if person1 not in self.connections:
            self.connections[person1] = []
        if person2 not in self.connections:
            self.connections[person2] = []
        self.connections[person1].append(person2)
        self.connections[person2].append(person1)

    def degrees_of_separation(self, person1, person2):
        """Find degrees of separation between two people"""
        if person1 == person2:
            return 0

        visited = {person1}
        queue = deque([(person1, 0)])

        while queue:
            person, degree = queue.popleft()

            for friend in self.connections.get(person, []):
                if friend == person2:
                    return degree + 1

                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, degree + 1))

        return -1

    def find_friends_at_distance(self, person, distance):
        """Find all friends at exact distance"""
        visited = {person}
        queue = deque([(person, 0)])
        result = []

        while queue:
            current, dist = queue.popleft()

            if dist == distance:
                result.append(current)
                continue
            elif dist < distance:
                for friend in self.connections.get(current, []):
                    if friend not in visited:
                        visited.add(friend)
                        queue.append((friend, dist + 1))

        return result

# Test social network
net = SocialNetwork()
friendships = [
    ('Alice', 'Bob'),
    ('Bob', 'Charlie'),
    ('Charlie', 'David'),
    ('Alice', 'Eve'),
    ('Eve', 'Frank'),
]

print("Building social network:")
for p1, p2 in friendships:
    net.add_friendship(p1, p2)
    print(f"  {p1} ↔ {p2}")

print(f"\nDegrees of separation:")
print(f"  Alice ↔ David: {net.degrees_of_separation('Alice', 'David')} degrees")
print(f"  Alice ↔ Frank: {net.degrees_of_separation('Alice', 'Frank')} degrees")

print(f"\nFriends 2 hops away from Alice: {net.find_friends_at_distance('Alice', 2)}")

# ==================== PART 4: Maze Solver ====================
print("\n[PART 4] Maze Solver Using BFS")
print("-" * 70)

class MazeSolver:
    """Solve maze using BFS"""

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0

    def solve(self, start, end):
        """Find shortest path from start to end"""
        visited = set([start])
        queue = deque([(start, [start])])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.rows and 0 <= ny < self.cols and
                    self.maze[nx][ny] != '#' and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return None

# Test maze
maze = [
    ['S', '.', '#', '.', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.'],
    ['#', '#', '.', '#', 'E'],
]

print("Maze (S=start, E=end, #=wall, .=path):")
for row in maze:
    print("  " + " ".join(row))

solver = MazeSolver(maze)
path = solver.solve((0, 0), (3, 4))
print(f"\nShortest path: {path}")
print(f"Path length: {len(path) - 1 if path else 'No path'}")

# ==================== PART 5: Word Transformation ====================
print("\n[PART 5] Word Transformation Using BFS")
print("-" * 70)

class WordTransformer:
    """Find shortest word transformation sequence"""

    def __init__(self, word_list):
        self.word_list = set(word_list)

    def get_neighbors(self, word):
        """Get words one letter different"""
        neighbors = []

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in self.word_list:
                        neighbors.append(new_word)

        return neighbors

    def find_transformation(self, start, end):
        """Find shortest transformation sequence"""
        if start == end:
            return [start]

        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            word, path = queue.popleft()

            for neighbor in self.get_neighbors(word):
                if neighbor == end:
                    return path + [end]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

# Test word transformation
words = ['hit', 'hot', 'dot', 'dog', 'lot', 'log', 'cog']
transformer = WordTransformer(words)

print("Available words:", words)
transformation = transformer.find_transformation('hit', 'cog')
print(f"\nTransformation 'hit' → 'cog': {transformation}")
if transformation:
    print(f"Number of steps: {len(transformation) - 1}")

# ==================== PART 6: Performance Analysis ====================
print("\n[PART 6] BFS Performance Analysis")
print("-" * 70)

import time

def benchmark_bfs_large_graph():
    """Benchmark BFS on large graph"""
    # Create large graph
    g = {}
    for i in range(1000):
        g[i] = [(i + 1) % 1000, (i + 10) % 1000]

    # BFS
    start = time.time()
    visited = set([0])
    queue = deque([0])
    count = 0

    while queue:
        node = queue.popleft()
        count += 1

        for neighbor in g[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    elapsed = (time.time() - start) * 1000

    return count, elapsed

nodes_visited, time_ms = benchmark_bfs_large_graph()
print(f"BFS on 1000-node graph:")
print(f"  Nodes visited: {nodes_visited}")
print(f"  Time: {time_ms:.2f} ms")
print(f"  → Linear O(V + E) algorithm")

# ==================== PART 7: Summary ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Topics Covered:

1. Graph BFS Traversal
   - Traverse all reachable nodes
   - Find connected components
   - Check graph connectivity
   - Complexity: O(V + E)

2. Shortest Path Finder
   - Find path between two nodes
   - Guaranteed shortest in unweighted graphs
   - BFS explores level by level
   - Complexity: O(V + E)

3. Social Network Analysis
   - Calculate degrees of separation
   - Find friends at specific distance
   - Network connectivity analysis
   - Practical application of BFS

4. Maze Solver
   - Find path through maze
   - Handle obstacles and boundaries
   - Grid-based BFS variant
   - Real-world pathfinding

5. Word Transformation
   - Model as graph problem
   - Nodes = words, Edges = one-letter differences
   - Find shortest transformation sequence
   - Practical linguistics problem

6. Performance Analysis
   - BFS is linear O(V + E)
   - Space O(V) for visited set and queue
   - Scales well to large graphs
   - Optimal for unweighted shortest path

Real-World Applications:

✓ Social networks (friend connections)
✓ GPS navigation (shortest route)
✓ Game AI (pathfinding)
✓ Web crawling (page discovery)
✓ Network analysis (connectivity)
✓ Puzzle solving (state exploration)
✓ Epidemic simulation (spread analysis)

Key Insights:

✓ BFS is fundamental for unweighted graphs
✓ Always use visited set to avoid cycles
✓ Queue enables level-by-level processing
✓ Perfect for shortest path problems
✓ Works with any graph representation
✓ Time complexity: O(V + E)
✓ Space complexity: O(V)

Common Patterns:

1. Basic BFS: Traverse all reachable nodes
2. Path finding: Track path during BFS
3. Distance tracking: Include distance in queue
4. Multi-source: Start with multiple nodes
5. Grid-based: Use (row, col) coordinates
6. State space: Each state is a node

Performance Characteristics:

- Visiting all nodes: O(V)
- Exploring all edges: O(E)
- Total BFS: O(V + E)
- No backtracking needed (unlike DFS)
- Always finds shortest path first

Next Steps:
1. Implement DFS for comparison
2. Study Dijkstra's (weighted graphs)
3. Learn A* algorithm (heuristic search)
4. Practice on LeetCode BFS problems
5. Move to Topic 06: Basic Sorting
""")

print("=" * 70)
print("Project Complete! Topic 05 Finished Successfully!")
print("=" * 70)
