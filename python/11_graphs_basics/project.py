"""
Project: Graph Applications in the Real World

Build practical systems using graphs:
1. Social Network Analysis
2. Course Prerequisite Solver
3. Web Crawler
4. Game State Solver (BFS)
"""

from collections import defaultdict, deque
from typing import List, Set, Tuple, Optional
import time

print("=" * 70)
print("PROJECT: Graph Applications in the Real World")
print("=" * 70)

# ==================== PART 1: Social Network Analysis ====================
print("\n[PART 1] Social Network Analysis")
print("-" * 70)

class SocialNetwork:
    """Model and analyze social networks"""

    def __init__(self):
        self.users = set()
        self.friendships = defaultdict(set)

    def add_user(self, user_id: str):
        """Add user to network"""
        self.users.add(user_id)

    def add_friendship(self, user1: str, user2: str):
        """Add bidirectional friendship"""
        self.add_user(user1)
        self.add_user(user2)
        self.friendships[user1].add(user2)
        self.friendships[user2].add(user1)

    def get_friends(self, user_id: str) -> Set[str]:
        """Get direct friends"""
        return self.friendships.get(user_id, set())

    def get_friends_of_friends(self, user_id: str) -> Set[str]:
        """Get friends of friends (2 hops away)"""
        friends_of_friends = set()
        for friend in self.get_friends(user_id):
            for fof in self.get_friends(friend):
                if fof != user_id and fof not in self.get_friends(user_id):
                    friends_of_friends.add(fof)
        return friends_of_friends

    def shortest_connection(self, user1: str, user2: str) -> Optional[List[str]]:
        """Find shortest path between two users (degrees of separation)"""
        if user1 == user2:
            return [user1]

        visited = {user1}
        queue = deque([(user1, [user1])])

        while queue:
            current, path = queue.popleft()

            for friend in self.get_friends(current):
                if friend == user2:
                    return path + [friend]

                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend]))

        return None  # Not connected

    def common_friends(self, user1: str, user2: str) -> Set[str]:
        """Find mutual friends"""
        return self.get_friends(user1) & self.get_friends(user2)

    def count_communities(self) -> int:
        """Count disconnected groups using DFS"""
        visited = set()
        communities = 0

        def dfs(user):
            visited.add(user)
            for friend in self.get_friends(user):
                if friend not in visited:
                    dfs(friend)

        for user in self.users:
            if user not in visited:
                dfs(user)
                communities += 1

        return communities

# Test social network
print("Social Network Demo:\n")
network = SocialNetwork()

# Create friendships
friendships = [
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Dave"),
    ("Carol", "Eve"),
    ("Frank", "Grace"),  # Separate community
]

for user1, user2 in friendships:
    network.add_friendship(user1, user2)

print("Network structure:")
for user in sorted(network.users):
    print(f"  {user}: {network.get_friends(user)}")

# Find shortest path
path = network.shortest_connection("Alice", "Eve")
print(f"\nDegrees of separation (Alice → Eve): {path}")
print(f"Distance: {len(path) - 1} degrees")

# Find mutual friends
common = network.common_friends("Alice", "Bob")
print(f"\nMutual friends (Alice & Bob): {common}")

# Count communities
communities = network.count_communities()
print(f"Communities: {communities}")

print("→ Time: O(V + E) for all operations")
print("→ Social networks typically have small diameters")

# ==================== PART 2: Course Prerequisites ====================
print("\n[PART 2] Course Prerequisite Scheduler")
print("-" * 70)

class CourseScheduler:
    """Solve course prerequisites using topological sort"""

    def __init__(self, num_courses: int, prerequisites: List[Tuple]):
        self.num_courses = num_courses
        self.graph = defaultdict(list)
        self.in_degree = [0] * num_courses

        for course, prereq in prerequisites:
            self.graph[prereq].append(course)
            self.in_degree[course] += 1

    def find_order(self) -> Optional[List[int]]:
        """Find valid course order (topological sort)"""
        queue = deque()

        # Start with courses that have no prerequisites
        for i in range(self.num_courses):
            if self.in_degree[i] == 0:
                queue.append(i)

        order = []

        while queue:
            course = queue.popleft()
            order.append(course)

            # Remove edges from current course
            for next_course in self.graph[course]:
                self.in_degree[next_course] -= 1
                if self.in_degree[next_course] == 0:
                    queue.append(next_course)

        # If all courses scheduled, return order; else cycle detected
        return order if len(order) == self.num_courses else None

