import type React from "react";
import { DIFF_BG, DIFF_TEXT, pct } from "../lib/format";
import type { Difficulty, ProblemState, Verdict } from "../lib/types";

/* ------------------------------------------------------------------ badges */

const DIFF_STYLE: Record<Difficulty, string> = {
  Easy: "bg-mint-500/12 text-mint-400 ring-1 ring-mint-500/25",
  Medium: "bg-amber-500/12 text-amber-400 ring-1 ring-amber-500/25",
  Hard: "bg-rose-500/12 text-rose-400 ring-1 ring-rose-500/25",
  Challenge: "bg-volt-500/15 text-volt-300 ring-1 ring-volt-500/30",
};

export function DifficultyBadge({ value }: { value: Difficulty }) {
  return <span className={`chip ${DIFF_STYLE[value] ?? DIFF_STYLE.Easy}`}>{value}</span>;
}

/** Difficulty as bare coloured text — for dense table rows. */
export function DifficultyText({ value }: { value: Difficulty }) {
  return (
    <span className={`text-[12px] font-semibold ${DIFF_TEXT[value] ?? ""}`}>
      {value}
    </span>
  );
}

export const VERDICT_META: Record<Verdict, { label: string; tone: string; icon: string }> = {
  accepted: { label: "Accepted", tone: "text-mint-400", icon: "✓" },
  failed:   { label: "Wrong Answer", tone: "text-rose-400", icon: "✕" },
  stub:     { label: "Not Attempted", tone: "text-mist-400", icon: "○" },
  error:    { label: "Runtime Error", tone: "text-amber-400", icon: "!" },
  missing:  { label: "Function Missing", tone: "text-amber-400", icon: "?" },
  untested: { label: "No Reference Tests", tone: "text-sky-400", icon: "i" },
  ran:      { label: "Executed", tone: "text-sky-400", icon: "▸" },
};

export function VerdictPill({ verdict }: { verdict: Verdict }) {
  const m = VERDICT_META[verdict] ?? VERDICT_META.ran;
  const bg =
    verdict === "accepted" ? "bg-mint-500/10 ring-mint-500/25"
    : verdict === "failed" ? "bg-rose-500/10 ring-rose-500/25"
    : verdict === "error" || verdict === "missing" ? "bg-amber-500/10 ring-amber-500/25"
    : "bg-ink-750 ring-white/10";
  return (
    <span className={`chip ring-1 ${bg} ${m.tone}`}>
      <span className="text-[10px]">{m.icon}</span>{m.label}
    </span>
  );
}

/** Solved / attempted / todo, as the leading column of a problem row. */
export function StateMark({ state }: { state: ProblemState }) {
  if (state === "solved")
    return (
      <span title="Solved" className="grid h-5 w-5 place-items-center rounded-full bg-mint-500/15 text-mint-400">
        <Icon name="check" className="h-3 w-3" />
      </span>
    );
  if (state === "attempted")
    return (
      <span title="Attempted" className="grid h-5 w-5 place-items-center rounded-full bg-amber-500/15">
        <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
      </span>
    );
  return (
    <span title="Not started" className="grid h-5 w-5 place-items-center rounded-full ring-1 ring-inset ring-white/[.08]">
      <span className="h-1.5 w-1.5 rounded-full bg-ink-600" />
    </span>
  );
}

/* ------------------------------------------------------------------- icons */

