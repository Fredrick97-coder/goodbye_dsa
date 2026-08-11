"""Specs for Topic 20 -- Backtracking.

Most references here are `itertools`, which makes them trustworthy: the
learner's generator is checked against the stdlib rather than against a
second copy of the same idea.
"""

import itertools
import math

from ..spec import as_set_of_tuples, as_sorted, as_sorted_inner, spec

# ------------------------------------------------------------- references


def _ref_subsets(nums):
    return [list(c) for r in range(len(nums) + 1)
            for c in itertools.combinations(nums, r)]


def _ref_perms(nums):
    return [list(p) for p in itertools.permutations(nums)]


def _ref_combine(n, k):
    return [list(c) for c in itertools.combinations(range(1, n + 1), k)]


def _ref_subsets_dup(nums):
    seen = {tuple(sorted(c)) for r in range(len(nums) + 1)
            for c in itertools.combinations(sorted(nums), r)}
    return [list(t) for t in seen]


def _ref_permute_unique(nums):
    return [list(p) for p in set(itertools.permutations(sorted(nums)))]


def _ref_comb_sum(candidates, target):
    cands = sorted(set(candidates))
    out = set()
    if not cands:
        return []
    limit = target // min(cands) if min(cands) > 0 else 0
    for r in range(1, limit + 1):
        for combo in itertools.combinations_with_replacement(cands, r):
            if sum(combo) == target:
                out.add(tuple(sorted(combo)))
    return [list(t) for t in out]


def _ref_comb_sum2(candidates, target):
    out = set()
    for r in range(1, len(candidates) + 1):
        for combo in itertools.combinations(sorted(candidates), r):
            if sum(combo) == target:
                out.add(tuple(sorted(combo)))
    return [list(t) for t in out]


def _ref_binary_strings(n):
    return ["".join(p) for p in itertools.product("01", repeat=n)]


def _ref_letters(digits):
    keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    if not digits:
        return []
    return ["".join(p) for p in
            itertools.product(*[keypad[d] for d in digits])]


def _ref_parens(n):
    """Filter all bracket strings -- brute force, but obviously correct."""
    out = []
    for bits in itertools.product("()", repeat=2 * n):
        s = "".join(bits)
        depth = 0
        ok = True
        for ch in s:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                ok = False
                break
        if ok and depth == 0:
            out.append(s)
    return out


def _ref_partition_pal(s):
    """Enumerate every cut position set, keep all-palindromic partitions."""
    n = len(s)
    out = []
    for mask in range(1 << max(0, n - 1)):
        parts = []
        start = 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(s[start:i + 1])
                start = i + 1
        parts.append(s[start:])
        if all(p == p[::-1] for p in parts):
            out.append(parts)
    return out


def _ref_restore_ip(s):
    out = []
    n = len(s)
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                d = n - a - b - c
                if d < 1 or d > 3:
                    continue
                segs = [s[:a], s[a:a + b], s[a + b:a + b + c], s[a + b + c:]]
                ok = True
                for seg in segs:
                    if (seg[0] == "0" and len(seg) > 1) or int(seg) > 255:
                        ok = False
                        break
                if ok:
                    out.append(".".join(segs))
    return out


def _ref_word_break_all(s, words):
    wset = set(words)
    memo = {}

    def go(i):
        if i == len(s):
            return [""]
        if i in memo:
            return memo[i]
        res = []
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in wset:
                for rest in go(j):
                    res.append(s[i:j] if not rest else s[i:j] + " " + rest)
        memo[i] = res
        return res

    return go(0)


def _ref_exist(board, word):
    R, C = len(board), len(board[0]) if board else 0

    def go(r, c, i, seen):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or (r, c) in seen:
            return False
        if board[r][c] != word[i]:
            return False
        seen.add((r, c))
        ok = any(go(r + dr, c + dc, i + 1, seen)
                 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        seen.discard((r, c))
        return ok

    return any(go(r, c, 0, set()) for r in range(R) for c in range(C))


def _ref_subset_sum(nums, target):
    """Returns (found, witness) to match the exercise's declared signature."""
    for r in range(len(nums) + 1):
        for combo in itertools.combinations(nums, r):
            if sum(combo) == target:
                return True, list(combo)
    return False, None


def _found_flag(x):
    """Accept either (bool, witness) or a bare bool, and compare the flag."""
    if x is None:
        return None
    if isinstance(x, tuple):
        return bool(x[0])
    return bool(x)


NQUEENS = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}


def _valid_queens(sol):
    """A solution is a list where sol[row] = col."""
    n = len(sol)
    return (sorted(sol) == sorted(set(sol))
            and all(abs(sol[i] - sol[j]) != j - i
                    for i in range(n) for j in range(i + 1, n)))