# Test course scheduler
print("Course Prerequisite Demo:\n")
courses = 4
prerequisites = [(1, 0), (2, 0), (3, 1), (3, 2)]

print(f"Courses: {list(range(courses))}")
print(f"Prerequisites (course → prereq): {prerequisites}")

scheduler = CourseScheduler(courses, prerequisites)
order = scheduler.find_order()

if order:
    print(f"Valid order: {order}")
    print("Can take: 0 first, then 1,2 (any order), then 3")
else:
    print("Impossible: cycle detected in prerequisites!")

print("→ Time: O(V + E), Space: O(V + E)")
print("→ Uses Kahn's algorithm (topological sort with in-degrees)")

# ==================== PART 3: Web Crawler ====================
print("\n[PART 3] Web Crawler with Graph Traversal")
print("-" * 70)

class WebCrawler:
    """Crawl web pages starting from seed URL"""

    def __init__(self, max_pages: int = 100):
        self.max_pages = max_pages
        self.visited_urls = set()
        self.pages = {}  # URL → list of outgoing links

    def add_links(self, url: str, outgoing_links: List[str]):
        """Register outgoing links from URL"""
        self.pages[url] = outgoing_links

    def crawl(self, start_url: str) -> int:
        """Crawl from start URL, return page count"""
        visited = {start_url}
        queue = deque([start_url])
        count = 0

        while queue and count < self.max_pages:
            url = queue.popleft()
            count += 1
            print(f"  [{count}] Crawling: {url}")

            # Add outgoing links to queue
            if url in self.pages:
                for link in self.pages[url]:
                    if link not in visited:
                        visited.add(link)
                        queue.append(link)

        return count

# Test web crawler
print("Web Crawler Demo:\n")
crawler = WebCrawler(max_pages=10)

# Add page structures (simplified)
crawler.add_links("home.html", ["about.html", "products.html"])
crawler.add_links("about.html", ["home.html", "team.html"])
crawler.add_links("products.html", ["product1.html", "product2.html"])
crawler.add_links("team.html", ["about.html"])
crawler.add_links("product1.html", ["products.html"])
crawler.add_links("product2.html", ["products.html"])

pages_crawled = crawler.crawl("home.html")
print(f"\nPages crawled: {pages_crawled}")

print("→ Time: O(V + E) for complete crawl")
print("→ BFS ensures breadth-first exploration (fairer distribution)")

# ==================== PART 4: Game State Solver (Puzzle) ====================
print("\n[PART 4] Game Puzzle Solver (BFS State Space)")
print("-" * 70)

class PuzzleSolver:
    """Solve puzzles using BFS on state graph"""

    def __init__(self, start_state: str, goal_state: str):
        self.start = start_state
        self.goal = goal_state

    def get_neighbors(self, state: str) -> List[str]:
        """Get valid next states from current state"""
        # Simplified: only swap adjacent tiles
        neighbors = []
        state_list = list(state)

        # Find blank position
        blank_pos = state.index("_")

        # Try swaps with adjacent positions
        for new_pos in [blank_pos - 1, blank_pos + 1]:
            if 0 <= new_pos < len(state):
                # Check not across row boundary (in 3x3 grid)
                if abs(blank_pos % 3 - new_pos % 3) <= 1:
                    new_state = state_list[:]
                    new_state[blank_pos], new_state[new_pos] = (
                        new_state[new_pos],
                        new_state[blank_pos],
                    )
                    neighbors.append("".join(new_state))

        return neighbors

    def solve(self, max_moves: int = 50) -> Optional[List[str]]:
        """Find solution path using BFS"""
        if self.start == self.goal:
            return [self.start]

        visited = {self.start}
        queue = deque([(self.start, [self.start])])

        while queue:
            state, path = queue.popleft()

            if len(path) > max_moves:
                return None  # Give up

            for next_state in self.get_neighbors(state):
                if next_state == self.goal:
                    return path + [next_state]

                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state]))

        return None  # No solution

# Test puzzle solver
print("Puzzle Solver Demo (3x3 sliding puzzle):\n")

# Simple puzzle: swap two tiles
start = "1_3456789"  # Blank at position 1
goal = "123456789"   # Solved

print(f"Start: {start}")
print(f"Goal:  {goal}")

solver = PuzzleSolver(start, goal)
solution = solver.solve()

