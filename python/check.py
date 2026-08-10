#!/usr/bin/env python3
"""
check.py -- run your exercise.py solutions against reference tests.

    python check.py              # every topic that has tests
    python check.py 19           # one topic
    python check.py 19 20 22     # several
    python check.py 19 -v        # show the detail for passes too
    python check.py --todo       # what is left to solve, by topic
    python check.py --coverage   # which problems have tests at all

Statuses
    PASS     matched on every case and every randomized trial
    FAIL     produced a wrong answer (the failing input is shown)
    STUB     not implemented yet -- still `pass`
    ERROR    raised an exception
    MISSING  the function or class is not defined in exercise.py

Tests compare against the standard library (math.comb, itertools, sorted,
heapq) or an independent brute-force reference -- never against a copy of
the same algorithm.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _harness.catalog import parse_all                      # noqa: E402
from _harness.loader import topic_dirs, topic_title         # noqa: E402
from _harness.runner import run_topic                       # noqa: E402
from _harness.spec import ERROR, FAIL, MISSING, PASS, STUB  # noqa: E402
from _harness.specs import load_all                         # noqa: E402

MARK = {PASS: "PASS ", FAIL: "FAIL ", STUB: "todo ",
        ERROR: "ERROR", MISSING: "gone "}
ORDER = [FAIL, ERROR, MISSING, PASS, STUB]


def _bar(done: int, total: int, width: int = 28) -> str:
    if total == 0:
        return "[" + " " * width + "]"
    filled = int(done / total * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def cmd_check(topics, verbose: bool) -> int:
    all_specs = load_all()
    dirs = topic_dirs()

    if not topics:
        topics = sorted(all_specs)
    missing_specs = [t for t in topics if t not in all_specs]
    topics = [t for t in topics if t in all_specs]

    grand = {PASS: 0, FAIL: 0, STUB: 0, ERROR: 0, MISSING: 0}
    problems = []

    for t in topics:
        specs = all_specs[t]
        results, err = run_topic(t, specs)
        name = topic_title(dirs[t]) if t in dirs else f"topic {t}"

        print(f"\n{'=' * 66}")
        print(f"Topic {t:02d} -- {name}   ({len(specs)} checks)")
        print("=" * 66)

        if err:
            print(f"  could not import exercise.py: {err}")
            grand[ERROR] += 1
            continue

        counts = {PASS: 0, FAIL: 0, STUB: 0, ERROR: 0, MISSING: 0}
        for r in results:
            counts[r.status] += 1
            grand[r.status] += 1
            if r.status == PASS and not verbose:
                continue
            if r.status == STUB and not verbose:
                continue
            line = f"  [{MARK[r.status]}] {r.num:>2}. {r.target}"
            if r.detail:
                line += f"\n            {r.detail}"
            print(line)
            if r.status in (FAIL, ERROR):
                problems.append((t, r))

        if verbose:
            for r in results:
                if r.status == PASS:
                    print(f"  [{MARK[PASS]}] {r.num:>2}. {r.target}"
                          f"   ({r.checked} checks)")

        solved = counts[PASS]
        total = len(results)
        print(f"\n  {_bar(solved, total)}  {solved}/{total} passing"
              f"   |  todo {counts[STUB]}"
              f"  fail {counts[FAIL]}"
              f"  error {counts[ERROR]}"
              f"  missing {counts[MISSING]}")

    print(f"\n{'=' * 66}")
    print("SUMMARY")
    print("=" * 66)
    total = sum(grand.values())
    print(f"  passing : {grand[PASS]:>4} / {total}")
    print(f"  todo    : {grand[STUB]:>4}   (not implemented yet)")
    print(f"  failing : {grand[FAIL]:>4}")
    print(f"  errors  : {grand[ERROR]:>4}")
    print(f"  missing : {grand[MISSING]:>4}")

    if missing_specs:
        print(f"\n  no tests yet for topic(s): "
              f"{', '.join(f'{t:02d}' for t in missing_specs)}")

    if problems:
        print(f"\n  Fix these first:")
        for t, r in problems[:12]:
            print(f"    topic {t:02d}, problem {r.num}: {r.target}")

    if grand[PASS] == total and total:
        print("\n  Everything with a test is passing. Nice.")
    return 1 if (grand[FAIL] or grand[ERROR]) else 0


def cmd_todo() -> int:
    """What is left to solve, using the exercise files as the source."""
    all_specs = load_all()
    cat = parse_all()
    dirs = topic_dirs()

    print("=" * 66)
    print("REMAINING WORK BY TOPIC")
    print("=" * 66)
    print(f"  {'topic':<32} {'problems':>9} {'tested':>7} {'solved':>7}")
    print("  " + "-" * 60)

    tot_p = tot_t = tot_solved = 0
    for t in sorted(cat):
        probs = cat[t]
        specs = all_specs.get(t, [])

        # Count PROBLEMS, not specs -- one problem can define several
        # functions (topic 22's "GCD AND LCM" is one problem, two targets),
        # so counting specs would report more tests than problems exist.
        tested_nums = {s.num for s in specs}
        solved_nums: set = set()
        if specs:
            results, err = run_topic(t, specs)
            if not err:
                by_num: dict = {}
                for r in results:
                    by_num.setdefault(r.num, []).append(r.status)
                solved_nums = {n for n, sts in by_num.items()
                               if all(s == PASS for s in sts)}

        name = topic_title(dirs[t])[:30]
        print(f"  {t:02d} {name:<29} {len(probs):>9} {len(tested_nums):>7} "
              f"{len(solved_nums):>7}")
        tot_p += len(probs)
        tot_t += len(tested_nums)
        tot_solved += len(solved_nums)

    print("  " + "-" * 60)
    print(f"  {'TOTAL':<32} {tot_p:>9} {tot_t:>7} {tot_solved:>7}")
    print(f"\n  {_bar(tot_solved, tot_p, 40)}  {tot_solved}/{tot_p} problems solved")
    print(f"  {tot_t} of {tot_p} problems have automated tests "
          f"({tot_t / tot_p * 100:.0f}%)")
    print("  'solved' means every function in that problem passes.")
    return 0


def cmd_coverage() -> int:
    """Show exactly which problems have tests, so the gaps are visible."""
    all_specs = load_all()
    cat = parse_all()
    print("=" * 66)
    print("TEST COVERAGE -- which problems have automated checks")
    print("=" * 66)
    for t in sorted(cat):
        tested = {s.num for s in all_specs.get(t, [])}
        probs = cat[t]
        if not probs:
            continue
        marks = "".join("#" if p.num in tested else "." for p in probs)
        print(f"  {t:02d}  {marks:<30} {len(tested)}/{len(probs)}")
    print("\n  '#' has a test, '.' does not.")
    print("  Untested problems still appear in drill.py -- you just have to")
    print("  check those by hand.")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:]]
    verbose = "-v" in args or "--verbose" in args
    args = [a for a in args if a not in ("-v", "--verbose")]

    if "--todo" in args:
        return cmd_todo()
    if "--coverage" in args:
        return cmd_coverage()
    if "-h" in args or "--help" in args:
        print(__doc__)
        return 0

    topics = []
    for a in args:
        try:
            topics.append(int(a))
        except ValueError:
            print(f"unrecognised argument: {a!r}  (try --help)")
            return 2
    return cmd_check(topics, verbose)


if __name__ == "__main__":
    raise SystemExit(main())