def _queens_prop(sols):
    """(count, all_valid) -- lets us check the count AND the boards."""
    if sols is None:
        return None
    return (len(sols), all(_valid_queens(s) for s in sols))


def _catalan(n):
    return math.comb(2 * n, n) // (n + 1)


# ------------------------------------------------------------- generators


def g_small_distinct(rng):
    n = rng.randint(0, 7)
    return (rng.sample(range(1, 20), n),)


def g_small_perm(rng):
    n = rng.randint(0, 6)
    return (rng.sample(range(1, 20), n),)


def g_dup_list(rng):
    return ([rng.randint(1, 4) for _ in range(rng.randint(0, 7))],)


def g_dup_small(rng):
    return ([rng.randint(1, 3) for _ in range(rng.randint(0, 6))],)


def g_n_k(rng):
    n = rng.randint(1, 8)
    return (n, rng.randint(1, n))


def g_comb_sum(rng):
    cands = sorted(set(rng.randint(2, 9) for _ in range(rng.randint(1, 5))))
    return (cands, rng.randint(1, 16))


def g_comb_sum2(rng):
    return ([rng.randint(1, 8) for _ in range(rng.randint(1, 7))],
            rng.randint(1, 15))


def g_pal_string(rng):
    return ("".join(rng.choice("ab") for _ in range(rng.randint(1, 8))),)


def g_grid_word(rng):
    R, C = rng.randint(1, 3), rng.randint(1, 3)
    board = [[rng.choice("ab") for _ in range(C)] for _ in range(R)]
    word = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
    return (board, word)