export function Icon({ name, className = "w-4 h-4" }: { name: string; className?: string }) {
  const paths: Record<string, React.ReactElement> = {
    play: <path d="M8 5.14v14l11-7-11-7z" />,
    check: <path d="M20 6 9 17l-5-5" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    x: <path d="M18 6 6 18M6 6l12 12" strokeWidth="2.5" fill="none" strokeLinecap="round" />,
    search: <><circle cx="11" cy="11" r="7" strokeWidth="2" fill="none" /><path d="m20 20-3.5-3.5" strokeWidth="2" strokeLinecap="round" /></>,
    reset: <path d="M3 12a9 9 0 1 0 3-6.7M3 4v5h5" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    chevron: <path d="m6 9 6 6 6-6" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    list: <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" strokeWidth="2" fill="none" strokeLinecap="round" />,
    spark: <path d="M12 2 9.6 8.6 3 11l6.6 2.4L12 20l2.4-6.6L21 11l-6.6-2.4z" />,
    clock: <><circle cx="12" cy="12" r="9" strokeWidth="2" fill="none" /><path d="M12 7v5l3 2" strokeWidth="2" fill="none" strokeLinecap="round" /></>,
    flask: <path d="M9 3h6v5l4.5 9A2 2 0 0 1 17.7 20H6.3a2 2 0 0 1-1.8-3L9 8V3z" strokeWidth="1.8" fill="none" strokeLinejoin="round" />,
    doc: <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5z" strokeWidth="1.8" fill="none" strokeLinejoin="round" />,
    home: <path d="M3 10.5 12 3l9 7.5M5.5 9.5V20h13V9.5" strokeWidth="1.8" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    grid: <><rect x="3" y="3" width="7.5" height="7.5" rx="2" strokeWidth="1.8" fill="none" /><rect x="13.5" y="3" width="7.5" height="7.5" rx="2" strokeWidth="1.8" fill="none" /><rect x="3" y="13.5" width="7.5" height="7.5" rx="2" strokeWidth="1.8" fill="none" /><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2" strokeWidth="1.8" fill="none" /></>,
    chart: <path d="M4 20V10m6 10V4m6 16v-7m4 7H3" strokeWidth="2" fill="none" strokeLinecap="round" />,
    star: <path d="m12 3.5 2.6 5.5 6 .8-4.4 4.2 1.1 6L12 17.2 6.7 20l1.1-6L3.4 9.8l6-.8z" strokeWidth="1.6" strokeLinejoin="round" />,
    starOutline: <path d="m12 3.5 2.6 5.5 6 .8-4.4 4.2 1.1 6L12 17.2 6.7 20l1.1-6L3.4 9.8l6-.8z" strokeWidth="1.6" fill="none" strokeLinejoin="round" />,
    dice: <><rect x="3.5" y="3.5" width="17" height="17" rx="4" strokeWidth="1.8" fill="none" /><circle cx="8.5" cy="8.5" r="1.4" /><circle cx="15.5" cy="15.5" r="1.4" /><circle cx="12" cy="12" r="1.4" /></>,
    flame: <path d="M12 2.5c3.5 4 6 6.2 6 10a6 6 0 0 1-12 0c0-2 .8-3.4 2-4.6.2 1.6 1 2.6 2.2 2.6 1.4 0 2.2-1.2 2-3.2-.2-1.8-.5-3.4-.2-4.8z" strokeWidth="1.6" fill="none" strokeLinejoin="round" />,
    arrowLeft: <path d="M19 12H5m0 0 6-6m-6 6 6 6" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    arrowRight: <path d="M5 12h14m0 0-6-6m6 6-6 6" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    note: <path d="M5 4.5h14v10l-4.5 5H5zM14.5 19.5v-5h4.5" strokeWidth="1.8" fill="none" strokeLinejoin="round" />,
    history: <><path d="M3.5 12a8.5 8.5 0 1 0 2.9-6.4M3.5 4v5h5" strokeWidth="1.8" fill="none" strokeLinecap="round" strokeLinejoin="round" /><path d="M12 8v4.5l3 1.8" strokeWidth="1.8" fill="none" strokeLinecap="round" /></>,
    code: <path d="m9 8-4 4 4 4m6-8 4 4-4 4" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
    book: <path d="M4 4.5h6a2.5 2.5 0 0 1 2 2.2 2.5 2.5 0 0 1 2-2.2h6v13h-6a2.5 2.5 0 0 0-2 2 2.5 2.5 0 0 0-2-2H4z" strokeWidth="1.7" fill="none" strokeLinejoin="round" />,
    copy: <><rect x="9" y="9" width="11" height="11" rx="2.5" strokeWidth="1.8" fill="none" /><path d="M15 5.5A2.5 2.5 0 0 0 12.5 3H6.5A2.5 2.5 0 0 0 4 5.5v6A2.5 2.5 0 0 0 6.5 14" strokeWidth="1.8" fill="none" strokeLinecap="round" /></>,
    trophy: <path d="M8 4h8v4a4 4 0 0 1-8 0zM8 5H5v1.5A3.5 3.5 0 0 0 8 10M16 5h3v1.5A3.5 3.5 0 0 1 16 10M12 12v4m-3.5 4h7" strokeWidth="1.8" fill="none" strokeLinecap="round" strokeLinejoin="round" />,
  };
  return (
    <svg viewBox="0 0 24 24" className={className} fill="currentColor" stroke="currentColor" aria-hidden>
      {paths[name] ?? null}
    </svg>
  );
}

/* ------------------------------------------------------------------ layout */

