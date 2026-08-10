import { useMemo, useState } from "react";
import type { Difficulty, Meta, ProblemSummary } from "../lib/types";
import { DifficultyBadge, Icon } from "./ui";

const DIFFS: Difficulty[] = ["Easy", "Medium", "Hard", "Challenge"];

export function ProblemList({
  problems, meta, currentId, solved, onPick, onClose,
}: {
  problems: ProblemSummary[];
  meta: Meta | null;
  currentId: string | null;
  solved: Record<string, { at: number; ms: number }>;
  onPick: (id: string) => void;
  onClose: () => void;
}) {
  const [query, setQuery] = useState("");
  const [diff, setDiff] = useState<Difficulty | null>(null);
  const [topic, setTopic] = useState<number | null>(null);
  const [testedOnly, setTestedOnly] = useState(false);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return problems.filter((p) =>
      (!q || p.title.toLowerCase().includes(q)
          || p.topicName.toLowerCase().includes(q)
          || p.targets.some((t) => t.toLowerCase().includes(q))) &&
      (!diff || p.difficulty === diff) &&
      (topic === null || p.topic === topic) &&
      (!testedOnly || p.tested));
  }, [problems, query, diff, topic, testedOnly]);

  const grouped = useMemo(() => {
    const map = new Map<number, ProblemSummary[]>();
    for (const p of filtered) {
      if (!map.has(p.topic)) map.set(p.topic, []);
      map.get(p.topic)!.push(p);
    }
    return [...map.entries()].sort((a, b) => a[0] - b[0]);
  }, [filtered]);

  const solvedCount = Object.keys(solved).length;

  return (
    <aside className="panel flex h-full w-full flex-col rounded-none border-y-0 border-l-0">
      {/* header */}
      <div className="space-y-3 border-b border-white/[.06] px-4 py-3.5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-[13px] font-bold text-white">Problems</h2>
            <p className="mt-0.5 text-[11px] text-mist-400">
              {solvedCount} solved · {problems.length} total
            </p>
          </div>
          <button onClick={onClose} className="btn-ghost !p-1.5 lg:hidden" aria-label="Close list">
            <Icon name="x" className="h-4 w-4" />
          </button>
        </div>

        <div className="relative">
          <Icon name="search" className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mist-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search title or function…"
            className="w-full rounded-lg border border-white/[.07] bg-ink-950/60 py-2 pl-8 pr-3
                       text-[12.5px] text-mist-100 placeholder:text-mist-400
                       focus:border-volt-500/50 focus:outline-none focus:ring-2 focus:ring-volt-500/20"
          />
        </div>

        <div className="flex flex-wrap gap-1.5">
          {DIFFS.map((d) => (
            <button
              key={d}
              onClick={() => setDiff(diff === d ? null : d)}
              className={`chip transition-all ${
                diff === d
                  ? "bg-volt-500 text-white"
                  : "bg-ink-800 text-mist-400 ring-1 ring-white/[.06] hover:text-mist-200"
              }`}
            >
              {d}
              <span className="opacity-60">{meta?.stats.byDifficulty[d] ?? ""}</span>
            </button>
          ))}
          <button
            onClick={() => setTestedOnly(!testedOnly)}
            className={`chip transition-all ${
              testedOnly
                ? "bg-sky-500 text-white"
                : "bg-ink-800 text-mist-400 ring-1 ring-white/[.06] hover:text-mist-200"
            }`}
          >
            <Icon name="flask" className="h-3 w-3" /> auto-graded
          </button>
        </div>

        {meta && (
          <select
            value={topic ?? ""}
            onChange={(e) => setTopic(e.target.value ? Number(e.target.value) : null)}
            className="w-full rounded-lg border border-white/[.07] bg-ink-950/60 px-2.5 py-2
                       text-[12px] text-mist-200 focus:border-volt-500/50 focus:outline-none"
          >
            <option value="">All 22 topics</option>
            {meta.topics.map((t) => (
              <option key={t.topic} value={t.topic}>
                {String(t.topic).padStart(2, "0")} · {t.name} ({t.problemCount})
              </option>
            ))}
          </select>
        )}
      </div>

      {/* list */}
      <div className="scroll-thin flex-1 overflow-y-auto px-2 py-2">
        {grouped.length === 0 && (
          <p className="px-3 py-8 text-center text-xs text-mist-400">
            Nothing matches those filters.
          </p>
        )}

        {grouped.map(([topicNum, items]) => (
          <section key={topicNum} className="mb-3">
            <h3 className="sticky top-0 z-10 bg-ink-900/95 px-2 py-1.5 text-[10px]
                           font-bold uppercase tracking-[.13em] text-mist-400 backdrop-blur">
              {String(topicNum).padStart(2, "0")} · {items[0].topicName}
            </h3>
            <div className="mt-0.5 space-y-0.5">
              {items.map((p) => {
                const active = p.id === currentId;
                const done = Boolean(solved[p.id]);
                return (
                  <button
                    key={p.id}
                    onClick={() => onPick(p.id)}
                    className={`group flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left
                                transition-all ${
                      active
                        ? "bg-volt-500/15 ring-1 ring-volt-500/35"
                        : "hover:bg-white/[.04]"
                    }`}
                  >
                    <span className={`grid h-4 w-4 shrink-0 place-items-center rounded-full text-[9px] font-bold ${
                      done ? "bg-mint-500/20 text-mint-400" : "bg-ink-750 text-mist-400"
                    }`}>
                      {done ? "✓" : p.num}
                    </span>
                    <span className={`flex-1 truncate text-[12.5px] ${
                      active ? "font-semibold text-white" : "text-mist-200"
                    }`}>
                      {p.title}
                    </span>
                    {!p.tested && (
                      <span title="no reference tests" className="h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500/60" />
                    )}
                    <DifficultyBadge value={p.difficulty} />
                  </button>
                );
              })}
            </div>
          </section>
        ))}
      </div>

      <div className="border-t border-white/[.06] px-4 py-2.5">
        <p className="text-[10.5px] leading-relaxed text-mist-400">
          <span className="mr-1 inline-block h-1.5 w-1.5 rounded-full bg-amber-500/60 align-middle" />
          amber dot = no reference tests, so check it by hand
        </p>
      </div>
    </aside>
  );
}
