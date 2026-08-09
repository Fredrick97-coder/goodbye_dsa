"""
Project: Advanced Graph Algorithms in the Real World

Build practical systems using advanced graph algorithms:
1. GPS Navigation (Dijkstra)
2. Airline Network (Bellman-Ford)
3. Network Design (MST)
4. Social Network Analysis (SCCs)
"""

import heapq
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import time

print("=" * 70)
print("PROJECT: Advanced Graph Algorithms Applications")
print("=" * 70)

# ==================== PART 1: GPS Navigation (Dijkstra) ====================
print("\n[PART 1] GPS Navigation System (Dijkstra's Algorithm)")
print("-" * 70)

@dataclass
class Route:
    distance: float
    time_minutes: float

class GPSNavigator:
    """Find fastest route between cities using Dijkstra"""

    def __init__(self):
        self.graph = {}

    def add_road(self, city1: str, city2: str, distance: float, speed_limit: int = 60):
        """Add bidirectional road between cities"""
        time_minutes = (distance / speed_limit) * 60

        if city1 not in self.graph:
            self.graph[city1] = []
        if city2 not in self.graph:
            self.graph[city2] = []

        self.graph[city1].append((city2, distance, time_minutes))
        self.graph[city2].append((city1, distance, time_minutes))

    def find_fastest_route(self, start: str, end: str) -> Tuple[float, List[str]]:
        """Find fastest route using Dijkstra's algorithm"""
        times = {city: float('inf') for city in self.graph}
        times[start] = 0
        parent = {city: None for city in self.graph}
        pq = [(0, start)]

        while pq:
            curr_time, curr_city = heapq.heappop(pq)

            if curr_time > times[curr_city]:
                continue

            for neighbor, distance, time_mins in self.graph[curr_city]:
                new_time = curr_time + time_mins

                if new_time < times[neighbor]:
                    times[neighbor] = new_time
                    parent[neighbor] = curr_city
                    heapq.heappush(pq, (new_time, neighbor))

        # Reconstruct path
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()

        return times[end], path

# Test GPS Navigator
print("GPS Navigation Demo:\n")
navigator = GPSNavigator()

roads = [
    ("NYC", "Boston", 215, 65),
    ("NYC", "Philadelphia", 95, 65),
    ("Boston", "Philadelphia", 305, 70),
    ("Philadelphia", "DC", 140, 70),
    ("Boston", "DC", 440, 65),
    ("NYC", "DC", 225, 65),
]

for city1, city2, dist, speed in roads:
    navigator.add_road(city1, city2, dist, speed)

time_mins, route = navigator.find_fastest_route("Boston", "DC")

print("Road Network:")
for c1, c2, dist, speed in roads:
    print(f"  {c1} ↔ {c2}: {dist} miles @ {speed} mph")

print(f"\nFastest route from Boston to DC:")
print(f"  Route: {' → '.join(route)}")
print(f"  Time: {time_mins:.1f} minutes ({time_mins/60:.1f} hours)")

print("→ Time: O((V + E) log V), Space: O(V)")
print("→ Real application: Google Maps, Apple Maps")

# ==================== PART 2: Airline Network (Bellman-Ford) ====================
print("\n[PART 2] Airline Network (Bellman-Ford - Negative Weights)")
print("-" * 70)

