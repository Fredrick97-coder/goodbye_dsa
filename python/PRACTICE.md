# Practice Tools

Two commands close the two gaps that reading the curriculum cannot.

| Command | Gap it closes |
|---------|---------------|
| `python check.py` | You had **no way to know if your answer was right** |
| `python drill.py` | Every problem here arrives **pre-labelled with its topic** |

---

## 1. `check.py` — get told when you're wrong

```bash
python check.py              # every topic that has tests
python check.py 19           # just topic 19
python check.py 19 20 22     # several
python check.py 20 -v        # also list what passed
python check.py --todo       # progress across all 22 topics
python check.py --coverage   # exactly which problems have tests
```

Solve a stub in any `exercise.py`, run `check.py <topic>`, and you get a
verdict per problem:

| Status | Meaning |
|--------|---------|
| `PASS` | matched on every fixed case **and** every randomized trial |
| `FAIL` | wrong answer — **the failing input is printed** |
| `todo` | still a `pass` stub (not reported as a failure) |
| `ERROR` | raised an exception |
| `gone` | the function or class isn't defined |

The `todo` status matters. With ~394 unimplemented stubs, marking them all
`FAIL` would bury the one problem you actually got wrong.

### What the tests compare against

Never against a copy of the same algorithm. Each spec uses either:

- **the standard library** — `sorted`, `math.comb`, `math.gcd`, `math.isqrt`,
  `pow(a,b,m)`, `itertools.permutations`, `int(s, base)`
- **a brute-force reference** written deliberately differently (interval
  merging by pairwise fusion rather than a sorting sweep; spiral traversal by
  simulated walk rather than shrinking boundaries; TSP by permutations rather
  than bitmask DP)
- **published constants** — 25 primes below 100, 92 solutions to 8-Queens,
  Catalan numbers, 2,598,960 five-card hands

Most specs run **both** fixed edge cases and 150 randomized trials against a
reference, so a solution that only works on the example input will fail.

### Where answers legitimately vary

Some problems have several correct answers. Those specs compare a *property*
instead of the literal output, and say so:

- **longest palindromic substring** → the length, and that it *is* a palindrome
- **N-Queens** → the solution count, and that every board is genuinely valid
- **topological sort** → validated as *a* valid order for that DAG
- **activity selection** → the count of chosen activities
- **Kruskal / Prim** → the total MST weight, not the edge list
- **DFS/BFS traversal** → the reachable set, not the visit order

### Conventions the specs assume

Where a problem is ambiguous, the spec picks one and documents it. If your
solution uses the other convention it will `FAIL` with the input shown — read
the note, then change whichever is wrong.

- **Intervals are half-open**: `[1,2]` and `[2,3]` do **not** overlap
- **`divide`** truncates toward zero (C-style), not Python's floor
- **`two_sum`** in topic 10 returns **1-indexed** positions
- **`quick_select`** returns the k-th **smallest**, 1-indexed
- **linked-list digits** in `add_two_numbers` are least-significant-first
- **`find_middle`** returns the second middle for even-length lists
- **weighted graphs** are `{u: [(v, weight), ...]}`; edge lists are `(u, v, w)`
- **`network_delay_time`** nodes are `1..n`
- **`cheapest_flights_k_stops`**: `k` is *stops*, so `k+1` edges

---

## 2. `drill.py` — practise without being told the answer

```bash
python drill.py                    # 1 random problem, topic HIDDEN
python drill.py -n 5               # a five-problem set
python drill.py -n 5 --timed 20    # ...with a 20-minute target each
python drill.py --difficulty hard  # Easy | Medium | Hard | Challenge
python drill.py --topic 19 20      # restrict to certain topics
python drill.py --fresh            # prefer problems you haven't drawn
python drill.py --reveal           # show the topic up front (not blind)
python drill.py --stats            # what you've drawn, and your times
python drill.py --seed 42          # reproducible set
```

Opening `20_backtracking/exercise.py` tells you the answer is backtracking.
Interviews don't. Recognising *which* technique applies is a separate skill
from executing it, and this is the only thing in the repo that trains it.

Each draw prints the problem statement, hides the topic, and prompts you to
say out loud — before writing code — which technique it is, the complexity you
expect, and one edge case that breaks a naive attempt. Press Enter and it
reveals where the problem lives, plus your elapsed time against the budget.

History is kept in `.drill_history.json`. Delete that file to reset.

---

## Suggested loop

1. `python drill.py -n 3 --timed 25 --fresh`
2. Solve the stubs it names, in the real `exercise.py` files
3. `python check.py <those topics>`
4. Fix whatever failed; re-run until clean
5. Weekly: `python drill.py --stats` and `python check.py --todo`

Do step 1 **without** running any code, out loud, against a clock. That is the
part no file in this repo can do for you.

---

## Coverage — honestly

Run `python check.py --coverage` for the live figure. At the time of writing:

```
264 of 342 problems have automated tests (77%)
20 of 22 topics have specs
```

**Two topics have no tests yet:**

- **05 Queues** — most problems mutate a `Queue` object through a method
  sequence, which needs per-problem scripting rather than a reference call
- **17 Advanced Trees** — AVL rotations, segment trees and Fenwick trees need
  the learner's own node/class objects constructed per problem

Untested problems still appear in `drill.py`; you just have to check those by
hand. Nothing is silently reported as passing.

---

## The tests are themselves tested

```bash
python -m _harness.selftest
```

This installs each spec's own reference *as if it were your solution*. Every
spec must then pass — a spec that fails its own reference is a broken spec,
and would mark **correct** code as wrong, which is worse than having no test.

It has already caught eight real bugs in the specs:

- an expected value copied from a truncated LeetCode example that was no
  longer a valid answer to the shortened input
- two brute-force references that conflated *adjacent* intervals with
  *overlapping* ones, producing 710 and 68 false failures against correct code
- four references that returned a new matrix where the exercise mutates in
  place, so a correct in-place solution looked unimplemented
- generated matrices with **ragged rows**, because `randint` inside a nested
  comprehension is re-evaluated per row and throws `IndexError` inside
  otherwise-correct solutions
- a hardcoded subarray-GCD count that was simply wrong (4 instead of 5)
- a factorisation check whose prime set only covered a fifth of the input range

Run it after editing anything under `_harness/`.

---

## Adding tests for an uncovered problem

Specs live in `_harness/specs/tNN.py` and are plain data:

```python
from ..spec import spec

SPECS = [
    # fixed cases only
    spec(4, "count_digits",
         cases=[((12345,), 5), ((0,), 1), ((-7,), 1)]),

    # cases PLUS 150 randomized trials against a reference
    spec(3, "gcd", ref=math.gcd,
         gen=lambda rng: (rng.randint(1, 5000), rng.randint(1, 5000)),
         cases=[((48, 18), 6)]),
]
```

Useful fields:

| Field | Use |
|-------|-----|
| `cases` | `[(args_tuple, expected), ...]` |
| `ref` + `gen` | compare against a reference over random inputs |
| `norm` | canonicalise **both** sides (order-insensitive compare) |
| `prop` | transform the **actual** only — for "is it valid?" checks |
| `inplace=True` | function mutates `args[0]` and returns `None` |
| `tol` | float comparison tolerance |
| `script` / `ref_script` | drive a class through a method sequence |
| `build` / `build_cases` | construct inputs from the learner's own classes |
| `note` | shown on failure — document any convention you assume |

Two rules:

1. **Make the reference structurally different** from the algorithm being
   taught. A reference that reuses the same idea tests nothing.
2. **Run `python -m _harness.selftest`** afterwards. If your new spec fails
   its own reference, the spec is wrong.