SPECS = [
    spec(1, "subsets", ref=_ref_subsets, gen=g_small_distinct,
         norm=as_set_of_tuples, cases=[
        (([1, 2, 3],), _ref_subsets([1, 2, 3])), (([],), [[]]),
    ]),
    spec(2, "permutations", ref=_ref_perms, gen=g_small_perm,
         norm=as_set_of_tuples, cases=[
        (([1, 2, 3],), _ref_perms([1, 2, 3])), (([],), [[]]),
    ]),
    spec(3, "combine", ref=_ref_combine, gen=g_n_k, norm=as_sorted_inner,
         cases=[((4, 2), _ref_combine(4, 2))]),
    spec(4, "generate_parenthesis", ref=_ref_parens,
         gen=lambda r: (r.randint(0, 6),), norm=as_sorted, cases=[
        ((3,), _ref_parens(3)),
    ]),
    spec(4, "generate_parenthesis", prop=lambda x: None if x is None else len(x),
         cases=[((n,), _catalan(n)) for n in range(0, 8)]),
    spec(5, "letter_combinations", ref=_ref_letters,
         gen=lambda r: ("".join(r.choice("23456789")
                                for _ in range(r.randint(0, 3))),),
         norm=as_sorted, cases=[
        (("23",), _ref_letters("23")), (("",), []),
    ]),
    spec(6, "binary_strings", ref=_ref_binary_strings,
         gen=lambda r: (r.randint(0, 8),), norm=as_sorted,
         cases=[((2,), ["00", "01", "10", "11"])]),
    spec(7, "subsets_with_dup", ref=_ref_subsets_dup, gen=g_dup_list,
         norm=as_sorted_inner, cases=[
        (([1, 2, 2],), _ref_subsets_dup([1, 2, 2])),
    ]),
    spec(8, "permute_unique", ref=_ref_permute_unique, gen=g_dup_small,
         norm=as_set_of_tuples, cases=[
        (([1, 1, 2],), [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
    ]),
    spec(9, "combination_sum", ref=_ref_comb_sum, gen=g_comb_sum,
         norm=as_sorted_inner, cases=[
        (([2, 3, 6, 7], 7), [[2, 2, 3], [7]]),
    ]),
    spec(10, "combination_sum2", ref=_ref_comb_sum2, gen=g_comb_sum2,
         norm=as_sorted_inner, cases=[
        (([10, 1, 2, 7, 6, 1, 5], 8),
         [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
    ]),
    spec(11, "partition_palindromes", ref=_ref_partition_pal, gen=g_pal_string,
         norm=as_set_of_tuples, cases=[
        (("aab",), [["a", "a", "b"], ["aa", "b"]]),
    ]),
    spec(12, "restore_ip_addresses", ref=_ref_restore_ip,
         gen=lambda r: ("".join(r.choice("0125")
                                for _ in range(r.randint(4, 12))),),
         norm=as_sorted, cases=[
        (("25525511135",), ["255.255.11.135", "255.255.111.35"]),
        (("0000",), ["0.0.0.0"]),
    ]),
    spec(13, "exist", ref=_ref_exist, gen=g_grid_word, cases=[
        (([list("ABCE"), list("SFCS"), list("ADEE")], "ABCCED"), True),
        (([list("ABCE"), list("SFCS"), list("ADEE")], "SEE"), True),
        (([list("ABCE"), list("SFCS"), list("ADEE")], "ABCB"), False),
    ]),
    spec(14, "subset_sum", norm=_found_flag, ref=_ref_subset_sum,
         gen=lambda r: ([r.randint(1, 12) for _ in range(r.randint(0, 8))],
                        r.randint(0, 20)),
         cases=[(([3, 34, 4, 12, 5, 2], 9), True),
                (([1, 2], 100), False)],
         note="only the boolean is checked; any valid witness is accepted"),
    spec(15, "solve_n_queens", prop=_queens_prop,
         cases=[((n,), (NQUEENS[n], True)) for n in range(1, 9)]),
    spec(16, "total_n_queens",
         cases=[((n,), NQUEENS[n]) for n in range(1, 10)]),
    spec(17, "solve_sudoku", inplace=True,
         prop=lambda b: None if b is None else all(
             sorted(b[i]) == list("123456789") for i in range(9)) and all(
             sorted(b[r][c] for r in range(9)) == list("123456789")
             for c in range(9)),
         cases=[((
             [list("53..7...."), list("6..195..."), list(".98....6."),
              list("8...6...3"), list("4..8.3..1"), list("7...2...6"),
              list(".6....28."), list("...419..5"), list("....8..79")],
         ), True)]),
    spec(19, "word_break_all", ref=_ref_word_break_all,
         gen=lambda r: ("".join(r.choice("ab") for _ in range(r.randint(1, 8))),
                        ["a", "b", "ab", "ba", "aa"]),
         norm=as_sorted, cases=[
        (("catsanddog", ["cat", "cats", "and", "sand", "dog"]),
         ["cat sand dog", "cats and dog"]),
    ]),
    spec(24, "generate_trees",
         prop=lambda x: None if x is None else len(x),
         cases=[((n,), _catalan(n)) for n in range(1, 8)]),
]


# ---------------------------------------------------------- added coverage

def _ref_find_words(board, words):
    """Brute force per word, which is exactly what the problem improves on."""
    rows, cols = len(board), len(board[0]) if board else 0

    def search(word):
        def walk(r, c, i, seen):
            if i == len(word):
                return True
            if not (0 <= r < rows and 0 <= c < cols):
                return False
            if (r, c) in seen or board[r][c] != word[i]:
                return False
            seen.add((r, c))
            found = any(walk(r + dr, c + dc, i + 1, seen)
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            seen.discard((r, c))
            return found
        return any(walk(r, c, 0, set())
                   for r in range(rows) for c in range(cols))

    return [w for w in words if w and search(w)]


def g_word_board(rng):
    rows, cols = rng.randint(1, 4), rng.randint(1, 4)
    board = [[rng.choice("abc") for _ in range(cols)] for _ in range(rows)]
    words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
             for _ in range(rng.randint(1, 5))]
    return (board, sorted(set(words)))


def _ref_add_operators(num, target):
    out = []

    def walk(i, expr, value, prev):
        if i == len(num):
            if value == target:
                out.append(expr)
            return
        for j in range(i + 1, len(num) + 1):
            part = num[i:j]
            if len(part) > 1 and part[0] == "0":
                break                       # no leading zeros
            n = int(part)
            if i == 0:
                walk(j, part, n, n)
            else:
                walk(j, expr + "+" + part, value + n, n)
                walk(j, expr + "-" + part, value - n, -n)
                walk(j, expr + "*" + part, value - prev + prev * n, prev * n)

    if num:
        walk(0, "", 0, 0)
    return out


def g_add_ops(rng):
    num = "".join(rng.choice("0123") for _ in range(rng.randint(1, 5)))
    return (num, rng.randint(-6, 12))


def _valid_tour(tour):
    """
    Any knight's tour is acceptable, so validate rather than compare.

    The board size is recovered from the tour itself: a full tour visits every
    cell exactly once, so its length is n*n.
    """
    if tour is None:
        return None
    cells = [tuple(c) for c in tour]
    n2 = len(cells)
    n = int(round(n2 ** 0.5))
    if n * n != n2 or len(set(cells)) != n2:
        return False
    if any(not (0 <= r < n and 0 <= c < n) for r, c in cells):
        return False
    moves = {(1, 2), (2, 1), (-1, 2), (-2, 1),
             (1, -2), (2, -1), (-1, -2), (-2, -1)}
    return all((b[0] - a[0], b[1] - a[1]) in moves
               for a, b in zip(cells, cells[1:]))


def _canonical_colouring(colours):
    """
    Relabel colours by first appearance.

    Which colour gets which number is arbitrary, so [0,1,0] and [2,7,2] are the
    same answer. The cases below are chosen so the PARTITION is unique, which
    makes this canonical form comparable.
    """
    if colours is None:
        return None
    mapping = {}
    out = []
    for c in colours:
        if c not in mapping:
            mapping[c] = len(mapping)
        out.append(mapping[c])
    return out


def _ref_knapsack(weights, values, capacity):
    """The Topic 12 DP, used as the reference for the branch-and-bound version."""
    best = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def g_knapsack(rng):
    n = rng.randint(0, 8)
    weights = [rng.randint(1, 10) for _ in range(n)]
    values = [rng.randint(1, 20) for _ in range(n)]
    return (weights, values, rng.randint(0, 20))


SPECS += [
    spec(18, "find_words", ref=_ref_find_words, gen=g_word_board,
         norm=as_sorted,
         cases=[((([["o", "a", "a", "n"], ["e", "t", "a", "e"],
                    ["i", "h", "k", "r"], ["i", "f", "l", "v"]]),
                  ["oath", "pea", "eat", "rain"]), ["oath", "eat"])],
         note="order does not matter; each word may reuse a cell only once "
              "within that word"),

    spec(20, "add_operators", ref=_ref_add_operators, gen=g_add_ops,
         norm=as_sorted,
         cases=[(("123", 6), ["1*2*3", "1+2+3"]),
                (("232", 8), ["2*3+2", "2+3*2"]),
                (("105", 5), ["1*0+5", "10-5"]),
                (("00", 0), ["0*0", "0+0", "0-0"])],
         note="insert +, - or * between digits with no spaces; multi-digit "
              "numbers may not have a leading zero. Order does not matter"),

    spec(21, "knights_tour", prop=_valid_tour,
         cases=[((1,), True), ((5,), True), ((3,), None), ((4,), None)],
         note="ANY valid tour is accepted -- the check is that every square is "
              "visited exactly once by legal knight moves. Return None when no "
              "tour exists (3x3 and 4x4 have none)"),

    spec(25, "knapsack_branch_and_bound", ref=_ref_knapsack, gen=g_knapsack,
         cases=[(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9),
                (([], [], 10), 0)],
         note="returns the optimal VALUE; branch and bound must reach the "
              "same answer as the DP, just by exploring fewer nodes"),
]

# One spec per graph, so the property check can see its own input -- the same
# idiom the topological-sort specs use.
_COLOUR_CASES = [
    ([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 3, [0, 1, 2]),      # K3, 3 colours
    ([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 2, None),           # K3, impossible
    ([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], 2,
     [0, 1, 0, 1]),                                         # path, 2 colours
    ([[0, 0], [0, 0]], 1, [0, 0]),                          # no edges
]

SPECS += [
    spec(22, "graph_colouring", norm=_canonical_colouring,
         cases=[((_graph, _m), _expected)],
         note="colour numbering is arbitrary, so the answer is compared after "
              "relabelling by first appearance. Return None when the graph is "
              "not m-colourable")
    for _graph, _m, _expected in _COLOUR_CASES
]


def _cryptarithm_ok(words, result):
    """
    Validate a returned letter->digit mapping against the puzzle.

    Closing over the puzzle is the only way to check this: the mapping alone
    says nothing about whether the sum works out.
    """
    def check(mapping):
        if mapping is None:
            return False
        letters = {ch for w in words + [result] for ch in w}
        if set(mapping) != letters:
            return False
        digits = [mapping[ch] for ch in letters]
        if len(set(digits)) != len(digits) or any(d < 0 or d > 9 for d in digits):
            return False
        if any(mapping[w[0]] == 0 for w in words + [result] if len(w) > 1):
            return False

        def value(word):
            return int("".join(str(mapping[ch]) for ch in word))

        return sum(value(w) for w in words) == value(result)
    return check


_CRYPT_CASES = [
    (["SEND", "MORE"], "MONEY", True),
    (["TO", "GO"], "OUT", True),
    # A + A = B is solvable (1 + 1 = 2); A = B is NOT, because the letters must
    # take distinct digits. An earlier version expected the latter to succeed.
    (["A", "A"], "B", True),
    (["AB", "AB"], "AAA", None),        # unsatisfiable
]

SPECS += [
    spec(23, "solve_cryptarithm",
         prop=(lambda w, r: lambda m: _cryptarithm_ok(w, r)(m)
               if m is not None else None)(_words, _result),
         cases=[((_words, _result), _expected)],
         note="return a letter -> digit dict, or None when unsolvable. Any "
              "valid assignment is accepted: distinct digits, and no leading "
              "zero on a multi-letter word")
    for _words, _result, _expected in _CRYPT_CASES
]
