"""
Specs for Topic 05 -- Queues.

Two things are worth knowing about this topic.

`reverse_queue` and `rotate_queue` are graded with `accept_inplace`: the
classic implementations rearrange the queue they were handed and return None,
but returning a new queue is just as reasonable a reading of the problem, so
both pass.

`level_order_traversal` takes a tree root, and this exercise file -- unlike
topic 08 -- defines no TreeNode for the learner to build one from. The spec
supplies its own node class instead. That is sound because the function only
ever reads `.val`, `.left` and `.right`: it consumes a tree, it does not
construct one.
"""

from collections import deque

from ..spec import spec


# ------------------------------------------------------------------- helpers

def _as_list(x):
    """deque, list or tuple -> list. The contract is the order, not the type."""
    if x is None:
        return None
    return list(x)


def _ref_reverse(q):
    return list(q)[::-1]


def _ref_rotate(q, k):
    """
    Rotate RIGHT by k, as the exercise's own example states:
    [1,2,3,4,5], k=2 -> [4,5,1,2,3].
    """
    items = list(q)
    if not items:
        return []
    k %= len(items)
    return items[-k:] + items[:-k] if k else items


def _ref_track(operations):
    size = 0
    out = []
    for op in operations:
        name = op[0]
        if name == "enqueue":
            size += 1
        elif name == "dequeue" and size > 0:
            size -= 1
        out.append(size)
    return out


def _ref_deck(deck):
    """
    Invert the reveal process: sort, then deal from the back with a deque.

    The forward process is "reveal the top card, then move the next card to the
    bottom", so running it backwards means pushing the largest remaining card
    to the front after rotating the last card back to the front.
    """
    q = deque()
    for card in sorted(deck, reverse=True):
        if q:
            q.appendleft(q.pop())
        q.appendleft(card)
    return list(q)


def _ref_oranges(grid):
    rows, cols = len(grid), len(grid[0]) if grid else 0
    fresh = 0
    frontier = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                frontier.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    seen = {cell: 0 for cell in frontier}
    minutes = 0
    while frontier:
        r, c = frontier.popleft()
        t = seen[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 \
                    and (nr, nc) not in seen:
                seen[(nr, nc)] = t + 1
                fresh -= 1
                minutes = max(minutes, t + 1)
                frontier.append((nr, nc))
    return -1 if fresh else minutes


def _ref_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            count += 1
            stack = [(r, c)]
            seen.add((r, c))
            while stack:
                y, x = stack.pop()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < rows and 0 <= nx < cols \
                            and grid[ny][nx] == "1" and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        stack.append((ny, nx))
    return count


def _ref_shortest_path(grid):
    """0 is walkable, 1 is a wall. Returns the number of CELLS on the path."""
    if not grid or not grid[0]:
        return -1
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] != 0 or grid[rows - 1][cols - 1] != 0:
        return -1
    frontier = deque([(0, 0, 1)])
    seen = {(0, 0)}
    while frontier:
        r, c, dist = frontier.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return dist
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 \
                    and (nr, nc) not in seen:
                seen.add((nr, nc))
                frontier.append((nr, nc, dist + 1))
    return -1


def _ref_word_ladder(start, end, word_list):
    """Number of words in the sequence, both ends included. 0 if impossible."""
    words = set(word_list)
    if end not in words:
        return 0
    frontier = deque([(start, 1)])
    seen = {start}
    while frontier:
        word, length = frontier.popleft()
        if word == end:
            return length
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in words and nxt not in seen:
                    seen.add(nxt)
                    frontier.append((nxt, length + 1))
    return 0


# ------------------------------------------------------------------ builders

