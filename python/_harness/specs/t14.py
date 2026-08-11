"""
Specs for Topic 14 -- Graph Algorithms.

The exercise file says "adjacency list" without pinning the weighted format,
so these specs use the shape the topic's own examples.py uses:

    graph = {u: [(v, weight), ...], ...}

and edge lists as [(u, v, weight), ...]. If your solution assumes a different
convention, the mismatch will show up as a FAIL with the input printed --
change the spec rather than your solution in that case.
"""

import heapq
from collections import defaultdict, deque

from ..spec import as_sorted_inner, spec

INF = float("inf")


# --------------------------------------------------------------- references

def _dijkstra(graph, start):
    dist = {v: INF for v in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist.get(v, INF):
            continue
        for w, weight in graph.get(v, []):
            nd = d + weight
            if nd < dist.get(w, INF):
                dist[w] = nd
                heapq.heappush(pq, (nd, w))
    return dist


def _bellman_ford(edges, vertices, start):
    dist = {v: INF for v in range(vertices)}
    dist[start] = 0
    for _ in range(vertices - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def _floyd_warshall(graph, vertices):
    d = [[INF] * vertices for _ in range(vertices)]
    for v in range(vertices):
        d[v][v] = 0
    for u in graph:
        for v, w in graph[u]:
            d[u][v] = min(d[u][v], w)
    for k in range(vertices):
        for i in range(vertices):
            for j in range(vertices):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def _mst_weight(edges, vertices):
    """Kruskal. Returns the total weight, or None if the graph is unconnected."""
    parent = list(range(vertices))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for w, u, v in sorted((w, u, v) for u, v, w in edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            total += w
            used += 1
    return total if used == vertices - 1 else None


def _prim_weight(graph, start):
    seen = {start}
    pq = [(w, v) for v, w in graph.get(start, [])]
    heapq.heapify(pq)
    total = 0
    while pq:
        w, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        total += w
        for nxt, nw in graph.get(v, []):
            if nxt not in seen:
                heapq.heappush(pq, (nw, nxt))
    return total if len(seen) == len(graph) else None


def _grid_shortest(grid):
    """Minimum sum path top-left to bottom-right, 4-directional Dijkstra."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    dist = [[INF] * C for _ in range(R)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    while pq:
        d, r, c = heapq.heappop(pq)
        if d > dist[r][c]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    return dist[R - 1][C - 1]


def _network_delay(edges, n, k):
    """Nodes are 1..n, as in the classic statement."""
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = {v: INF for v in range(1, n + 1)}
    dist[k] = 0
    pq = [(0, k)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        for w, weight in graph[v]:
            if d + weight < dist[w]:
                dist[w] = d + weight
                heapq.heappush(pq, (d + weight, w))
    worst = max(dist.values())
    return -1 if worst == INF else worst


def _scc(graph, vertices):
    """Kosaraju. Returns components as sorted lists, outer list sorted too."""
    order = []
    seen = set()

    def dfs1(v):
        seen.add(v)
        for w, _ in graph.get(v, []):
            if w not in seen:
                dfs1(w)
        order.append(v)

    for v in range(vertices):
        if v not in seen:
            dfs1(v)

    rev = defaultdict(list)
    for u in graph:
        for v, _ in graph[u]:
            rev[v].append(u)

    comps = []
    seen.clear()
    for v in reversed(order):
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        comp = []
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in rev[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(sorted(comp))
    return sorted(comps)


def _cheapest_flights(flights, n, src, dst, k):
    """At most k STOPS, i.e. k+1 edges. Bellman-Ford bounded by hops."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]
        for u, v, w in flights:
            if dist[u] != INF and dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == INF else dist[dst]


def _min_cost_connect(cost):
    """Prim on a dense cost matrix."""
    n = len(cost)
    if n <= 1:
        return 0
    seen = {0}
    total = 0
    while len(seen) < n:
        best = INF
        best_v = None
        for u in seen:
            for v in range(n):
                if v not in seen and cost[u][v] < best:
                    best, best_v = cost[u][v], v
        total += best
        seen.add(best_v)
    return total


def _topo_valid(order, graph, vertices):
    if order is None:
        return None
    if sorted(order) != list(range(vertices)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u in graph for v, _ in graph[u])


# ------------------------------------------------------------------ generators

def g_weighted_graph(rng, n_lo=1, n_hi=7, directed=True):
    n = rng.randint(n_lo, n_hi)
    graph = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < 0.35:
                w = rng.randint(1, 20)
                graph[u].append((v, w))
                if not directed:
                    graph[v].append((u, w))
    return graph, n


def g_dijkstra(rng):
    graph, n = g_weighted_graph(rng)
    return (graph, rng.randrange(n))


def g_edges(rng):
    graph, n = g_weighted_graph(rng)
    edges = [(u, v, w) for u in graph for v, w in graph[u]]
    return (edges, n, rng.randrange(n))


def g_floyd(rng):
    graph, n = g_weighted_graph(rng)
    return (graph, n)


def g_undirected_edges(rng):
    n = rng.randint(1, 7)
    edges = [(u, v, rng.randint(1, 20))
             for u in range(n) for v in range(u + 1, n)
             if rng.random() < 0.55]
    return (edges, n)


def g_grid(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    return ([[rng.randint(0, 9) for _ in range(C)] for _ in range(R)],)


def g_cost_matrix(rng):
    n = rng.randint(1, 6)
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w = rng.randint(1, 30)
            m[i][j] = m[j][i] = w
    return (m,)


def g_dag(rng):
    n = rng.randint(1, 7)
    perm = list(range(n))
    rng.shuffle(perm)
    graph = {v: [] for v in range(n)}
    for a in range(n):
        for b in range(a + 1, n):
            if rng.random() < 0.35:
                graph[perm[a]].append((perm[b], rng.randint(1, 9)))
    return (graph, n)


SAMPLE_G = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}

def _ref_bridges(n, connections):
    """
    Brute force: an edge is critical when removing it disconnects the graph.

    O(E * (V + E)) and obviously correct, which is what a reference is for --
    the learner writes Tarjan's low-link version.
    """
    from collections import defaultdict, deque
    edges = [tuple(e) for e in connections]

    def connected(skip):
        adj = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            if i == skip:
                continue
            adj[a].append(b)
            adj[b].append(a)
        seen = {0}
        q = deque([0])
        while q:
            node = q.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        return len(seen) == n

    if not connected(-1):
        # A disconnected graph has no single edge whose removal disconnects
        # something that was joined to begin with.
        return []
    return [list(edges[i]) for i in range(len(edges)) if not connected(i)]


def g_bridge_graph(rng):
    """A connected graph: a spanning tree plus a few extra edges."""
    n = rng.randint(2, 8)
    edges = [(i, rng.randrange(i)) for i in range(1, n)]
    for _ in range(rng.randint(0, 3)):
        a, b = rng.sample(range(n), 2)
        if (a, b) not in edges and (b, a) not in edges:
            edges.append((a, b))
    return (n, edges)


def _as_edge_set(x):
    """Direction and order carry no meaning for an undirected bridge."""
    if x is None:
        return None
    return sorted(tuple(sorted(e)) for e in x)


SPECS = [
    spec(1, "dijkstra_shortest_path", ref=_dijkstra, gen=g_dijkstra,
         cases=[((SAMPLE_G, 0), {0: 0, 1: 3, 2: 1, 3: 4})],
         note="graph = {u: [(v, weight), ...]}"),
    spec(2, "kruskal_mst",
         prop=lambda r: None if r is None else r[1],
         ref=lambda edges, n: _mst_weight(edges, n),
         gen=g_undirected_edges,
         cases=[(([(0, 1, 1), (1, 2, 2), (0, 2, 3)], 3), 3)],
         note="returns (edges, total_weight); only the WEIGHT is compared"),
    spec(3, "topological_sort",
         prop=lambda o: o,
         cases=[],
         note="replaced below with per-graph validators"),
    spec(4, "shortest_path_grid", ref=_grid_shortest, gen=g_grid,
         cases=[(([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7)],
         note="sum of cell weights along the path, including both ends"),
    spec(5, "bellman_ford", ref=_bellman_ford, gen=g_edges,
         cases=[(([(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)], 4, 0),
                 {0: 0, 1: 3, 2: 1, 3: 4})],
         note="edges = [(u, v, weight)]; unreachable stays inf"),
    spec(6, "floyd_warshall", ref=_floyd_warshall, gen=g_floyd,
         cases=[((SAMPLE_G, 4),
                 _floyd_warshall(SAMPLE_G, 4))]),
    spec(7, "prims_mst",
         prop=lambda r: None if r is None else r[1],
         ref=lambda g, s: _prim_weight(g, s),
         gen=lambda r: (lambda gn: (gn[0], 0))(
             g_weighted_graph(r, 1, 7, directed=False)),
         cases=[(({0: [(1, 1)], 1: [(0, 1), (2, 2)], 2: [(1, 2)]}, 0), 3)],
         note="undirected graph; only the total WEIGHT is compared"),
    spec(8, "network_delay_time", ref=_network_delay,
         gen=lambda r: (lambda n: (
             [(r.randint(1, n), r.randint(1, n), r.randint(1, 10))
              for _ in range(r.randint(0, 10))], n, r.randint(1, n)))(
             r.randint(1, 6)),
         cases=[(([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2), 2),
                (([(1, 2, 1)], 2, 2), -1)],
         note="nodes are 1..n"),
    spec(9, "find_scc", ref=_scc, gen=g_floyd, norm=as_sorted_inner,
         cases=[(({0: [(1, 1)], 1: [(2, 1)], 2: [(0, 1)]}, 3), [[0, 1, 2]])]),
    spec(10, "cheapest_flights_k_stops", ref=_cheapest_flights,
         gen=lambda r: (lambda n: (
             [(r.randrange(n), r.randrange(n), r.randint(1, 20))
              for _ in range(r.randint(0, 10))],
             n, r.randrange(n), r.randrange(n), r.randint(0, 3)))(
             r.randint(1, 6)),
         cases=[(([(0, 1, 100), (1, 2, 100), (0, 2, 500)], 3, 0, 2, 1), 200),
                (([(0, 1, 100), (1, 2, 100), (0, 2, 500)], 3, 0, 2, 0), 500)],
         note="k is the number of STOPS, so k+1 edges are allowed"),
    spec(11, "minimum_cost_connect_cities", ref=_min_cost_connect,
         gen=g_cost_matrix,
         cases=[(([[0, 1, 3], [1, 0, 2], [3, 2, 0]],), 3)]),
]

# topological_sort accepts ANY valid order, so validate instead of comparing.
SPECS = [s for s in SPECS if s.target != "topological_sort"]
_TOPO = [
    ({0: [(1, 1)], 1: [(2, 1)], 2: []}, 3),
    ({0: [], 1: [], 2: []}, 3),
    ({0: [(2, 1)], 1: [(2, 1)], 2: [(3, 1)], 3: []}, 4),
]
SPECS += [
    spec(3, "topological_sort",
         prop=(lambda g, n: lambda o: _topo_valid(o, g, n))(_g, _n),
         cases=[((_g, _n), True)],
         note="ANY valid topological order is accepted")
    for _g, _n in _TOPO

]


SPECS += [
    spec(12, "find_critical_connections", ref=_ref_bridges,
         gen=g_bridge_graph, norm=_as_edge_set,
         cases=[((4, [(0, 1), (1, 2), (2, 0), (1, 3)]), [[1, 3]]),
                ((2, [(0, 1)]), [[0, 1]])],
         note="undirected, so [a,b] and [b,a] are the same bridge and the "
              "order of the list does not matter"),
]
