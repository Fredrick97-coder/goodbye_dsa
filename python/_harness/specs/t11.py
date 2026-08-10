"""Specs for Topic 11 -- Graphs (Basics).

Graphs arrive either as an adjacency dict or as an edge list, matching the
signatures in the exercise file. Traversal ORDER is not compared where more
than one order is legitimate -- only the reachable set, or the length.
"""

from collections import deque

from ..spec import as_sorted, spec


def _adj_from_edges(n, edges, directed=False):
    g = {i: [] for i in range(n)}
    for a, b in edges:
        g[a].append(b)
        if not directed:
            g[b].append(a)
    return g


def _reachable(graph, start):
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for w in graph.get(v, []):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return sorted(seen)


def _components(n, edges):
    g = _adj_from_edges(n, edges)
    seen = set()
    count = 0
    for v in range(n):
        if v in seen:
            continue
        count += 1
        stack = [v]
        seen.add(v)
        while stack:
            x = stack.pop()
            for w in g[x]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return count


def _cycle_undirected(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return True
        parent[rb] = ra
    return False


def _cycle_directed(n, edges):
    g = _adj_from_edges(n, edges, directed=True)
    WHITE, GREY, BLACK = 0, 1, 2
    colour = [WHITE] * n

    def visit(v):
        colour[v] = GREY
        for w in g[v]:
            if colour[w] == GREY:
                return True
            if colour[w] == WHITE and visit(w):
                return True
        colour[v] = BLACK
        return False

    return any(colour[v] == WHITE and visit(v) for v in range(n))


def _shortest_path(graph, start, end):
    """Returns the path as a list; [] when unreachable. BFS = shortest hops."""
    if start == end:
        return [start]
    prev = {start: None}
    q = deque([start])
    while q:
        v = q.popleft()
        for w in graph.get(v, []):
            if w not in prev:
                prev[w] = v
                if w == end:
                    path = [w]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return path[::-1]
                q.append(w)
    return []


def _topo_valid(order, n, edges):
    """Any valid topological order is acceptable, so validate rather than compare."""
    if order is None:
        return None
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in edges)


def _is_bipartite(n, edges):
    g = _adj_from_edges(n, edges)
    colour = {}
    for s in range(n):
        if s in colour:
            continue
        colour[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for w in g[v]:
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    q.append(w)
                elif colour[w] == colour[v]:
                    return False
    return True


def _ladder_length(begin, end, word_list):
    words = set(word_list)
    if end not in words:
        return 0
    q = deque([(begin, 1)])
    seen = {begin}
    while q:
        word, d = q.popleft()
        if word == end:
            return d
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + c + word[i + 1:]
                if nxt in words and nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, d + 1))
    return 0


def g_graph_start(rng):
    n = rng.randint(1, 8)
    g = {i: [] for i in range(n)}
    for a in range(n):
        for b in range(n):
            if a != b and rng.random() < 0.3:
                g[a].append(b)
    return (g, rng.randrange(n))


def g_undirected_edges(rng):
    n = rng.randint(1, 8)
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)
             if rng.random() < 0.3]
    return (n, edges)


def g_dag_edges(rng):
    """Random DAG: only edges from lower to higher index, then relabelled."""
    n = rng.randint(1, 8)
    perm = list(range(n))
    rng.shuffle(perm)
    edges = [(perm[a], perm[b]) for a in range(n) for b in range(a + 1, n)
             if rng.random() < 0.3]
    return (n, edges)


def g_digraph_edges(rng):
    n = rng.randint(1, 7)
    edges = [(a, b) for a in range(n) for b in range(n)
             if a != b and rng.random() < 0.25]
    return (n, edges)


def g_graph_pair(rng):
    g, s = g_graph_start(rng)
    return (g, s, rng.randrange(len(g)))


SPECS = [
    spec(1, "dfs_traversal", prop=lambda x: None if x is None else sorted(set(x)),
         ref=lambda g, s: _reachable(g, s), gen=g_graph_start,
         cases=[(({0: [1, 2], 1: [2], 2: []}, 0), [0, 1, 2])],
         note="only the REACHABLE SET is compared; DFS order varies"),
    spec(2, "bfs_traversal", prop=lambda x: None if x is None else sorted(set(x)),
         ref=lambda g, s: _reachable(g, s), gen=g_graph_start,
         cases=[(({0: [1, 2], 1: [2], 2: []}, 0), [0, 1, 2])],
         note="only the REACHABLE SET is compared"),
    spec(3, "num_connected_components", ref=_components, gen=g_undirected_edges,
         cases=[((5, [(0, 1), (1, 2), (3, 4)]), 2),
                ((3, []), 3), ((1, []), 1)]),
    spec(4, "find_component", norm=as_sorted,
         ref=lambda g, n: _reachable(g, n),
         gen=lambda r: (lambda gs: (gs[0], gs[1]))(g_graph_start(r)),
         cases=[(({0: [1], 1: [0], 2: []}, 0), [0, 1])]),
    spec(5, "has_cycle_undirected", ref=_cycle_undirected,
         gen=g_undirected_edges,
         cases=[((3, [(0, 1), (1, 2), (2, 0)]), True),
                ((3, [(0, 1), (1, 2)]), False),
                ((1, []), False)]),
    spec(6, "has_cycle_directed", ref=_cycle_directed, gen=g_digraph_edges,
         cases=[((3, [(0, 1), (1, 2), (2, 0)]), True),
                ((3, [(0, 1), (1, 2)]), False),
                ((2, [(0, 1), (1, 0)]), True)]),
    spec(7, "shortest_path",
         prop=lambda p: None if p is None else len(p),
         ref=lambda g, s, e: len(_shortest_path(g, s, e)),
         gen=g_graph_pair,
         cases=[(({0: [1, 2], 1: [3], 2: [3], 3: []}, 0, 3), 3)],
         note="only the path LENGTH is compared; ties are legitimate"),
    spec(10, "is_bipartite", ref=_is_bipartite, gen=g_undirected_edges,
         cases=[((4, [(0, 1), (1, 2), (2, 3), (3, 0)]), True),
                ((3, [(0, 1), (1, 2), (2, 0)]), False),
                ((1, []), True)]),
    spec(9, "ladder_length", ref=_ladder_length,
         cases=[(("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0)]),
]

# topological_sort needs a VALIDATOR, not an equality check: many orders are
# correct for the same DAG. Each case gets a prop closed over its own graph,
# so the check is "is this output a valid topological order of that DAG?"
_TOPO_CASES = [
    (4, [(0, 1), (1, 2), (2, 3)]),
    (3, []),
    (5, [(0, 2), (1, 2), (2, 3), (2, 4)]),
    (1, []),
]
SPECS += [
    spec(8, "topological_sort",
         prop=(lambda n, e: lambda o: _topo_valid(o, n, e))(_n, _edges),
         cases=[((_n, _edges), True)],
         note="ANY valid topological order is accepted")
    for _n, _edges in _TOPO_CASES
]