export function Segmented<T extends string>({
  value, options, onChange,
}: { value: T; options: { id: T; label: string; badge?: number }[]; onChange: (v: T) => void }) {
  return (
    <div className="inline-flex rounded-lg bg-ink-850 p-0.5 ring-1 ring-white/[.06]">
      {options.map((o) => (
        <button
          key={o.id}
          onClick={() => onChange(o.id)}
          className={`flex items-center gap-1.5 rounded-[7px] px-3 py-1.5 text-xs font-semibold transition-all ${
            value === o.id
              ? "bg-ink-700 text-white shadow-sm"
              : "text-mist-400 hover:text-mist-200"
          }`}
        >
          {o.label}
          {o.badge !== undefined && o.badge > 0 && (
            <span className="rounded-full bg-white/[.08] px-1.5 font-mono text-[10px]">
              {o.badge}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}

export function Spinner({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <svg className={`${className} animate-spin`} viewBox="0 0 24 24" fill="none" aria-hidden>
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" className="opacity-20" />
      <path d="M22 12a10 10 0 0 0-10-10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

export function Empty({ icon, title, hint, action }: {
  icon: string; title: string; hint?: string; action?: React.ReactNode;
}) {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-3 px-8 py-12 text-center">
      <div className="grid h-12 w-12 place-items-center rounded-xl bg-ink-800 ring-1 ring-white/[.06]">
        <Icon name={icon} className="h-5 w-5 text-mist-400" />
      </div>
      <p className="text-sm font-semibold text-mist-200">{title}</p>
      {hint && <p className="max-w-xs text-xs leading-relaxed text-mist-400">{hint}</p>}
      {action}
    </div>
  );
}

/* ---------------------------------------------------------------- progress */

export function Bar({ value, total, tone = "bg-volt-500", className = "h-1.5" }: {
  value: number; total: number; tone?: string; className?: string;
}) {
  return (
    <div className={`w-full overflow-hidden rounded-full bg-ink-750 ${className}`}>
      <div className={`h-full rounded-full ${tone} transition-all duration-700`}
           style={{ width: `${pct(value, total)}%` }} />
    </div>
  );
}

/**
 * A stacked difficulty bar: solved / attempted / remaining in one track.
 *
 * One bar per difficulty would take four rows; stacking keeps the whole picture
 * on a single line, which is what makes it glanceable on the dashboard.
 */
export function StackedBar({ segments, total }: {
  segments: { value: number; tone: string; label: string }[]; total: number;
}) {
  return (
    <div className="flex h-2 w-full overflow-hidden rounded-full bg-ink-800">
      {segments.map((s) => (
        <div key={s.label} title={`${s.label}: ${s.value}`} className={`${s.tone} transition-all duration-700`}
             style={{ width: `${pct(s.value, total)}%` }} />
      ))}
    </div>
  );
}

/** The solved-count donut, drawn with a stroked circle rather than a library. */
export function Ring({ solved, total, size = 132 }: {
  solved: number; total: number; size?: number;
}) {
  const stroke = 9;
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const done = total > 0 ? solved / total : 0;
  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none"
                stroke="currentColor" strokeWidth={stroke} className="text-ink-800" />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none"
                stroke="url(#ringGrad)" strokeWidth={stroke} strokeLinecap="round"
                strokeDasharray={circ}
                strokeDashoffset={circ * (1 - done)}
                style={{ transition: "stroke-dashoffset .9s cubic-bezier(.2,.8,.2,1)" }} />
        <defs>
          <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#6d4aff" />
            <stop offset="100%" stopColor="#2ed3a0" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 grid place-content-center text-center">
        <p className="font-mono text-[26px] font-bold leading-none text-white">{solved}</p>
        <p className="mt-1 text-[10.5px] font-medium text-mist-400">of {total} solved</p>
      </div>
    </div>
  );
}

export function StatCard({ icon, label, value, sub, tone = "text-volt-300" }: {
  icon: string; label: string; value: React.ReactNode; sub?: string; tone?: string;
}) {
  return (
    <div className="panel rounded-xl px-4 py-3.5">
      <div className="flex items-center gap-2">
        <Icon name={icon} className={`h-3.5 w-3.5 ${tone}`} />
        <p className="text-[10px] font-bold uppercase tracking-[.13em] text-mist-400">{label}</p>
      </div>
      <p className="mt-2 font-mono text-[22px] font-bold leading-none text-white">{value}</p>
      {sub && <p className="mt-1.5 text-[11px] text-mist-400">{sub}</p>}
    </div>
  );
}

export { DIFF_BG };
