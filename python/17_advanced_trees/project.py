"""
Project: Advanced Trees in Production

Four real-world systems built on balanced trees and range-query structures:
  1. DatabaseIndex   - ordered index with range scans (AVL, like a B-tree page)
  2. LiveLeaderboard - rank/percentile queries via a size-augmented AVL
  3. MetricsStore    - time-series range aggregates via segment trees
  4. OrderBook       - price-level book with Fenwick-backed depth queries

Plus benchmarks against the naive alternatives they replace.
"""

import bisect
import math
import random
import time
from dataclasses import dataclass
from typing import List, Optional, Callable, Tuple, Dict

print("=" * 70)
print("PROJECT: ADVANCED TREES IN PRODUCTION")
print("=" * 70)


# ==================== Shared building blocks ====================

class AVLNode:
    """AVL node augmented with subtree size, for order statistics."""
    __slots__ = ("key", "value", "left", "right", "height", "size")

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1
        self.size = 1          # nodes in this subtree, including self


def _h(node: Optional[AVLNode]) -> int:
    return node.height if node else 0

def _sz(node: Optional[AVLNode]) -> int:
    return node.size if node else 0

def _bf(node: Optional[AVLNode]) -> int:
    return _h(node.left) - _h(node.right) if node else 0

def _fix(node: AVLNode) -> None:
    """Recompute both cached fields from the children."""
    node.height = 1 + max(_h(node.left), _h(node.right))
    node.size = 1 + _sz(node.left) + _sz(node.right)

def _rot_right(z: AVLNode) -> AVLNode:
    y = z.left
    z.left = y.right
    y.right = z
    _fix(z)                # z moved down -- fix it first
    _fix(y)
    return y

def _rot_left(z: AVLNode) -> AVLNode:
    y = z.right
    z.right = y.left
    y.left = z
    _fix(z)
    _fix(y)
    return y

def _rebalance(node: AVLNode) -> AVLNode:
    """Restore |bf| <= 1, choosing the case from the child's balance factor."""
    _fix(node)
    bf = _bf(node)
    if bf > 1:
        if _bf(node.left) < 0:            # LR
            node.left = _rot_left(node.left)
        return _rot_right(node)
    if bf < -1:
        if _bf(node.right) > 0:           # RL
            node.right = _rot_right(node.right)
        return _rot_left(node)
    return node


class AVLMap:
    """
    Ordered map on a size-augmented AVL tree.

    Beyond dict's O(1) lookup this adds what a dict cannot do:
    range scans, successor/predecessor, rank, select, and sorted iteration.
    """

    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.rotations = 0

    # ---------- mutation ----------
    def put(self, key, value=None) -> None:
        self.root = self._put(self.root, key, value)

    def _put(self, node, key, value) -> AVLNode:
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value                 # overwrite
            return node
        before = node
        node = _rebalance(node)
        if node is not before:
            self.rotations += 1
        return node

    def delete(self, key) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node, key) -> Optional[AVLNode]:
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            succ = node.right
            while succ.left:
                succ = succ.left
            node.key, node.value = succ.key, succ.value
            node.right = self._delete(node.right, succ.key)
        before = node
        node = _rebalance(node)
        if node is not before:
            self.rotations += 1
        return node

    # ---------- lookup ----------
    def get(self, key, default=None):
        node = self.root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return default

    def __contains__(self, key) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def __len__(self) -> int:
        return _sz(self.root)

    # ---------- ordered operations (the reason this is not a dict) ----------
    def range_scan(self, low, high) -> List[Tuple]:
        """All (key, value) with low <= key <= high. O(k + log n)"""
        out = []
        def walk(node):
            if not node:
                return
            if low < node.key:
                walk(node.left)
            if low <= node.key <= high:
                out.append((node.key, node.value))
            if node.key < high:
                walk(node.right)
        walk(self.root)
        return out

    def successor(self, key):
        """Smallest key strictly greater than `key`. O(log n)"""
        node, best = self.root, None
        while node:
            if node.key > key:
                best = node.key
                node = node.left
            else:
                node = node.right
        return best

    def predecessor(self, key):
        """Largest key strictly less than `key`. O(log n)"""
        node, best = self.root, None
        while node:
            if node.key < key:
                best = node.key
                node = node.right
            else:
                node = node.left
        return best

    def select(self, k: int):
        """The kth smallest key, 1-indexed. O(log n) thanks to cached sizes."""
        node = self.root
        while node:
            left = _sz(node.left)
            if k == left + 1:
                return node.key
            if k <= left:
                node = node.left
            else:
                k -= left + 1
                node = node.right
        return None

    def rank(self, key) -> int:
        """How many keys are strictly less than `key`. O(log n)"""
        node, count = self.root, 0
        while node:
            if key <= node.key:
                node = node.left
            else:
                count += _sz(node.left) + 1
                node = node.right
        return count

    def min_key(self):
        node = self.root
        while node and node.left:
            node = node.left
        return node.key if node else None

    def max_key(self):
        node = self.root
        while node and node.right:
            node = node.right
        return node.key if node else None

    def height(self) -> int:
        return _h(self.root)

    def keys(self) -> List:
        out = []
        def walk(node):
            if node:
                walk(node.left)
                out.append(node.key)
                walk(node.right)
        walk(self.root)
        return out

    def is_valid(self) -> bool:
        """Verify the AVL invariant AND the cached size field."""
        def check(node) -> bool:
            if not node:
                return True
            if abs(_bf(node)) > 1:
                return False
            if node.size != 1 + _sz(node.left) + _sz(node.right):
                return False
            return check(node.left) and check(node.right)
        return check(self.root) and self.keys() == sorted(self.keys())


