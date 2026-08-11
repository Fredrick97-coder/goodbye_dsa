import { useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../lib/api";
import { useAppData } from "../lib/app-data";
import { pct } from "../lib/format";
import type { Difficulty, ProblemSummary } from "../lib/types";
import { DifficultyText, Icon, StateMark } from "../components/ui";

const DIFFS: Difficulty[] = ["Easy", "Medium", "Hard", "Challenge"];
const STATES = [
  { id: "solved", label: "Solved" },
  { id: "attempted", label: "Attempted" },
  { id: "todo", label: "Todo" },
];

/** Every filter lives in the URL, so a filtered view can be bookmarked. */
function useFilters() {
  const [params, setParams] = useSearchParams();
  const set = (key: string, value: string | null) => {
    const next = new URLSearchParams(params);
    if (value === null || value === "" || next.get(key) === value) next.delete(key);
    else next.set(key, value);
    setParams(next, { replace: true });
  };
  return {
    q: params.get("q") ?? "",
    topic: params.get("topic"),
    difficulty: params.get("difficulty"),
    status: params.get("status"),
    tested: params.get("tested") === "1",
    starred: params.get("starred") === "1",
    set,
    clear: () => setParams(new URLSearchParams(), { replace: true }),
    active: [...params.keys()].length,
  };
}

function Pill({ active, onClick, children, tone = "bg-volt-500" }: {
  active: boolean; onClick: () => void; children: React.ReactNode; tone?: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`chip transition-all ${
        active ? `${tone} text-white`
               : "bg-ink-800 text-mist-400 ring-1 ring-white/[.06] hover:text-mist-200"
      }`}
    >
      {children}
    </button>
  );
}

function Row({ p, onStar }: { p: ProblemSummary; onStar: () => void }) {
  return (
    <div className="group grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-3 border-b
                    border-white/[.035] px-3 py-2 transition-colors hover:bg-white/[.025]
                    sm:grid-cols-[28px_minmax(0,1fr)_130px_92px_58px_54px_36px]">
      <StateMark state={p.status} />

      <div className="min-w-0">
        <Link to={`/problems/${p.id}`}
              className="flex items-baseline gap-2 truncate text-[13px] font-medium text-mist-100
                         transition-colors hover:text-volt-300">
          <span className="font-mono text-[11px] text-mist-400">{p.id}</span>
          <span className="truncate">{p.title}</span>
        </Link>
        <div className="mt-0.5 flex items-center gap-2 sm:hidden">
          <DifficultyText value={p.difficulty} />
          <span className="truncate text-[11px] text-mist-400">{p.topicName}</span>
        </div>
      </div>

      <Link to={`/problems?topic=${p.topic}`}
            className="hidden truncate text-[11.5px] text-mist-400 transition-colors
                       hover:text-mist-200 sm:block">
        {p.topicName}
      </Link>

      <div className="hidden sm:block"><DifficultyText value={p.difficulty} /></div>

      <div className="hidden items-center sm:flex">
        {p.tested ? (
          <span title={`${p.testCount} reference spec${p.testCount === 1 ? "" : "s"}`}
                className="flex items-center gap-1 font-mono text-[11px] text-sky-400/80">
            <Icon name="flask" className="h-3 w-3" />{p.testCount}
          </span>
        ) : (
          <span title="no reference tests — check by hand"
                className="font-mono text-[11px] text-amber-500/70">manual</span>
        )}
      </div>

      <div className="hidden sm:block">
        {p.attempts > 0 && (
          <span title={`${p.attempts} graded submission${p.attempts === 1 ? "" : "s"}`}
                className="font-mono text-[11px] text-mist-400">{p.attempts}&times;</span>
        )}
      </div>

      <button
        onClick={onStar}
        title={p.bookmarked ? "Remove bookmark" : "Bookmark"}
        className={`hidden justify-self-end rounded-md p-1 transition-all sm:block ${
          p.bookmarked ? "text-amber-400"
                       : "text-ink-600 opacity-0 hover:text-mist-200 group-hover:opacity-100"
        }`}
      >
        <Icon name={p.bookmarked ? "star" : "starOutline"} className="h-3.5 w-3.5" />
      </button>
    </div>
  );
}