class AirlineNetwork:
    """Find best currency exchange rates across airports"""

    def __init__(self):
        self.edges = []
        self.airports = set()

    def add_flight(self, from_airport: str, to_airport: str, exchange_rate: float):
        """Add flight with exchange rate (can be > 1 or < 1)"""
        self.edges.append((from_airport, to_airport, -exchange_rate))  # Negative for max
        self.airports.add(from_airport)
        self.airports.add(to_airport)

    def find_arbitrage(self, start: str) -> Tuple[bool, Dict]:
        """Find profit opportunity (negative cycle) or best rates"""
        airport_list = list(self.airports)
        airport_idx = {airport: i for i, airport in enumerate(airport_list)}
        num_airports = len(airport_list)

        # Bellman-Ford to find profit (negative cycle)
        rates = {airport: 0 for airport in self.airports}
        rates[start] = 1.0

        # Relax edges V-1 times
        for _ in range(num_airports - 1):
            for from_a, to_a, neg_rate in self.edges:
                if rates[from_a] > 0:
                    new_rate = rates[from_a] * (-neg_rate)
                    if new_rate > rates[to_a]:
                        rates[to_a] = new_rate

        # Check for arbitrage (negative cycle = profit cycle)
        for from_a, to_a, neg_rate in self.edges:
            if rates[from_a] > 0:
                new_rate = rates[from_a] * (-neg_rate)
                if new_rate > rates[to_a]:
                    return True, rates  # Arbitrage found!

        return False, rates

# Test Airline Network
print("Airline Exchange Rate Demo:\n")
network = AirlineNetwork()

flights = [
    ("JFK", "LHR", 1.35),     # 1 USD → 1.35 GBP
    ("LHR", "CDG", 1.20),     # 1 GBP → 1.20 EUR
    ("CDG", "JFK", 0.95),     # 1 EUR → 0.95 USD (profit!)
]

for from_a, to_a, rate in flights:
    network.add_flight(from_a, to_a, rate)

arbitrage_found, rates = network.find_arbitrage("JFK")

print("Exchange Rates:")
for from_a, to_a, rate in flights:
    print(f"  {from_a} → {to_a}: 1 unit → {rate:.2f}")

print(f"\nArbitrage opportunity: {'YES (Profit!)' if arbitrage_found else 'No'}")

if arbitrage_found:
    print(f"Example: Start with 1.0 USD at JFK")
    print(f"  1.0 USD × 1.35 = 1.35 GBP at LHR")
    print(f"  1.35 GBP × 1.20 = 1.62 EUR at CDG")
    print(f"  1.62 EUR × 0.95 = 1.54 USD at JFK ✓ Profit!")

print("→ Time: O(V × E), Space: O(V)")
print("→ Used for currency arbitrage detection")

# ==================== PART 3: Network Design (MST) ====================
print("\n[PART 3] Network Design (Minimum Spanning Tree)")
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

class NetworkDesign:
    """Design minimum-cost network connecting all cities"""

    def __init__(self):
        self.edges = []
        self.cities = set()

    def add_cable_cost(self, city1: str, city2: str, cost: float):
        """Add potential cable connection with cost"""
        self.edges.append((cost, city1, city2))
        self.cities.add(city1)
        self.cities.add(city2)

    def design_network(self) -> Tuple[float, List[Tuple]]:
        """Find minimum-cost network using Kruskal's algorithm"""
        self.edges.sort()
        city_idx = {city: i for i, city in enumerate(sorted(self.cities))}
        uf = UnionFind(len(self.cities))

        mst = []
        total_cost = 0

        for cost, city1, city2 in self.edges:
            u, v = city_idx[city1], city_idx[city2]

            if uf.union(u, v):
                mst.append((city1, city2, cost))
                total_cost += cost

                if len(mst) == len(self.cities) - 1:
                    break

        return total_cost, mst

# Test Network Design
print("Network Design Demo:\n")
design = NetworkDesign()

cables = [
    ("NYC", "Boston", 500),
    ("NYC", "Philly", 300),
    ("Boston", "Philly", 400),
    ("Philly", "DC", 350),
    ("Boston", "DC", 600),
    ("NYC", "DC", 450),
]

for city1, city2, cost in cables:
    design.add_cable_cost(city1, city2, cost)

total_cost, network = design.design_network()

print("Possible cable connections (cost in thousands):")
for c1, c2, cost in cables:
    print(f"  {c1} ↔ {c2}: ${cost}k")

print(f"\nMinimum-cost network design (MST):")
for c1, c2, cost in network:
    print(f"  {c1} ↔ {c2}: ${cost}k")