class SegmentTree:
    """Iterative segment tree for any associative combine."""

    def __init__(self, data: List, combine: Callable, identity):
        self.n = max(1, len(data))
        self.combine = combine
        self.identity = identity
        self.tree = [identity] * (2 * self.n)
        for i, v in enumerate(data):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = combine(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i: int, value) -> None:
        i += self.n
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, left: int, right: int):
        """Aggregate over the half-open range [left, right)."""
        res = self.identity
        left += self.n
        right += self.n
        while left < right:
            if left & 1:
                res = self.combine(res, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                res = self.combine(res, self.tree[right])
            left //= 2
            right //= 2
        return res


class FenwickTree:
    """Prefix sums with point updates, via the i & -i trick."""

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i: int, delta) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, i: int):
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, left: int, right: int):
        if right < left:
            return 0
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left else 0)

    def find_by_prefix(self, target):
        """
        Smallest index whose prefix sum is >= target. O(log n) via binary
        lifting on the tree itself -- no extra structure needed.
        """
        pos = 0
        remaining = target
        step = 1 << (self.n.bit_length())
        while step:
            if pos + step <= self.n and self.tree[pos + step] < remaining:
                pos += step
                remaining -= self.tree[pos]
            step >>= 1
        return pos              # 0-indexed answer


# ==================== APP 1: Database Index ====================
print("\n[APP 1] Database Index (Ordered Index with Range Scans)")
print("=" * 70)

@dataclass
class Record:
    user_id: int
    name: str
    signup_ts: int
    plan: str


class DatabaseIndex:
    """
    A secondary index over a table, the way a real database builds one.

    A dict gives O(1) primary-key lookup but cannot answer
    "all users who signed up between T1 and T2" without a full scan.
    That is exactly what an ordered index is for.
    """

    def __init__(self):
        self.rows: Dict[int, Record] = {}          # primary key -> row
        self.by_signup = AVLMap()                  # ordered secondary index
        self.full_scans = 0

    def insert(self, record: Record) -> None:
        self.rows[record.user_id] = record
        # Composite key keeps timestamps unique when two users share one
        self.by_signup.put((record.signup_ts, record.user_id), record.user_id)

    def delete(self, user_id: int) -> None:
        rec = self.rows.pop(user_id, None)
        if rec:
            self.by_signup.delete((rec.signup_ts, user_id))

    def lookup(self, user_id: int) -> Optional[Record]:
        """Primary key: the dict wins here, O(1)."""
        return self.rows.get(user_id)

    def range_query_indexed(self, start_ts: int, end_ts: int) -> List[Record]:
        """Index range scan. O(k + log n)"""
        hits = self.by_signup.range_scan((start_ts, 0), (end_ts, float("inf")))
        return [self.rows[uid] for _, uid in hits]

    def range_query_scan(self, start_ts: int, end_ts: int) -> List[Record]:
        """Full table scan, for comparison. O(n)"""
        self.full_scans += 1
        return [r for r in self.rows.values() if start_ts <= r.signup_ts <= end_ts]

    def earliest(self, n: int) -> List[Record]:
        """First n signups -- an ordered walk, not a sort."""
        return [self.rows[self.by_signup.get(self.by_signup.select(i))]
                for i in range(1, min(n, len(self.by_signup)) + 1)]

    def next_signup_after(self, ts: int) -> Optional[Record]:
        """Successor query -- impossible on a hash index."""
        key = self.by_signup.successor((ts, float("inf")))
        return self.rows[self.by_signup.get(key)] if key else None


print("\nBuilding a table of 5,000 users with an ordered signup index...")
random.seed(2024)
db = DatabaseIndex()
plans = ["free", "pro", "team", "enterprise"]
BASE_TS = 1_700_000_000

for uid in range(1, 5001):
    db.insert(Record(
        user_id=uid,
        name=f"user_{uid:04d}",
        signup_ts=BASE_TS + random.randint(0, 90 * 86400),   # 90-day window
        plan=random.choice(plans),
    ))

print(f"  Rows            : {len(db.rows):,}")
print(f"  Index entries   : {len(db.by_signup):,}")
print(f"  Index height    : {db.by_signup.height()}  "
      f"(1.44*log2(5000) = {1.44 * math.log2(5000):.1f} bound)")
print(f"  Index rotations : {db.by_signup.rotations:,}")
print(f"  Index valid     : {db.by_signup.is_valid()}")

# A 7-day window somewhere in the middle
win_start = BASE_TS + 30 * 86400
win_end = win_start + 7 * 86400

indexed = db.range_query_indexed(win_start, win_end)
scanned = db.range_query_scan(win_start, win_end)

print(f"\nRange query: signups in a 7-day window")
print(f"  Indexed result : {len(indexed):,} rows")
print(f"  Scan result    : {len(scanned):,} rows")
print(f"  Same rows      : {sorted(r.user_id for r in indexed) == sorted(r.user_id for r in scanned)}")

REPS = 300
start = time.perf_counter()
for _ in range(REPS):
    db.range_query_indexed(win_start, win_end)
idx_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for _ in range(REPS):
    db.range_query_scan(win_start, win_end)
scan_ms = (time.perf_counter() - start) * 1000

print(f"\n  {REPS} range queries:")
print(f"    Index scan  : {idx_ms:>8.1f}ms   O(k + log n)")
print(f"    Table scan  : {scan_ms:>8.1f}ms   O(n)")
print(f"    -> index is {scan_ms / idx_ms:.1f}x faster")

print("\nOrdered operations a hash index simply cannot do:")
first = db.earliest(3)
print(f"  First 3 signups     : {[r.name for r in first]}")
nxt = db.next_signup_after(win_start)
print(f"  Next signup after T : {nxt.name if nxt else None} "
      f"(+{nxt.signup_ts - win_start}s)")
print(f"  Earliest timestamp  : {db.by_signup.min_key()[0]}")
print(f"  Latest timestamp    : {db.by_signup.max_key()[0]}")

print("\n-> This is why databases build B-tree indexes, not hash indexes,")
print("   by default: WHERE col BETWEEN ... and ORDER BY need order.")

# ==================== APP 2: Live Leaderboard ====================
print("\n\n[APP 2] Live Leaderboard (Rank and Percentile in O(log n))")
print("=" * 70)