if solution:
    print(f"\nSolution found! ({len(solution) - 1} moves)")
    for i, state in enumerate(solution[:3]):
        print(f"  Step {i}: {state}")
    if len(solution) > 3:
        print(f"  ... ({len(solution) - 3} more steps)")
else:
    print("No solution found within move limit")

print("→ Time: O(states), Space: O(states)")
print("→ BFS guaranteed to find shortest solution")

# ==================== PART 5: Analysis ====================
print("\n[PART 5] Graph Algorithm Performance")
print("-" * 70)

def benchmark_graph_traversal(size: int):
    """Benchmark DFS vs BFS on random graph"""
    import random

    # Create random graph
    graph = defaultdict(list)
    for _ in range(size):
        u, v = random.randint(0, size - 1), random.randint(0, size - 1)
        if u != v:
            graph[u].append(v)

    # DFS (iterative to avoid stack overflow)
    start_time = time.time()
    visited = set()
    stack = [0]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    dfs_time = (time.time() - start_time) * 1000

    # BFS
    start_time = time.time()
    visited = {0}
    queue = deque([0])

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    bfs_time = (time.time() - start_time) * 1000

    return dfs_time, bfs_time

print("Performance Comparison:\n")
print(f"{'Nodes':<10} {'DFS':<12} {'BFS':<12} {'Similar':<10}")
print("-" * 44)

for size in [100, 1000, 5000]:
    dfs_t, bfs_t = benchmark_graph_traversal(size)
    similar = "Yes" if abs(dfs_t - bfs_t) < max(dfs_t, bfs_t) * 0.5 else "No"
    print(f"{size:<10} {dfs_t:>6.3f}ms {'':<2} {bfs_t:>6.3f}ms {'':<2} {similar:<10}")

print("\n→ Both DFS and BFS: O(V + E)")
print("→ Similar performance, choice depends on problem")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Graph Applications:

1. Social Network Analysis
   - Find shortest connections (degrees of separation)
   - Discover mutual friends
   - Identify communities
   - Recommend connections

2. Course Prerequisite Scheduler
   - Topological sort for course order
   - Cycle detection for impossible prerequisites
   - Kahn's algorithm with in-degrees

3. Web Crawler
   - BFS for breadth-first discovery
   - URL deduplication with visited set
   - Controlled crawling with page limits
   - Parallel crawling of web pages

4. Game Puzzle Solver
   - State space as graph
   - BFS for shortest solution
   - Visited states prevent revisiting
   - Scalable to complex puzzles

Key Insights:

✓ Many problems can be modeled as graphs
✓ DFS: recursion, path finding, cycle detection
✓ BFS: shortest path (unweighted), level order
✓ Both: O(V + E) time complexity
✓ Graph size determines algorithm viability
✓ Visited set prevents infinite loops

Common Real-World Uses:

- Social networks (connections, recommendations)
- Maps/GPS (shortest route, navigation)
- Web crawling (indexing, discovery)
- Game AI (puzzle solving, pathfinding)
- Compiler (dependency resolution)
- Recommendation systems (graph-based)
- Network routing (shortest path)
- Schedule optimization (topological order)

Algorithm Complexity:

Algorithm           Time      Space    Use Case
─────────────────────────────────────────────
DFS                 O(V+E)    O(V)     Path, cycle
BFS                 O(V+E)    O(V)     Shortest, levels
Topological         O(V+E)    O(V)     DAG ordering
Connected Comp      O(V+E)    O(V)     Clustering
Cycle Detect        O(V+E)    O(V)     Validation
Bipartite Check     O(V+E)    O(V)     Coloring

What's Next (Advanced):

- Dijkstra's algorithm (weighted shortest path)
- Minimum Spanning Tree (Kruskal, Prim)
- Strongly Connected Components (Kosaraju)
- Maximum Flow (Ford-Fulkerson)
- A* algorithm (heuristic search)

Next Steps:
1. Master basic graph algorithms
2. Practice on LeetCode graph problems
3. Study advanced algorithms (Dijkstra, MST)
4. Implement real projects (social, maps, game)
""")

print("=" * 70)
print("Project Complete! Topic 11 Finished Successfully!")
print("=" * 70)
print("\n🎉 INTERMEDIATE LEVEL COMPLETE! (Topics 01-11)")
print("   Ready to move to Advanced Level (Topics 12-18)\n")