class _Node:
    """Duck-typed stand-in for a tree node (see the module docstring)."""

    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def _tree_from_level_order(values):
    """`values` is a level-order list with None for absent children."""
    if not values or values[0] is None:
        return None
    root = _Node(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.left = _Node(v)
                queue.append(node.left)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.right = _Node(v)
                queue.append(node.right)
    return root


def _ref_levels(root):
    if root is None:
        return []
    out = []
    frontier = deque([root])
    while frontier:
        out.append([n.val for n in frontier])
        nxt = deque()
        for node in frontier:
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        frontier = nxt
    return out


def g_queue(rng):
    return (deque(rng.randint(0, 30) for _ in range(rng.randint(0, 10))),)


def g_queue_k(rng):
    n = rng.randint(0, 8)
    return (deque(rng.randint(0, 30) for _ in range(n)), rng.randint(0, 10))


def g_ops(rng):
    ops = []
    for _ in range(rng.randint(0, 14)):
        if rng.random() < 0.6:
            ops.append(("enqueue", rng.randint(0, 9)))
        else:
            ops.append(("dequeue",))
    return (ops,)


def g_deck(rng):
    n = rng.randint(1, 10)
    return (rng.sample(range(1, 60), n),)


def g_orange_grid(rng):
    rows, cols = rng.randint(1, 5), rng.randint(1, 5)
    return ([[rng.choice([0, 1, 1, 2]) for _ in range(cols)]
             for _ in range(rows)],)


def g_island_grid(rng):
    rows, cols = rng.randint(1, 6), rng.randint(1, 6)
    return ([[rng.choice("0011") for _ in range(cols)]
             for _ in range(rows)],)


def g_path_grid(rng):
    rows, cols = rng.randint(1, 6), rng.randint(1, 6)
    grid = [[0 if rng.random() < 0.7 else 1 for _ in range(cols)]
            for _ in range(rows)]
    return (grid,)


def g_ladder(rng):
    """
    A small closed alphabet keeps a path reachable often enough to matter.

    Drawing from all 26 letters would make almost every case unreachable, so
    the test would only ever exercise the "return 0" branch.
    """
    letters = "abc"
    words = {"".join(rng.choice(letters) for _ in range(3))
             for _ in range(rng.randint(2, 12))}
    start = "".join(rng.choice(letters) for _ in range(3))
    end = "".join(rng.choice(letters) for _ in range(3))
    return (start, end, sorted(words))


def b_tree(module, rng):
    n = rng.randint(0, 12)
    values = [rng.randint(0, 50) if rng.random() < 0.85 else None
              for _ in range(n)]
    if values and values[0] is None:
        values[0] = 1
    return (_tree_from_level_order(values),)


def c_levels(module):
    return [
        ((_tree_from_level_order([1, 2, 3, 4, 5]),), [[1], [2, 3], [4, 5]]),
        ((_tree_from_level_order([1]),), [[1]]),
        ((None,), []),
    ]


SPECS = [
    spec(1, "Queue",
         script=lambda cls: (lambda q: [
             q.enqueue(1), q.enqueue(2), q.enqueue(3),
             q.dequeue(), q.front(), q.isEmpty(), q.size(),
         ][3:])(cls()),
         ref_script=lambda: [1, 2, False, 2],
         note="enqueue 1,2,3 then dequeue/front/isEmpty/size"),

    spec(2, "reverse_queue", ref=_ref_reverse, gen=g_queue,
         accept_inplace=True, prop=_as_list,
         cases=[((deque([1, 2, 3, 4, 5]),), [5, 4, 3, 2, 1]),
                ((deque(),), [])],
         note="either return the reversed queue or reverse it in place"),

    spec(3, "rotate_queue", ref=_ref_rotate, gen=g_queue_k,
         accept_inplace=True, prop=_as_list,
         cases=[((deque([1, 2, 3, 4, 5]), 2), [4, 5, 1, 2, 3]),
                ((deque([1, 2, 3]), 0), [1, 2, 3]),
                ((deque(), 3), [])],
         note="rotate RIGHT by k, as in the example; k may exceed the length. "
              "Either return the queue or rotate it in place"),

    spec(4, "track_queue_operations", ref=_ref_track, gen=g_ops,
         cases=[(([("enqueue", 5), ("enqueue", 10), ("dequeue",),
                   ("enqueue", 20)],), [1, 2, 1, 2]),
                (([],), [])],
         note="return the size AFTER each operation; a dequeue on an empty "
              "queue leaves the size at 0"),

    spec(5, "RecentCounter",
         script=lambda cls: (lambda c: [c.ping(t)
                                        for t in [1, 100, 3001, 3002]])(cls()),
         ref_script=lambda: [1, 2, 3, 3],
         note="ping(1),ping(100),ping(3001),ping(3002) -> only calls within "
              "[t-3000, t] count, so the last one drops ping(1)"),

    spec(6, "MovingAverage",
         script=lambda cls: (lambda m: [round(m.next(v), 4)
                                        for v in [1, 10, 3, 5]])(cls(3)),
         ref_script=lambda: [1.0, 5.5, 4.6667, 6.0],
         note="window of 3: averages of [1], [1,10], [1,10,3], [10,3,5]"),

    spec(7, "level_order_traversal", ref=_ref_levels, build=b_tree,
         build_cases=c_levels,
         note="root is handed to you with .val/.left/.right; you never build "
              "a tree yourself"),

    spec(8, "deck_revealed_increasing", ref=_ref_deck, gen=g_deck,
         cases=[(([17, 13, 11, 2, 3, 5, 7],), [2, 13, 3, 11, 5, 17, 7]),
                (([1],), [1])],
         note="return the deck order that reveals the cards in increasing "
              "order"),

    spec(9, "oranges_rotting", ref=_ref_oranges, gen=g_orange_grid,
         cases=[(([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4),
                (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1),
                (([[0, 2]],), 0)],
         note="-1 when a fresh orange can never rot; 0 when none are fresh"),

    spec(10, "num_islands", ref=_ref_islands, gen=g_island_grid,
         cases=[(([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
                   ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],), 3),
                (([["0"]],), 0)],
         note="the grid holds the STRINGS '1' and '0', not ints"),

    spec(11, "shortest_path_matrix", ref=_ref_shortest_path, gen=g_path_grid,
         cases=[(([[0, 0, 0], [1, 1, 0], [0, 0, 0]],), 5),
                (([[0, 1], [1, 0]],), -1),
                (([[0]],), 1)],
         note="0 is walkable and 1 is a wall; 4 directions; the answer counts "
              "CELLS on the path, so a 1x1 grid is 1. -1 when unreachable"),

    spec(12, "word_ladder", ref=_ref_word_ladder, gen=g_ladder,
         cases=[(("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
                (("a", "a", ["a"]), 1)],
         note="count the WORDS in the sequence including both ends; 0 when no "
              "transformation exists (the end word must be in the list)"),
]
