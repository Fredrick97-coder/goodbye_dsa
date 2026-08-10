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
