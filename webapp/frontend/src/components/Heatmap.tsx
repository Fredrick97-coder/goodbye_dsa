import { useMemo } from "react";
import { isoDay } from "../lib/format";
import type { ActivityDay } from "../lib/types";

const DAY_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""];

/** Four buckets is enough to read intensity; more just looks noisy. */
function tone(count: number): string {
  if (count === 0) return "bg-ink-800/70";
  if (count < 3) return "bg-volt-600/45";
  if (count < 7) return "bg-volt-500/70";
  if (count < 15) return "bg-volt-400";
  return "bg-mint-400";
}

/**
 * A GitHub-style contribution grid, built from the server's daily buckets.
 *
 * The grid is generated from today backwards rather than from the first
 * submission, so an empty week still shows as empty rather than collapsing --
 * a gap you can see is the entire point of the chart.
 */
export function Heatmap({ days, weeks = 26 }: { days: ActivityDay[]; weeks?: number }) {
  const { columns, months } = useMemo(() => {
    const index = new Map(days.map((d) => [d.date, d]));

    const today = new Date();
    today.setHours(12, 0, 0, 0);       // midday avoids DST edge cases
    const end = new Date(today);
    end.setDate(end.getDate() + (6 - end.getDay()));   // end of this week

    const cols: { date: Date; key: string; day: ActivityDay | undefined }[][] = [];
    const monthMarks: { col: number; label: string }[] = [];
    const cursor = new Date(end);
    cursor.setDate(cursor.getDate() - (weeks * 7 - 1));

    for (let w = 0; w < weeks; w++) {
      const col: typeof cols[number] = [];
      for (let d = 0; d < 7; d++) {
        const date = new Date(cursor);
        const key = isoDay(date);
        col.push({ date, key, day: index.get(key) });
        cursor.setDate(cursor.getDate() + 1);
      }
      // Label the week that contains the 1st, using the month of THAT day.
      // Taking the month of the column's Sunday instead reports the previous
      // month whenever a month starts mid-week -- which is most months.
      const firstOfMonth = col.find((c) => c.date.getDate() === 1);
      if (firstOfMonth) {
        monthMarks.push({
          col: w,
          label: firstOfMonth.date.toLocaleDateString(undefined, { month: "short" }),
        });
      }
      cols.push(col);
    }
    return { columns: cols, months: monthMarks };
  }, [days, weeks]);

  const todayKey = isoDay(new Date());

  return (
    <div className="scroll-thin overflow-x-auto">
      <div className="inline-block min-w-full">
        <div className="flex gap-[3px] pl-[34px] text-[9.5px] text-mist-400">
          {columns.map((_, i) => {
            const mark = months.find((m) => m.col === i);
            return (
              <span key={i} className="w-[13px] shrink-0">
                {mark ? mark.label : ""}
              </span>
            );
          })}
        </div>

        <div className="mt-1 flex gap-[3px]">
          <div className="flex w-[31px] shrink-0 flex-col gap-[3px] pr-1 text-right text-[9.5px] text-mist-400">
            {DAY_LABELS.map((l, i) => (
              <span key={i} className="h-[13px] leading-[13px]">{l}</span>
            ))}
          </div>
          {columns.map((col, w) => (
            <div key={w} className="flex flex-col gap-[3px]">
              {col.map((cell) => {
                const future = cell.key > todayKey;
                const n = cell.day?.submissions ?? 0;
                return (
                  <div
                    key={cell.key}
                    title={future ? "" : `${cell.key}: ${n} submission${n === 1 ? "" : "s"}` +
                      (cell.day?.solved ? `, ${cell.day.solved} solved` : "")}
                    className={`h-[13px] w-[13px] rounded-[3px] ${
                      future ? "bg-transparent"
                             : `${tone(n)} ${cell.key === todayKey ? "ring-1 ring-volt-400/70" : ""}`
                    }`}
                  />
                );
              })}
            </div>
          ))}
        </div>

        <div className="mt-3 flex items-center gap-2 pl-[34px] text-[10px] text-mist-400">
          <span>less</span>
          {[0, 2, 5, 10, 20].map((n) => (
            <span key={n} className={`h-[11px] w-[11px] rounded-[3px] ${tone(n)}`} />
          ))}
          <span>more</span>
        </div>
      </div>
    </div>
  );
}