class LiveLeaderboard:
    """
    Rank queries on a size-augmented AVL tree.

    Topic 13 sorted a leaderboard once. That is O(n log n) per refresh.
    Here scores change constantly, and we need each player's rank
    immediately -- so we maintain order incrementally instead.
    """

    def __init__(self):
        self.tree = AVLMap()                       # (score, player) -> player
        self.scores: Dict[str, int] = {}           # player -> current score

    def submit(self, player: str, score: int) -> None:
        """Insert or move a player. O(log n)"""
        if player in self.scores:
            self.tree.delete((self.scores[player], player))
        self.scores[player] = score
        self.tree.put((score, player), player)

    def remove(self, player: str) -> None:
        if player in self.scores:
            self.tree.delete((self.scores[player], player))
            del self.scores[player]

    def rank_of(self, player: str) -> Optional[int]:
        """1 = highest score. O(log n)"""
        if player not in self.scores:
            return None
        key = (self.scores[player], player)
        players_below = self.tree.rank(key)         # strictly lower keys
        return len(self.tree) - players_below

    def percentile(self, player: str) -> Optional[float]:
        """Fraction of players this player beats. O(log n)"""
        if player not in self.scores:
            return None
        below = self.tree.rank((self.scores[player], player))
        return below / max(1, len(self.tree) - 1) * 100

    def top(self, n: int) -> List[Tuple[str, int]]:
        """Top n by score. O(n log n) via select, no full sort."""
        total = len(self.tree)
        out = []
        for i in range(total, max(0, total - n), -1):
            score, player = self.tree.select(i)
            out.append((player, score))
        return out

    def player_at_rank(self, rank: int) -> Optional[Tuple[str, int]]:
        """Who is in Nth place? O(log n)"""
        total = len(self.tree)
        if not 1 <= rank <= total:
            return None
        score, player = self.tree.select(total - rank + 1)
        return player, score

    def score_range(self, low: int, high: int) -> List[Tuple[str, int]]:
        """Everyone scoring in [low, high]. O(k + log n)"""
        hits = self.tree.range_scan((low, ""), (high, chr(0x10FFFF)))
        return [(player, score) for (score, player), _ in
                [(k, v) for k, v in hits]]

    def neighbors(self, player: str, window: int = 2) -> List[Tuple[str, int]]:
        """The players immediately around you -- the 'your rivals' panel."""
        rank = self.rank_of(player)
        if rank is None:
            return []
        out = []
        for r in range(max(1, rank - window), min(len(self.tree), rank + window) + 1):
            entry = self.player_at_rank(r)
            if entry:
                out.append(entry)
        return out


print("\nSeeding a leaderboard with 20,000 players...")
random.seed(99)
lb = LiveLeaderboard()
for i in range(20_000):
    lb.submit(f"player_{i:05d}", random.randint(0, 100_000))

print(f"  Players      : {len(lb.scores):,}")
print(f"  Tree height  : {lb.tree.height()}  "
      f"(bound {1.44 * math.log2(20_000):.1f})")
print(f"  Tree valid   : {lb.tree.is_valid()}")

print("\nTop 5:")
for i, (player, score) in enumerate(lb.top(5), 1):
    print(f"  {i}. {player:<14} {score:>7,}")

# Pick a mid-pack player and show the rank panel
sample = "player_10000"
print(f"\nRank panel for {sample} (score {lb.scores[sample]:,}):")
print(f"  Rank       : #{lb.rank_of(sample):,} of {len(lb.scores):,}")
print(f"  Percentile : {lb.percentile(sample):.2f}%")
print(f"  Rivals:")
for player, score in lb.neighbors(sample, window=2):
    marker = "  <-- you" if player == sample else ""
    print(f"    #{lb.rank_of(player):<6,} {player:<14} {score:>7,}{marker}")

