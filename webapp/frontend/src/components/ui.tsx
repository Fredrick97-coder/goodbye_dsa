import type React from "react";
import type { Difficulty, Verdict } from "../lib/types";

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

export const VERDICT_META: Record<Verdict, { label: string; tone: string; icon: string }> = {
  accepted: { label: "Accepted", tone: "text-mint-400", icon: "✓" },
  failed:   { label: "Wrong Answer", tone: "text-rose-400", icon: "✕" },
  stub:     { label: "Not Attempted", tone: "text-mist-400", icon: "○" },
  error:    { label: "Runtime Error", tone: "text-amber-400", icon: "!" },
  missing:  { label: "Function Missing", tone: "text-amber-400", icon: "?" },
  untested: { label: "No Reference Tests", tone: "text-sky-400", icon: "i" },
  ran:      { label: "Executed", tone: "text-sky-400", icon: "▸" },
};

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
}: { value: T; options: { id: T; label: string }[]; onChange: (v: T) => void }) {
  return (
    <div className="inline-flex rounded-lg bg-ink-850 p-0.5 ring-1 ring-white/[.06]">
      {options.map((o) => (
        <button
          key={o.id}
          onClick={() => onChange(o.id)}
          className={`rounded-[7px] px-3 py-1.5 text-xs font-semibold transition-all ${
            value === o.id
              ? "bg-ink-700 text-white shadow-sm"
              : "text-mist-400 hover:text-mist-200"
          }`}
        >
          {o.label}
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

export function Empty({ icon, title, hint }: { icon: string; title: string; hint?: string }) {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-3 px-8 text-center">
      <div className="grid h-12 w-12 place-items-center rounded-xl bg-ink-800 ring-1 ring-white/[.06]">
        <Icon name={icon} className="h-5 w-5 text-mist-400" />
      </div>
      <p className="text-sm font-semibold text-mist-200">{title}</p>
      {hint && <p className="max-w-xs text-xs leading-relaxed text-mist-400">{hint}</p>}
    </div>
  );
}
