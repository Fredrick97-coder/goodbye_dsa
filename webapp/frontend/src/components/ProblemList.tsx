import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useAppData } from "../lib/app-data";
import type { Difficulty } from "../lib/types";
import { DifficultyBadge, Icon, StateMark } from "./ui";

const DIFFS: Difficulty[] = ["Easy", "Medium", "Hard", "Challenge"];

/**
 * The in-solver problem switcher.
 *
 * Deliberately lighter than the Problem Set page: while solving, the job is to
 * hop to the next problem in a couple of clicks, not to slice the catalogue.
 */
export function ProblemList({ currentId, onClose }: {
  currentId: string | null; onClose: () => void;
}) {
  const { problems, meta } = useAppData();
  const [query, setQuery] = useState("");
  const [diff, setDiff] = useState<Difficulty | null>(null);
  const [topic, setTopic] = useState<number | null>(
    // Open on the current problem's topic: that is where the next one to solve
    // almost always is.
    currentId ? Number(currentId.slice(0, 2)) : null,
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return problems.filter((p) =>
      (!q || p.title.toLowerCase().includes(q)
          || p.topicName.toLowerCase().includes(q)
          || p.targets.some((t) => t.toLowerCase().includes(q)))
      && (!diff || p.difficulty === diff)
      && (topic === null || p.topic === topic));
  }, [problems, query, diff, topic]);

  const grouped = useMemo(() => {
    const map = new Map<number, typeof filtered>();
    for (const p of filtered) {
      if (!map.has(p.topic)) map.set(p.topic, []);
      map.get(p.topic)!.push(p);
    }
    return [...map.entries()].sort((a, b) => a[0] - b[0]);
  }, [filtered]);

  return (
    <aside className="flex h-full w-full flex-col bg-ink-900/70">
      <div className="space-y-2.5 border-b border-white/[.06] px-3.5 py-3">
        <div className="flex items-center justify-between">
          <h2 className="text-[12px] font-bold text-white">Switch problem</h2>
          <div className="flex items-center gap-1">
            <Link to="/problems" className="btn-ghost !px-1.5 !py-1 text-[11px]" title="Open the full problem set">
              <Icon name="grid" className="h-3.5 w-3.5" />
            </Link>
            <button onClick={onClose} className="btn-ghost !p-1.5" aria-label="Close list">
              <Icon name="x" className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        <div className="relative">
          <Icon name="search" className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mist-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search…"
            className="w-full rounded-lg border border-white/[.07] bg-ink-950/60 py-1.5 pl-8 pr-2.5
                       text-[12px] text-mist-100 placeholder:text-mist-400
                       focus:border-volt-500/50 focus:outline-none"
          />
        </div>

        <div className="flex flex-wrap gap-1">
          {DIFFS.map((d) => (
            <button key={d} onClick={() => setDiff(diff === d ? null : d)}
                    className={`chip !px-2 !text-[10px] transition-all ${
                      diff === d ? "bg-volt-500 text-white"
                                 : "bg-ink-800 text-mist-400 ring-1 ring-white/[.06]"}`}>
              {d}
            </button>
          ))}
        </div>

        <select
          value={topic ?? ""}
          onChange={(e) => setTopic(e.target.value ? Number(e.target.value) : null)}
          className="w-full rounded-lg border border-white/[.07] bg-ink-950/60 px-2 py-1.5
                     text-[11.5px] text-mist-200 focus:border-volt-500/50 focus:outline-none"
        >
          <option value="">All {meta?.topics.length ?? 22} topics</option>
          {meta?.topics.map((t) => (
            <option key={t.topic} value={t.topic}>
              {String(t.topic).padStart(2, "0")} · {t.name}
            </option>
          ))}
        </select>
      </div>

      <div className="scroll-thin flex-1 overflow-y-auto px-1.5 py-2">
        {grouped.length === 0 && (
          <p className="px-3 py-8 text-center text-[11.5px] text-mist-400">Nothing matches.</p>
        )}
        {grouped.map(([topicNum, items]) => (
          <section key={topicNum} className="mb-2.5">
            <h3 className="sticky top-0 z-10 bg-ink-900/95 px-2 py-1.5 text-[9.5px]
                           font-bold uppercase tracking-[.13em] text-mist-400 backdrop-blur">
              {String(topicNum).padStart(2, "0")} · {items[0].topicName}
            </h3>
            <div className="mt-0.5 space-y-0.5">
              {items.map((p) => (
                <Link
                  key={p.id}
                  to={`/problems/${p.id}`}
                  className={`flex w-full items-center gap-2 rounded-lg px-2 py-1.5 transition-all ${
                    p.id === currentId ? "bg-volt-500/15 ring-1 ring-volt-500/35"
                                       : "hover:bg-white/[.04]"}`}
                >
                  <StateMark state={p.status} />
                  <span className={`flex-1 truncate text-[12px] ${
                    p.id === currentId ? "font-semibold text-white" : "text-mist-200"}`}>
                    {p.title}
                  </span>
                  {!p.tested && (
                    <span title="no reference tests" className="h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500/60" />
                  )}
                  <DifficultyBadge value={p.difficulty} />
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>

      <div className="border-t border-white/[.06] px-3.5 py-2">
        <p className="text-[10px] leading-relaxed text-mist-400">
          <span className="mr-1 inline-block h-1.5 w-1.5 rounded-full bg-amber-500/60 align-middle" />
          amber dot = no reference tests, so check it by hand
        </p>
      </div>
    </aside>
  );
}
