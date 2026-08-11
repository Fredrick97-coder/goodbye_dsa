import type { Difficulty, ProblemState } from "./types";

/** "3m ago" / "yesterday" / "12 Mar" — short enough for a table cell. */
export function timeAgo(seconds: number): string {
  const diff = Date.now() / 1000 - seconds;
  if (diff < 45) return "just now";
  if (diff < 3600) return `${Math.round(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.round(diff / 3600)}h ago`;
  if (diff < 172800) return "yesterday";
  if (diff < 86400 * 30) return `${Math.round(diff / 86400)}d ago`;
  return new Date(seconds * 1000).toLocaleDateString(undefined,
    { day: "numeric", month: "short" });
}

export function timestamp(seconds: number): string {
  return new Date(seconds * 1000).toLocaleString(undefined, {
    day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
  });
}

export const DIFF_TEXT: Record<Difficulty, string> = {
  Easy: "text-mint-400",
  Medium: "text-amber-400",
  Hard: "text-rose-400",
  Challenge: "text-volt-300",
};

export const DIFF_BG: Record<Difficulty, string> = {
  Easy: "bg-mint-500",
  Medium: "bg-amber-500",
  Hard: "bg-rose-500",
  Challenge: "bg-volt-500",
};

export const STATE_LABEL: Record<ProblemState, string> = {
  solved: "Solved",
  attempted: "Attempted",
  todo: "Todo",
};

export function pct(part: number, whole: number): number {
  return whole > 0 ? Math.round((part / whole) * 100) : 0;
}

/** Local YYYY-MM-DD, matching how the server buckets activity days. */
export function isoDay(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${m}-${day}`;
}