print(f"\nTotal network cost: ${total_cost}k")

print("→ Time: O(E log E), Space: O(V)")
print("→ Used for: telecommunications, power grid, water pipes")

# ==================== PART 4: Social Network Analysis (SCC) ====================
print("\n[PART 4] Social Network Analysis (Strongly Connected Components)")
print("-" * 70)

class SocialNetwork:
    """Analyze communities in social networks"""

    def __init__(self):
        self.followers = {}  # follower relationships

    def add_follow(self, user1: str, user2: str):
        """user1 follows user2 (directed)"""
        if user1 not in self.followers:
            self.followers[user1] = []
        if user2 not in self.followers:
            self.followers[user2] = []
        self.followers[user1].append(user2)

    def find_communities(self) -> List[Set[str]]:
        """Find mutual follow communities using Kosaraju"""
        if not self.followers:
            return []

        users = list(self.followers.keys())
        user_idx = {user: i for i, user in enumerate(users)}
        n = len(users)

        # DFS 1: Record finish times
        visited = [False] * n
        stack = []

        def dfs1(v):
            visited[v] = True
            for neighbor in self.followers[users[v]]:
                neighbor_idx = user_idx[neighbor]
                if not visited[neighbor_idx]:
                    dfs1(neighbor_idx)
            stack.append(v)

        for i in range(n):
            if not visited[i]:
                dfs1(i)

        # Build transpose
        transpose = [[] for _ in range(n)]
        for u in range(n):
            for v_str in self.followers[users[u]]:
                v = user_idx[v_str]
                transpose[v].append(u)

        # DFS 2: Find SCCs
        visited = [False] * n
        communities = []

        def dfs2(v, community):
            visited[v] = True
            community.add(users[v])
            for neighbor_idx in transpose[v]:
                if not visited[neighbor_idx]:
                    dfs2(neighbor_idx, community)

        while stack:
            v = stack.pop()
            if not visited[v]:
                community = set()
                dfs2(v, community)
                if community:
                    communities.append(community)

        return communities

# Test Social Network
print("Social Network Community Detection:\n")
network = SocialNetwork()

follows = [
    ("Alice", "Bob"),
    ("Bob", "Charlie"),
    ("Charlie", "Alice"),
    ("Diana", "Eve"),
    ("Eve", "Frank"),
    ("Frank", "Diana"),
]

for user1, user2 in follows:
    network.add_follow(user1, user2)

communities = network.find_communities()

print("Follow relationships (directed):")
for u1, u2 in follows:
    print(f"  {u1} → {u2}")

print("\nCommunities (mutual followers = SCC):")
for i, community in enumerate(communities):
    print(f"  Community {i + 1}: {sorted(community)}")

print("→ Time: O(V + E), Space: O(V)")
print("→ Find groups with mutual follow relationships")

# ==================== PART 5: Algorithm Comparison ====================
print("\n[PART 5] Algorithm Performance Analysis")
print("-" * 70)

def benchmark_algorithms(vertices: int, edges: int):
    """Estimate time complexity for different algorithms"""
    import math

    dijkstra_time = (vertices + edges) * math.log(vertices)
    bellman_time = vertices * edges
    floyd_time = vertices ** 3
    kruskal_time = edges * math.log(edges)

    return {
        "Dijkstra": dijkstra_time,
        "Bellman-Ford": bellman_time,
        "Floyd-Warshall": floyd_time,
        "Kruskal's MST": kruskal_time,
    }

print("Estimated operations (relative):\n")
print(f"{'Algorithm':<20} {'100 nodes, 500 edges':<25} {'1000 nodes, 5000 edges':<25}")
print("-" * 70)

for v, e in [(100, 500), (1000, 5000)]:
    times = benchmark_algorithms(v, e)
    if v == 100:
        times_small = times
    else:
        times_large = times

for algo in times_small.keys():
    print(f"{algo:<20} {int(times_small[algo]):<25} {int(times_large[algo]):<25}")