export default function Problems() {
  const { problems, meta, patch } = useAppData();
  const f = useFilters();

  const filtered = useMemo(() => {
    const needle = f.q.trim().toLowerCase();
    return problems.filter((p) =>
      (!needle
        || p.title.toLowerCase().includes(needle)
        || p.topicName.toLowerCase().includes(needle)
        || p.id.includes(needle)
        || p.targets.some((t) => t.toLowerCase().includes(needle)))
      && (!f.difficulty || p.difficulty === f.difficulty)
      && (!f.topic || p.topic === Number(f.topic))
      && (!f.status || p.status === f.status)
      && (!f.tested || p.tested)
      && (!f.starred || p.bookmarked));
  }, [problems, f.q, f.difficulty, f.topic, f.status, f.tested, f.starred]);

  const solvedHere = filtered.filter((p) => p.status === "solved").length;

  const star = async (p: ProblemSummary) => {
    // Flip immediately, then confirm with the server. A star that waits for a
    // round trip feels broken even when the round trip is 4 ms.
    patch(p.id, { bookmarked: !p.bookmarked });
    try {
      const res = await api.toggleBookmark(p.id);
      patch(p.id, { bookmarked: res.bookmarked });
    } catch {
      patch(p.id, { bookmarked: p.bookmarked });
    }
  };

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl px-5 py-6">
        {/* -------------------------------------------------------- header */}
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-[21px] font-bold tracking-tight text-white">Problem Set</h1>
            <p className="mt-1 text-[12.5px] text-mist-400">
              {filtered.length} shown · {solvedHere} solved
              {f.active > 0 && " · filtered"}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {f.active > 0 && (
              <button onClick={f.clear} className="btn-ghost !py-1.5 text-[12px]">
                <Icon name="x" className="h-3.5 w-3.5" /> Clear filters
              </button>
            )}
          </div>
        </div>

        {/* ------------------------------------------------------- filters */}
        <div className="panel mt-5 space-y-3 rounded-xl px-4 py-3.5">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative min-w-[220px] flex-1">
              <Icon name="search" className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mist-400" />
              <input
                value={f.q}
                onChange={(e) => f.set("q", e.target.value)}
                placeholder="Search title, topic, function name or id…"
                className="w-full rounded-lg border border-white/[.07] bg-ink-950/60 py-2 pl-9 pr-3
                           text-[12.5px] text-mist-100 placeholder:text-mist-400
                           focus:border-volt-500/50 focus:outline-none focus:ring-2 focus:ring-volt-500/20"
              />
            </div>

            <select
              value={f.topic ?? ""}
              onChange={(e) => f.set("topic", e.target.value || null)}
              className="rounded-lg border border-white/[.07] bg-ink-950/60 px-2.5 py-2
                         text-[12px] text-mist-200 focus:border-volt-500/50 focus:outline-none"
            >
              <option value="">All topics</option>
              {meta?.topics.map((t) => (
                <option key={t.topic} value={t.topic}>
                  {String(t.topic).padStart(2, "0")} · {t.name} ({t.problemCount})
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-wrap items-center gap-1.5">
            {DIFFS.map((d) => (
              <Pill key={d} active={f.difficulty === d} onClick={() => f.set("difficulty", d)}>
                {d}
                <span className="opacity-60">{meta?.stats.byDifficulty[d] ?? ""}</span>
              </Pill>
            ))}
            <span className="mx-1 h-4 w-px bg-white/10" />
            {STATES.map((s) => (
              <Pill key={s.id} active={f.status === s.id} onClick={() => f.set("status", s.id)}
                    tone={s.id === "solved" ? "bg-mint-500" : s.id === "attempted" ? "bg-amber-500" : "bg-ink-600"}>
                {s.label}
              </Pill>
            ))}
            <span className="mx-1 h-4 w-px bg-white/10" />
            <Pill active={f.tested} onClick={() => f.set("tested", f.tested ? null : "1")} tone="bg-sky-500">
              <Icon name="flask" className="h-3 w-3" /> auto-graded
            </Pill>
            <Pill active={f.starred} onClick={() => f.set("starred", f.starred ? null : "1")} tone="bg-amber-500">
              <Icon name="star" className="h-3 w-3" /> bookmarked
            </Pill>
          </div>
        </div>

        {/* ---------------------------------------------------------- table */}
        <div className="panel mt-4 overflow-hidden rounded-xl">
          <div className="hidden grid-cols-[28px_minmax(0,1fr)_130px_92px_58px_54px_36px] items-center gap-3
                          border-b border-white/[.06] bg-ink-950/40 px-3 py-2 text-[10px]
                          font-bold uppercase tracking-[.13em] text-mist-400 sm:grid">
            <span />
            <span>Problem</span>
            <span>Topic</span>
            <span>Difficulty</span>
            <span>Tests</span>
            <span>Tries</span>
            <span />
          </div>

          {filtered.length === 0 ? (
            <p className="px-4 py-12 text-center text-[12.5px] text-mist-400">
              Nothing matches those filters.
            </p>
          ) : (
            filtered.map((p) => <Row key={p.id} p={p} onStar={() => void star(p)} />)
          )}
        </div>

        {filtered.length > 0 && (
          <p className="mt-4 text-center text-[11px] text-mist-400">
            {pct(solvedHere, filtered.length)}% of this view solved
          </p>
        )}
      </div>
    </div>
  );
}