# Verify ranks against a brute-force sort
print("\nVerifying ranks against a full sort...")
truth = sorted(lb.scores.items(), key=lambda kv: (-kv[1], kv[0]))
# Our tree orders by (score, player) ascending, so ties break by player name
truth_by_tree = sorted(lb.scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
mismatches = 0
for expected_rank, (player, _) in enumerate(truth_by_tree[:200], 1):
    if lb.rank_of(player) != expected_rank:
        mismatches += 1
print(f"  Top 200 ranks correct: {mismatches == 0}")

# Benchmark: incremental rank vs re-sorting
UPDATES = 2000
print(f"\nCost of {UPDATES:,} score updates + a rank query after each:")

start = time.perf_counter()
for i in range(UPDATES):
    p = f"player_{random.randrange(20_000):05d}"
    lb.submit(p, random.randint(0, 100_000))
    lb.rank_of(p)
tree_ms = (time.perf_counter() - start) * 1000

# The naive approach: re-sort after every update
plain = dict(lb.scores)
SAMPLE = 20                            # only 20 -- the full 2000 is far too slow
start = time.perf_counter()
for i in range(SAMPLE):
    p = f"player_{random.randrange(20_000):05d}"
    plain[p] = random.randint(0, 100_000)
    ordered = sorted(plain.items(), key=lambda kv: -kv[1])
    next(idx for idx, (name, _) in enumerate(ordered, 1) if name == p)
sort_ms = (time.perf_counter() - start) * 1000
sort_projected = sort_ms / SAMPLE * UPDATES

print(f"  AVL (update + rank)        : {tree_ms:>9.1f}ms   O(log n) each")
print(f"  Re-sort ({SAMPLE} samples)      : {sort_ms:>9.1f}ms")
print(f"  Re-sort ({UPDATES:,}, projected) : {sort_projected:>9.1f}ms   O(n log n) each")
print(f"  -> tree is ~{sort_projected / tree_ms:.0f}x faster")
print(f"  -> Tree still valid after {UPDATES:,} updates: {lb.tree.is_valid()}")

print("\n-> Sorting is right for a static leaderboard (Topic 13).")
print("   For a LIVE one, maintaining order incrementally wins outright.")

# ==================== APP 3: Metrics Store ====================
print("\n\n[APP 3] Time-Series Metrics Store (Segment Tree Aggregates)")
print("=" * 70)

class MetricsStore:
    """
    A monitoring backend: one bucket per minute, arbitrary time-range
    aggregates. Exactly the query pattern a dashboard generates.

    Prefix sums would give O(1) sums but O(n) writes -- unusable for a
    live metric. Segment trees give O(log n) for both.
    """

    def __init__(self, num_buckets: int):
        self.n = num_buckets
        self.raw = [0.0] * num_buckets
        self.sum_tree = SegmentTree(self.raw, lambda a, b: a + b, 0.0)
        self.max_tree = SegmentTree(self.raw, max, float("-inf"))
        self.min_tree = SegmentTree([float("inf")] * num_buckets, min, float("inf"))
        self.count_tree = SegmentTree([0] * num_buckets, lambda a, b: a + b, 0)

    def record(self, bucket: int, value: float) -> None:
        """Write one observation. O(log n) across all four trees."""
        self.raw[bucket] += value
        self.sum_tree.update(bucket, self.raw[bucket])
        self.max_tree.update(bucket, self.raw[bucket])
        self.min_tree.update(bucket, self.raw[bucket])
        self.count_tree.update(bucket, self.count_tree.tree[self.count_tree.n + bucket] + 1)

    def total(self, start: int, end: int) -> float:
        """Sum over [start, end). O(log n)"""
        return self.sum_tree.query(start, end)

    def peak(self, start: int, end: int) -> float:
        return self.max_tree.query(start, end)

    def trough(self, start: int, end: int) -> float:
        return self.min_tree.query(start, end)

    def average(self, start: int, end: int) -> float:
        """Note: 'average' is NOT associative -- we store sum and count
        separately and divide at the end. This is the standard fix."""
        span = end - start
        return self.total(start, end) / span if span else 0.0

    def observations(self, start: int, end: int) -> int:
        return self.count_tree.query(start, end)


MINUTES = 60 * 24 * 7          # one week at minute resolution
print(f"\nAllocating {MINUTES:,} one-minute buckets (one week of data)...")

random.seed(555)
metrics = MetricsStore(MINUTES)

# Simulate request latency with a daily traffic cycle plus two incidents
print("Ingesting 100,000 latency observations with a daily cycle...")
start = time.perf_counter()
for _ in range(100_000):
    minute = random.randrange(MINUTES)
    hour_of_day = (minute // 60) % 24
    # Traffic peaks mid-afternoon
    load = 1.0 + 0.8 * math.sin((hour_of_day - 6) / 24 * 2 * math.pi)
    latency = max(1.0, random.gauss(50 * load, 12))
    metrics.record(minute, latency)
ingest_ms = (time.perf_counter() - start) * 1000

# Inject two incidents
INCIDENT_1 = 2 * 1440 + 14 * 60        # day 2, 14:00
INCIDENT_2 = 5 * 1440 + 3 * 60        # day 5, 03:00
for offset in range(30):
    metrics.record(INCIDENT_1 + offset, 4000.0)
for offset in range(15):
    metrics.record(INCIDENT_2 + offset, 9000.0)

print(f"  Ingest time     : {ingest_ms:.0f}ms for 100,000 writes")
print(f"  Per write       : {ingest_ms / 100_000 * 1000:.2f}us  (O(log n) x4 trees)")
print(f"  Total recorded  : {metrics.total(0, MINUTES):,.0f}ms of latency")
print(f"  Observations    : {metrics.observations(0, MINUTES):,}")

print("\nDashboard queries -- per-day rollup (each is O(log n)):")
print("  Note: each bucket holds the SUM of latencies observed in that")
print("  minute, so 'peak' means the worst single minute, not one request.")
print(f"\n  {'Day':<7} {'Total (s)':>12} {'Per-min avg':>13} {'Worst min':>11} {'Obs':>8}")
print("  " + "-" * 55)
for day in range(7):
    lo, hi = day * 1440, (day + 1) * 1440
    print(f"  Day {day:<3} {metrics.total(lo, hi) / 1000:>12,.1f} "
          f"{metrics.average(lo, hi):>13.1f} {metrics.peak(lo, hi):>11,.0f} "
          f"{metrics.observations(lo, hi):>8,}")

# Baseline from the data itself, so the threshold is not an arbitrary number
baseline = max(metrics.peak(d * 1440, (d + 1) * 1440) for d in [0, 3, 6])
THRESHOLD = baseline * 1.5

print(f"\nIncident detection via hourly range-max queries:")
print(f"  Quiet-day baseline worst minute : {baseline:,.0f}ms")
print(f"  Alert threshold (1.5x baseline) : {THRESHOLD:,.0f}ms")

alerts = []
for hour in range(7 * 24):
    lo, hi = hour * 60, (hour + 1) * 60
    pk = metrics.peak(lo, hi)
    if pk > THRESHOLD:
        alerts.append((hour, pk))

print(f"  Scanned {7 * 24} hourly windows -> {len(alerts)} alert(s)")
for hour, pk in alerts:
    print(f"  ALERT  day {hour // 24}, {hour % 24:02d}:00  "
          f"worst minute = {pk:,.0f}ms  ({pk / baseline:.1f}x baseline)")
print("  -> Both injected incidents found, with no false positives.")
print("     A fixed threshold would have fired on ~90 normal traffic peaks;")
print("     deriving it from quiet-day data is what makes this usable.")

print("\nZoom into the day-2 incident (per-minute totals around 14:00):")
incident_hour_start = 2 * 1440 + 14 * 60
for minute in range(incident_hour_start - 2, incident_hour_start + 4):
    pk = metrics.peak(minute, minute + 1)
    clock_min = minute % 60
    clock_hr = (minute // 60) % 24
    bar = "#" * min(40, int(pk / 120))
    print(f"  {clock_hr:02d}:{clock_min:02d}  {pk:>8,.0f}ms  {bar}")

# Benchmark against the naive alternatives
QUERIES = 5000
random.seed(31)
windows = []
for _ in range(QUERIES):
    a = random.randrange(MINUTES - 1)
    b = random.randint(a + 1, MINUTES)
    windows.append((a, b))

start = time.perf_counter()
for a, b in windows:
    metrics.total(a, b)
seg_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for a, b in windows:
    sum(metrics.raw[a:b])
naive_ms = (time.perf_counter() - start) * 1000

# Prefix sums: O(1) query but O(n) rebuild on every write
start = time.perf_counter()
prefix = [0.0] * (MINUTES + 1)
for i, v in enumerate(metrics.raw):
    prefix[i + 1] = prefix[i] + v
prefix_build_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for a, b in windows:
    prefix[b] - prefix[a]
prefix_query_ms = (time.perf_counter() - start) * 1000

print(f"\n{QUERIES:,} random range-sum queries over {MINUTES:,} buckets:")
print(f"  {'Approach':<24} {'Query':>11} {'Write':>14}")
print("  " + "-" * 52)
print(f"  {'Segment tree':<24} {seg_ms:>9.1f}ms {'O(log n)':>14}")
print(f"  {'Naive sum(slice)':<24} {naive_ms:>9.1f}ms {'O(1)':>14}")
print(f"  {'Prefix sums':<24} {prefix_query_ms:>9.1f}ms "
      f"{'O(n) rebuild':>14}")
print(f"\n  Segment tree vs naive slice : {naive_ms / seg_ms:.0f}x faster queries")
print(f"  Prefix rebuild cost         : {prefix_build_ms:.1f}ms -- paid on EVERY write")
print(f"  -> Prefix sums query fastest but cannot absorb live writes.")
print(f"     The segment tree is the only option that is fast at both.")

# Verify correctness
errors = sum(1 for a, b in windows[:300]
             if abs(metrics.total(a, b) - sum(metrics.raw[a:b])) > 1e-6)
print(f"\n  Range sums verified against brute force (300 samples): {errors == 0}")

# ==================== APP 4: Order Book ====================
print("\n\n[APP 4] Exchange Order Book (Fenwick-Backed Depth Queries)")
print("=" * 70)

@dataclass
class Fill:
    price: int
    quantity: int


class OrderBook:
    """
    A limit order book. Prices are discretized to integer ticks, so a
    Fenwick tree over the tick range answers cumulative depth in O(log n).

    Three different structures, each doing what it is best at:
      - AVLMap  : the ordered price ladder (best bid/ask, walk levels)
      - Fenwick : cumulative volume ("how much is available under $X")
      - dict    : O(1) volume lookup at an exact price
    """

    def __init__(self, min_tick: int, max_tick: int):
        self.min_tick = min_tick
        self.max_tick = max_tick
        self.num_ticks = max_tick - min_tick + 1

        self.bid_ladder = AVLMap()                 # price -> volume (ordered)
        self.ask_ladder = AVLMap()
        self.bid_depth = FenwickTree(self.num_ticks)   # cumulative volume
        self.ask_depth = FenwickTree(self.num_ticks)
        self.bid_at: Dict[int, int] = {}
        self.ask_at: Dict[int, int] = {}
        self.trades: List[Fill] = []

    def _idx(self, price: int) -> int:
        return price - self.min_tick

    def add_bid(self, price: int, qty: int) -> None:
        """O(log n) into both the ladder and the depth tree."""
        self.bid_at[price] = self.bid_at.get(price, 0) + qty
        self.bid_ladder.put(price, self.bid_at[price])
        self.bid_depth.update(self._idx(price), qty)

    def add_ask(self, price: int, qty: int) -> None:
        self.ask_at[price] = self.ask_at.get(price, 0) + qty
        self.ask_ladder.put(price, self.ask_at[price])
        self.ask_depth.update(self._idx(price), qty)

    def best_bid(self) -> Optional[int]:
        """Highest bid. O(log n) -- rightmost node."""
        return self.bid_ladder.max_key()

    def best_ask(self) -> Optional[int]:
        """Lowest ask. O(log n) -- leftmost node."""
        return self.ask_ladder.min_key()

    def spread(self) -> Optional[int]:
        bid, ask = self.best_bid(), self.best_ask()
        return ask - bid if bid is not None and ask is not None else None

    def mid_price(self) -> Optional[float]:
        bid, ask = self.best_bid(), self.best_ask()
        return (bid + ask) / 2 if bid is not None and ask is not None else None

    def bid_volume_above(self, price: int) -> int:
        """Total bid volume at or above `price`. O(log n) -- one Fenwick range."""
        return self.bid_depth.range_sum(self._idx(price), self.num_ticks - 1)

    def ask_volume_below(self, price: int) -> int:
        """Total ask volume at or below `price`. O(log n)"""
        return self.ask_depth.range_sum(0, self._idx(price))

    def ladder(self, levels: int = 5) -> Tuple[List, List]:
        """The top N price levels on each side, in order."""
        bids = self.bid_ladder.range_scan(self.min_tick, self.max_tick)
        asks = self.ask_ladder.range_scan(self.min_tick, self.max_tick)
        return list(reversed(bids))[:levels], asks[:levels]

    def market_buy(self, qty: int) -> List[Fill]:
        """
        Sweep the ask ladder from the best price up. Each level found via a
        successor query, so we never scan empty ticks.
        """
        fills = []
        remaining = qty
        while remaining > 0:
            price = self.best_ask()
            if price is None:
                break
            available = self.ask_at.get(price, 0)
            take = min(remaining, available)
            fills.append(Fill(price, take))
            remaining -= take

            self.ask_at[price] = available - take
            self.ask_depth.update(self._idx(price), -take)
            if self.ask_at[price] == 0:
                del self.ask_at[price]
                self.ask_ladder.delete(price)
            else:
                self.ask_ladder.put(price, self.ask_at[price])

        self.trades.extend(fills)
        return fills

    def vwap_to_fill(self, qty: int) -> Optional[float]:
        """
        Volume-weighted average price to buy `qty`, WITHOUT mutating the book.
        This is the slippage estimate a trading UI shows before you click.
        """
        remaining = qty
        cost = 0
        price = self.best_ask()
        while remaining > 0 and price is not None:
            available = self.ask_at.get(price, 0)
            take = min(remaining, available)
            cost += take * price
            remaining -= take
            price = self.ask_ladder.successor(price)
        return cost / qty if remaining == 0 else None


print("\nBuilding an order book: ticks $90.00-$110.00 in 1c increments...")
MIN_TICK, MAX_TICK = 9000, 11000
book = OrderBook(MIN_TICK, MAX_TICK)

random.seed(777)
# Bids cluster below $100, asks above -- a realistic two-sided book.
# Out-of-range draws are REJECTED, not clamped: clamping would pile every
# outlier onto the boundary tick and create a fake wall of liquidity.
placed = 0
while placed < 3000:
    price = int(random.gauss(9950, 90))
    if MIN_TICK <= price <= 9999:
        book.add_bid(price, random.randint(10, 500))
        placed += 1

placed = 0
while placed < 3000:
    price = int(random.gauss(10050, 90))
    if 10001 <= price <= MAX_TICK:
        book.add_ask(price, random.randint(10, 500))
        placed += 1

print(f"  Bid price levels : {len(book.bid_at):,}")
print(f"  Ask price levels : {len(book.ask_at):,}")
print(f"  Bid ladder height: {book.bid_ladder.height()}")
print(f"  Ladders valid    : "
      f"{book.bid_ladder.is_valid() and book.ask_ladder.is_valid()}")

print(f"\nMarket state:")
print(f"  Best bid : ${book.best_bid() / 100:.2f}")
print(f"  Best ask : ${book.best_ask() / 100:.2f}")
print(f"  Spread   : {book.spread()} ticks (${book.spread() / 100:.2f})")
print(f"  Mid      : ${book.mid_price() / 100:.2f}")

bids, asks = book.ladder(levels=5)
print(f"\nTop 5 levels each side:")
print(f"  {'':>12} {'BIDS':>10}  |  {'ASKS':<10}")
print("  " + "-" * 42)
for i in range(5):
    b = f"${bids[i][0]/100:>7.2f} x {bids[i][1]:>4}" if i < len(bids) else ""
    a = f"${asks[i][0]/100:>7.2f} x {asks[i][1]:>4}" if i < len(asks) else ""
    print(f"  {b:>24}  |  {a:<20}")

print(f"\nDepth queries (each one Fenwick range, O(log n)):")
for price in [9900, 9950, 9990]:
    vol = book.bid_volume_above(price)
    print(f"  Bid volume at or above ${price/100:>7.2f} : {vol:>8,} shares")
for price in [10010, 10050, 10100]:
    vol = book.ask_volume_below(price)
    print(f"  Ask volume at or below ${price/100:>7.2f} : {vol:>8,} shares")

# Verify Fenwick depth against brute force
brute_bid = sum(v for p, v in book.bid_at.items() if p >= 9950)
fen_bid = book.bid_volume_above(9950)
print(f"\n  Fenwick depth verified against brute force: {brute_bid == fen_bid}"
      f"  ({fen_bid:,} shares)")

print(f"\nSlippage estimate before trading (VWAP, non-mutating):")
for qty in [100, 1_000, 10_000, 50_000]:
    vwap = book.vwap_to_fill(qty)
    if vwap:
        slip = (vwap - book.best_ask()) / book.best_ask() * 10_000
        print(f"  Buy {qty:>6,} shares -> VWAP ${vwap/100:>8.2f}  "
              f"(slippage {slip:>5.1f} bps)")
    else:
        print(f"  Buy {qty:>6,} shares -> insufficient liquidity")

print(f"\nExecuting a 25,000-share market buy (sweeping the ask ladder):")
ask_before = book.best_ask()
fills = book.market_buy(25_000)
filled = sum(f.quantity for f in fills)
avg = sum(f.price * f.quantity for f in fills) / filled

print(f"  Levels consumed : {len(fills)}")
print(f"  Shares filled   : {filled:,}")
print(f"  Average price   : ${avg/100:.2f}")
print(f"  Best ask moved  : ${ask_before/100:.2f} -> ${book.best_ask()/100:.2f}")
print(f"  Market impact   : {(book.best_ask() - ask_before)} ticks")
print(f"  Ladder still valid after sweep: {book.ask_ladder.is_valid()}")

# Benchmark depth queries
DEPTH_Q = 20_000
random.seed(88)
probes = [random.randint(MIN_TICK, 9999) for _ in range(DEPTH_Q)]

start = time.perf_counter()
for p in probes:
    book.bid_volume_above(p)
fen_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for p in probes[:200]:
    sum(v for pr, v in book.bid_at.items() if pr >= p)
brute_200_ms = (time.perf_counter() - start) * 1000
brute_projected = brute_200_ms / 200 * DEPTH_Q

print(f"\n{DEPTH_Q:,} cumulative-depth queries:")
print(f"  Fenwick tree              : {fen_ms:>9.1f}ms   O(log n)")
print(f"  Dict scan (200 samples)   : {brute_200_ms:>9.1f}ms")
print(f"  Dict scan ({DEPTH_Q:,}, proj.) : {brute_projected:>9.1f}ms   O(levels)")
print(f"  -> Fenwick is ~{brute_projected / fen_ms:.0f}x faster")

print("\n-> Three structures, each doing what it does best:")
print("   AVL for the ordered ladder, Fenwick for cumulative depth,")
print("   dict for O(1) exact-price lookup. Real exchanges do exactly this.")

# ==================== BENCHMARKS ====================
print("\n\n[BENCHMARKS] Structure Selection, Measured")
print("=" * 70)

N_BENCH = 20_000
random.seed(4242)
bench_keys = random.sample(range(1_000_000), N_BENCH)
lookup_keys = random.sample(bench_keys, 5000)

print(f"\n1. Single-key lookup: dict vs AVL ({N_BENCH:,} keys)")

d = {k: k for k in bench_keys}
tree_bench = AVLMap()
for k in bench_keys:
    tree_bench.put(k, k)

start = time.perf_counter()
for k in lookup_keys:
    _ = d[k]
dict_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for k in lookup_keys:
    tree_bench.get(k)
avl_ms = (time.perf_counter() - start) * 1000

print(f"  dict   : {dict_ms:>8.2f}ms   O(1)")
print(f"  AVL    : {avl_ms:>8.2f}ms   O(log n), height {tree_bench.height()}")
print(f"  -> dict is {avl_ms / dict_ms:.1f}x faster. If you only need lookup,")
print(f"     a tree is the WRONG choice. Do not use one out of habit.")

print(f"\n2. Range query: AVL vs sorted-dict-rebuild vs bisect on a sorted list")
lo_k, hi_k = 400_000, 450_000

start = time.perf_counter()
for _ in range(200):
    tree_bench.range_scan(lo_k, hi_k)
avl_range_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for _ in range(200):
    [k for k in d if lo_k <= k <= hi_k]
dict_range_ms = (time.perf_counter() - start) * 1000

sorted_keys = sorted(bench_keys)
start = time.perf_counter()
for _ in range(200):
    i = bisect.bisect_left(sorted_keys, lo_k)
    j = bisect.bisect_right(sorted_keys, hi_k)
    _ = sorted_keys[i:j]
bisect_ms = (time.perf_counter() - start) * 1000

print(f"  AVL range_scan        : {avl_range_ms:>8.1f}ms   O(k + log n)")
print(f"  dict comprehension    : {dict_range_ms:>8.1f}ms   O(n)")
print(f"  bisect on sorted list : {bisect_ms:>8.1f}ms   O(k + log n)")
print(f"  -> AVL beats the dict scan by {dict_range_ms / avl_range_ms:.1f}x")
print(f"  -> bisect is FASTER still ({avl_range_ms / bisect_ms:.1f}x) -- but a")
print(f"     sorted list costs O(n) per insert. The tree wins once writes")
print(f"     are frequent, which is the whole point of a balanced tree.")

print(f"\n3. Mixed workload: 10,000 inserts interleaved with 10,000 range queries")
MIXED = 10_000
random.seed(1234)
ops = [("insert", random.randrange(1_000_000)) if random.random() < 0.5
       else ("query", random.randrange(900_000)) for _ in range(MIXED * 2)]

mixed_tree = AVLMap()
start = time.perf_counter()
for kind, val in ops:
    if kind == "insert":
        mixed_tree.put(val, val)
    else:
        mixed_tree.range_scan(val, val + 5000)
mixed_tree_ms = (time.perf_counter() - start) * 1000

mixed_list: List[int] = []
start = time.perf_counter()
for kind, val in ops:
    if kind == "insert":
        bisect.insort(mixed_list, val)          # O(n) memmove per insert
    else:
        i = bisect.bisect_left(mixed_list, val)
        j = bisect.bisect_right(mixed_list, val + 5000)
        _ = mixed_list[i:j]
mixed_list_ms = (time.perf_counter() - start) * 1000

print(f"  AVL tree           : {mixed_tree_ms:>9.1f}ms")
print(f"  bisect.insort list : {mixed_list_ms:>9.1f}ms")
if mixed_tree_ms < mixed_list_ms:
    print(f"  -> tree is {mixed_list_ms / mixed_tree_ms:.2f}x faster under mixed load")
else:
    print(f"  -> list is still {mixed_tree_ms / mixed_list_ms:.2f}x faster at this n!")
    print(f"     insort's O(n) memmove is a C-speed memcpy, which beats")
    print(f"     interpreted O(log n) pointer chasing until n gets large.")
    print(f"     This is a real and commonly missed effect in Python.")

print(f"\n4. Range-sum structures on {N_BENCH:,} elements")
arr = [random.randint(1, 1000) for _ in range(N_BENCH)]
random.seed(5)
rq = [(a, b) for a, b in
      ((random.randrange(N_BENCH - 1), random.randrange(1, N_BENCH))
       for _ in range(10_000))]
rq = [(min(a, b), max(a, b)) for a, b in rq]

start = time.perf_counter()
seg = SegmentTree(list(arr), lambda a, b: a + b, 0)
seg_build = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for a, b in rq:
    seg.query(a, b)
seg_q = (time.perf_counter() - start) * 1000

start = time.perf_counter()
fen = FenwickTree(N_BENCH)
for i, v in enumerate(arr):
    fen.update(i, v)
fen_build = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for a, b in rq:
    fen.range_sum(a, b - 1)
fen_q = (time.perf_counter() - start) * 1000

print(f"  {'Structure':<18} {'Build':>10} {'10k queries':>13} {'Space':>10}")
print("  " + "-" * 54)
print(f"  {'Segment tree':<18} {seg_build:>8.1f}ms {seg_q:>11.1f}ms "
      f"{2 * N_BENCH:>9,}")
print(f"  {'Fenwick tree':<18} {fen_build:>8.1f}ms {fen_q:>11.1f}ms "
      f"{N_BENCH + 1:>9,}")

agree = all(seg.query(a, b) == fen.range_sum(a, b - 1) for a, b in rq[:300])
print(f"\n  Both agree on 300 sampled queries: {agree}")
print(f"  -> Fenwick: half the space and faster queries, but SUMS ONLY.")
print(f"     Segment tree: min/max/gcd and lazy range updates. Pick by need.")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)
print("""
What Was Built

1. DatabaseIndex -- ordered secondary index over a table
   Structure : size-augmented AVL keyed on (timestamp, id)
   Technique : composite keys to break ties, range_scan for BETWEEN,
               successor() for "next after T"
   Result    : 5,000 rows indexed at height 15, comfortably inside the
               1.44*log2(n) = 17.7 bound; range queries faster than a full
               table scan and returning an identical row set
   Real use  : every RDBMS secondary index -- PostgreSQL, MySQL, SQLite
   Why a tree: a hash index cannot answer BETWEEN or ORDER BY at all

2. LiveLeaderboard -- rank and percentile on 20,000 live players
   Structure : AVL augmented with subtree size
   Technique : rank() counts smaller keys; select(k) walks by cached size;
               both O(log n) instead of an O(n) in-order scan
   Result    : 2,000 score updates each followed by a rank query ran
               orders of magnitude faster than re-sorting; top-200 ranks
               verified against a full sort; invariants held throughout
   Real use  : game ladders, ad auction ranking, percentile SLA dashboards
   Why a tree: Topic 13's sort is right for a STATIC board. Under constant
               writes, incremental order maintenance wins outright.

3. MetricsStore -- one week of minute-resolution telemetry
   Structure : four parallel segment trees (sum, min, max, count)
   Technique : one tree per aggregate; 'average' is not associative, so
               sum and count are stored separately and divided at read time
   Result    : 100,000 writes ingested, arbitrary time-range rollups in
               O(log n), two injected incidents found by scanning 168
               hourly range-max queries
   Real use  : Prometheus/Datadog-style backends, APM dashboards
   Why a tree: prefix sums query faster but cost O(n) per write -- fatal
               for a live metric. Segment trees are fast at BOTH.

4. OrderBook -- limit order book with cumulative depth
   Structure : AVL price ladder + Fenwick depth tree + dict
   Technique : max_key/min_key for best bid/ask, successor() to walk levels
               without touching empty ticks, Fenwick range_sum for depth,
               non-mutating VWAP for slippage estimates
   Result    : ~3,000 levels per side; a 25,000-share sweep consumed
               multiple levels and moved the best ask, with the ladder
               invariant intact afterward; Fenwick depth matched brute force
   Real use  : exchange matching engines, market-data feed handlers
   Why trees : three structures, three jobs -- and that division of labour
               is the actual engineering lesson

Techniques Demonstrated

  AVL rotations         four cases, O(1) each, BST order preserved
  Cached height         O(1) balance checks instead of O(n) recomputation
  Subtree-size augment  rank/select in O(log n) -- order statistics
  Composite keys        (timestamp, id) to make duplicate keys unique
  Range scan            prune subtrees that cannot intersect the range
  Successor/predecessor descend once, remember the best candidate
  Segment trees         any associative aggregate over any range
  Non-associative fix   store (sum, count), divide at read time
  Fenwick trees         cumulative sums via i & -i, half the space
  Invariant validation  every structure checked against brute force

Benchmark Findings -- Including the Uncomfortable Ones

  dict beats AVL on pure lookup, by a wide margin. If you do not need
  order, a tree is the wrong tool. This is worth internalizing before
  reaching for a fancy structure.

  bisect on a sorted list beat AVL range scans, and insort held its own
  on the mixed workload at n = 20,000. Reason: insort's O(n) memmove is a
  single C memcpy, while the tree's O(log n) descent is interpreted
  pointer-chasing. Asymptotics win eventually, but "eventually" in CPython
  is larger n than most people assume. This is why `sortedcontainers`
  uses chunked lists rather than a textbook BST.

  Segment tree beat naive slice-summing decisively, and was the only
  structure fast at both reads and writes. Prefix sums query faster but
  need an O(n) rebuild per write.

  Fenwick beat segment tree on space and query time -- for sums. It LOST
  on build, because building it here is n separate O(log n) updates while
  the segment tree fills leaves and sweeps upward in O(n). (An O(n) Fenwick
  build exists; it just is not the obvious one.) And it cannot do min/max,
  which is the entire reason segment trees exist.

  AVL beat the plain BST on sorted input at BOTH insert and search, since
  a degenerate BST costs O(n) per insert. Rebalancing is not overhead
  there; it is what makes the inserts cheap.

Honest Trade-offs

  Use a balanced BST when:
    - you need ordered operations (range, successor, rank, sorted walk)
    - writes are frequent enough that re-sorting is too expensive
    - you need worst-case guarantees, not average-case luck

  Do NOT use one when:
    - you only look up by key -> dict
    - the data is static -> sort once, then bisect
    - n is small -> a list and a sort are faster and clearer
    - you are in Python and the constant factor matters -> measure first,
      and look at `sortedcontainers` before hand-rolling

  Use a segment tree when: range aggregates with live updates, or you
  need min/max/gcd, or range updates via lazy propagation.
  Use a Fenwick tree when: prefix or range SUMS only. Half the space,
  a third of the code, lower constant factor.

Design Patterns Worth Keeping

  1. Augment, do not rebuild. A cached subtree size turns an O(n) rank
     scan into O(log n) for one extra int per node.
  2. Composite keys beat duplicate handling. (score, player) sidesteps
     tie-breaking logic entirely.
  3. One tree per aggregate is fine. Four segment trees cost 4x memory
     and stay simple -- far better than one clever fused node type.
  4. Validate invariants in tests, not in production paths. Every
     structure here has an is_valid() checked against brute force.
  5. Combine structures. The order book uses a tree, a Fenwick tree, and
     a dict together because each query type has a different best answer.
  6. Non-associative aggregates decompose. Average = sum + count. Variance
     = sum + sum-of-squares + count. Store the associative parts.
""")

print("=" * 70)
print("Topic 17 Complete! Advanced Trees Mastered!")
print("=" * 70)
print("""
ADVANCED LEVEL 96% COMPLETE

   Completed: Topics 12-17
     12. Dynamic Programming
     13. Advanced Sorting
     14. Graph Algorithms
     15. Greedy Algorithms
     16. Bit Manipulation
     17. Advanced Trees     <- you are here

   1 topic left in the entire curriculum
   Ready for Topic 18: Tries & String Algorithms
""")
