#!/usr/bin/env python3
"""
drill.py -- mixed, BLIND practice across all 22 topics.

Every problem in exercise.py arrives pre-labelled with its topic, so opening
20_backtracking/exercise.py tells you the answer is backtracking. Interviews
do not do that. Recognising WHICH technique applies is a separate skill from
executing it, and this is the only thing here that trains it.

    python drill.py                    one random problem, topic hidden
    python drill.py -n 5               a five-problem set
    python drill.py -n 5 --timed 20    ...with a 20-minute budget each
    python drill.py --difficulty hard  filter by tier
    python drill.py --topic 19 20      restrict to certain topics
    python drill.py --reveal           show the topic immediately (not blind)
    python drill.py --fresh            prefer problems you have not drawn
    python drill.py --stats            what you have drawn so far
    python drill.py --seed 42          reproducible set

History lives in .drill_history.json next to this file. Delete it to reset.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _harness.catalog import Problem, flat_all                 # noqa: E402
from _harness.loader import topic_dirs                         # noqa: E402

HISTORY = Path(__file__).resolve().parent / ".drill_history.json"
TIERS = ["Easy", "Medium", "Hard", "Challenge"]
WIDTH = 68


def load_history() -> dict:
    if HISTORY.exists():
        try:
            return json.loads(HISTORY.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_history(hist: dict) -> None:
    HISTORY.write_text(json.dumps(hist, indent=1, sort_keys=True))


def rule(ch: str = "=") -> str:
    return ch * WIDTH


def show_problem(p: Problem, index: int, total: int, reveal: bool,
                 budget: int | None) -> None:
    print("\n" + rule())
    header = f"PROBLEM {index}/{total}"
    if budget:
        header += f"   (target: {budget} min)"
    print(header)
    print(rule())
    print(f"\n  {p.title}")
    print(f"  difficulty: {p.difficulty}")
    if reveal:
        print(f"  topic     : {p.topic:02d} {p.topic_name}")
        print(f"  function  : {', '.join(p.unique_targets) or '-'}")
    else:
        print(f"  topic     : ??  (work out which technique applies)")
    print()
    if p.input_desc:
        print(f"  Input  : {p.input_desc}")
    if p.output_desc:
        print(f"  Output : {p.output_desc}")
    if p.example:
        print(f"  Example: {p.example}")
    print()
    print("  Before writing code, say out loud:")
    print("    1. which technique this is, and why")
    print("    2. the complexity you expect")
    print("    3. one edge case that would break a naive attempt")


def reveal_answer(p: Problem, elapsed: float | None,
                  budget: int | None) -> None:
    print("\n  " + rule("-")[2:])
    print(f"  It lives in : {p.topic:02d}_{topic_dirs()[p.topic].name.split('_', 1)[1]}"
          f"/exercise.py")
    print(f"  Topic       : {p.topic:02d} {p.topic_name}")
    print(f"  Function(s) : {', '.join(p.unique_targets) or '-'}")
    print(f"  Check it    : python check.py {p.topic}")
    if elapsed is not None:
        mins = elapsed / 60
        verdict = ""
        if budget:
            verdict = ("  (within budget)" if mins <= budget
                       else f"  (over by {mins - budget:.1f} min)")
        print(f"  Your time   : {mins:.1f} min{verdict}")


def pick(problems: list[Problem], count: int, hist: dict,
         fresh: bool, rng: random.Random) -> list[Problem]:
    pool = list(problems)
    if fresh:
        unseen = [p for p in pool if p.label not in hist]
        # Fill from the unseen pool first, then top up with the rest.
        rng.shuffle(unseen)
        chosen = unseen[:count]
        if len(chosen) < count:
            rest = [p for p in pool if p.label not in {c.label for c in chosen}]
            rng.shuffle(rest)
            chosen += rest[:count - len(chosen)]
        return chosen
    rng.shuffle(pool)
    return pool[:count]


def cmd_stats(problems: list[Problem]) -> int:
    hist = load_history()
    print(rule())
    print("DRILL HISTORY")
    print(rule())
    if not hist:
        print("\n  Nothing drawn yet. Run `python drill.py -n 5` to start.")
        return 0

    by_topic: Counter = Counter()
    by_tier: Counter = Counter()
    total_time = 0.0
    timed = 0
    for p in problems:
        rec = hist.get(p.label)
        if not rec:
            continue
        by_topic[p.topic] += rec.get("count", 1)
        by_tier[p.difficulty] += rec.get("count", 1)
        if rec.get("seconds"):
            total_time += rec["seconds"]
            timed += 1

    drawn = len(hist)
    print(f"\n  problems drawn : {drawn} of {len(problems)}"
          f"  ({drawn / len(problems) * 100:.0f}%)")
    if timed:
        print(f"  average time   : {total_time / timed / 60:.1f} min "
              f"over {timed} timed attempts")

    print(f"\n  by difficulty:")
    for tier in TIERS:
        if by_tier[tier]:
            print(f"    {tier:<10} {by_tier[tier]:>4} draws")

    print(f"\n  by topic:")
    for t in sorted(by_topic):
        name = next((p.topic_name for p in problems if p.topic == t), "")
        print(f"    {t:02d} {name[:28]:<28} {by_topic[t]:>4} draws")

    never = [p for p in problems if p.label not in hist]
    print(f"\n  never drawn    : {len(never)}")
    if never:
        sample = never[:6]
        for p in sample:
            print(f"    {p.label}  [{p.difficulty:<9}] {p.title[:36]}")
        if len(never) > 6:
            print(f"    ... and {len(never) - 6} more")
        print("\n  Use --fresh to prioritise these.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("-n", "--count", type=int, default=1)
    ap.add_argument("--topic", type=int, nargs="*")
    ap.add_argument("--difficulty", type=str)
    ap.add_argument("--timed", type=int, metavar="MIN")
    ap.add_argument("--reveal", action="store_true")
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--seed", type=int)
    ap.add_argument("-h", "--help", action="store_true")
    args = ap.parse_args()

    if args.help:
        print(__doc__)
        return 0

    problems = flat_all()
    if not problems:
        print("no problems found -- are you running this from python/ ?")
        return 2

    if args.stats:
        return cmd_stats(problems)

    # Exclude discussion prompts with no stated Input/Output -- a blind
    # draw on those has nothing to recognise.
    pool = [p for p in problems if p.drillable]
    if args.topic:
        pool = [p for p in pool if p.topic in set(args.topic)]
    if args.difficulty:
        want = args.difficulty.strip().capitalize()
        pool = [p for p in pool if p.difficulty == want]
    if not pool:
        print("no problems match those filters.")
        print(f"  difficulties available: {', '.join(TIERS)}")
        return 2

    rng = random.Random(args.seed)
    hist = load_history()
    chosen = pick(pool, max(1, args.count), hist, args.fresh, rng)

    interactive = sys.stdin.isatty()
    print(rule())
    print(f"MIXED DRILL -- {len(chosen)} problem(s) "
          f"drawn from {len(pool)} candidates")
    if not args.reveal:
        print("Topics are HIDDEN. Naming the technique is half the exercise.")
    if not interactive:
        print("(non-interactive: printing everything, no timing)")
    print(rule())

    session_start = time.time()
    for i, p in enumerate(chosen, 1):
        show_problem(p, i, len(chosen), args.reveal, args.timed)

        elapsed = None
        if interactive:
            start = time.time()
            try:
                input("\n  [Enter] when you have solved it, or to give up... ")
            except (EOFError, KeyboardInterrupt):
                print("\n\n  stopped.")
                break
            elapsed = time.time() - start

        reveal_answer(p, elapsed, args.timed)

        rec = hist.setdefault(p.label, {"count": 0})
        rec["count"] = rec.get("count", 0) + 1
        rec["title"] = p.title
        rec["topic"] = p.topic
        if elapsed is not None:
            rec["seconds"] = round(elapsed, 1)

    save_history(hist)

    print("\n" + rule())
    print("SESSION DONE")
    print(rule())
    if interactive:
        print(f"  wall clock: {(time.time() - session_start) / 60:.1f} min")
    print(f"  history    : {HISTORY.name} ({len(hist)} problems drawn overall)")
    seen_topics = sorted({c.topic for c in chosen})
    print(f"\n  Next: solve the stubs, then run  python check.py "
          f"{' '.join(str(t) for t in seen_topics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