print("\n→ Floyd-Warshall expensive for large graphs")
print("→ Dijkstra practical for most cases")
print("→ Bellman-Ford needed for negative weights")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Graph Algorithm Applications:

1. GPS Navigation (Dijkstra's Algorithm)
   - Find fastest/shortest route between locations
   - Handles weighted graph of roads
   - O((V+E) log V) efficient
   - Real apps: Google Maps, Apple Maps, Waze

2. Currency Exchange (Bellman-Ford)
   - Detect arbitrage opportunities (negative cycles)
   - Handle negative weights (exchange rates < 1)
   - Detects profit cycles
   - Real apps: Forex trading, currency arbitrage

3. Network Design (Minimum Spanning Tree)
   - Connect all cities with minimum cable cost
   - Ensures connectivity with lowest cost
   - O(E log E) using Kruskal's
   - Real apps: Telecom, power grids, water pipes

4. Social Network Analysis (Strongly Connected Components)
   - Find communities with mutual relationships
   - Identify tightly-knit groups
   - O(V+E) with Kosaraju
   - Real apps: LinkedIn groups, Discord communities

Key Insights:

✓ Dijkstra: Most practical, non-negative weights only
✓ Bellman-Ford: Handles any weights, detects cycles
✓ Floyd-Warshall: All-pairs but expensive O(V³)
✓ Kruskal's: MST, edge-based, union-find essential
✓ Prim's: MST, vertex-based, priority queue
✓ Kosaraju: SCC in O(V+E) with two DFS passes

Algorithm Selection Strategy:

1. Shortest Path Problem:
   - Non-negative? → Dijkstra
   - Any weights? → Bellman-Ford
   - All-pairs & small? → Floyd-Warshall
   - Very sparse? → Bellman-Ford might be faster

2. Spanning Tree Problem:
   - Any → Kruskal's or Prim's (same result)
   - Dense? → Prim's O(E log V)
   - Sparse? → Kruskal's O(E log E)

3. Connectivity Problem:
   - Strongly connected? → Kosaraju/Tarjan
   - Bridges? → DFS with discovery times
   - Biconnected? → DFS with low values

Optimization Techniques:

1. Priority Queue: Essential for Dijkstra/Prim's
2. Union-Find: Mandatory for efficient Kruskal's
3. Graph Transpose: For SCC algorithms
4. 2D Array: For Floyd-Warshall
5. Edge List: For sorting in Kruskal's

Complexity Reference:

Algorithm           Best Use Case           Time
─────────────────────────────────────────────────
Dijkstra            Non-neg weights         O((V+E) log V)
Bellman-Ford        Negative detection      O(V*E)
Floyd-Warshall      All-pairs small         O(V³)
Kruskal's MST       General MST             O(E log E)
Prim's MST          Dense graphs            O(E log V)
Kosaraju SCC        SCCs needed             O(V+E)
Tarjan SCC          SCCs (1 pass)           O(V+E)

Interview Preparation:

✓ Understand: Dijkstra's correctness (greedy)
✓ Implement: Bellman-Ford from scratch
✓ Know: When to use each algorithm
✓ Practice: Graph modeling for problems
✓ Optimize: Data structures (heap, union-find)
✓ Edge cases: Disconnected graphs, negative cycles

Real-World Impact:

- Navigation: Millions of Dijkstra queries daily
- Financial: Arbitrage detection worth billions
- Telecom: MST saves massive infrastructure costs
- Social: Community detection powers recommendations
- Games: Pathfinding in open-world games

Next: Master graph algorithm applications and interview questions!
""")

print("=" * 70)
print("🎉 Topic 14 Complete! Advanced Graph Algorithms Mastered!")
print("=" * 70)
print("\n✅ ADVANCED LEVEL PROGRESSING...")
print("   4 more topics to complete (Topics 15-18)")
print("   Ready for Topic 15: Greedy Algorithms\n")
