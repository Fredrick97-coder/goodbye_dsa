import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import { timeAgo, timestamp } from "../lib/format";
import type { Submission } from "../lib/types";
import { Empty, Icon, Spinner, VerdictPill } from "./ui";

/** Read-only view of one past attempt, with a way to bring it back. */
function CodeSheet({ sub, onClose, onRestore }: {
  sub: Submission; onClose: () => void; onRestore: (source: string) => void;
}) {
  return (
    <div className="absolute inset-0 z-20 flex flex-col bg-ink-900">
      <div className="flex h-11 shrink-0 items-center gap-3 border-b border-white/[.06] px-4">
        <button onClick={onClose} className="btn-ghost !px-2 !py-1">
          <Icon name="arrowLeft" className="h-3.5 w-3.5" />
        </button>
        <VerdictPill verdict={sub.verdict} />
        <span className="font-mono text-[11px] text-mist-400">
          {sub.passed}/{sub.total} · {Math.round(sub.elapsedMs)} ms
        </span>
        <span className="ml-auto text-[11px] text-mist-400">{timestamp(sub.createdAt)}</span>
        <button onClick={() => onRestore(sub.source ?? "")} className="btn-outline !py-1 text-[11.5px]">
          <Icon name="reset" className="h-3.5 w-3.5" /> Load into editor
        </button>
      </div>
      <pre className="scroll-thin flex-1 overflow-auto px-4 py-3 font-mono text-[12px]
                      leading-relaxed text-mist-200">
{sub.source}
      </pre>
    </div>
  );
}

export function SubmissionsTab({
  problemId, reloadKey, onRestore,
}: { problemId: string; reloadKey: number; onRestore: (source: string) => void }) {
  const [rows, setRows] = useState<Submission[] | null>(null);
  const [open, setOpen] = useState<Submission | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setRows(await api.submissions(problemId, 100));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }, [problemId]);

  // reloadKey bumps after every graded submit, so the list is never stale.
  useEffect(() => { setRows(null); setOpen(null); void load(); }, [load, reloadKey]);

  const openOne = async (row: Submission) => {
    // The list endpoint deliberately omits source -- fetch the code on demand
    // so opening the tab does not pull every past solution over the wire.
    try { setOpen(await api.submission(row.id)); }
    catch (err) { setError(err instanceof Error ? err.message : String(err)); }
  };

  if (error)
    return (
      <div className="p-5">
        <p className="rounded-xl border border-rose-500/25 bg-rose-500/[.07] px-4 py-3
                      text-[12px] text-rose-300">{error}</p>
      </div>
    );

  if (rows === null)
    return <div className="grid h-full place-items-center"><Spinner className="h-5 w-5 text-volt-400" /></div>;

  if (rows.length === 0)
    return (
      <Empty icon="history" title="No submissions yet"
             hint="Press Submit and every graded attempt shows up here, with the code you wrote." />
    );

  const accepted = rows.filter((r) => r.verdict === "accepted").length;
  const best = rows.filter((r) => r.verdict === "accepted")
                   .reduce<number | null>((m, r) => (m === null ? r.elapsedMs : Math.min(m, r.elapsedMs)), null);

  return (
    <div className="relative h-full">
      <div className="scroll-thin h-full overflow-y-auto">
        <div className="space-y-3 px-5 py-4">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11.5px] text-mist-400">
            <span><span className="font-mono text-mist-100">{rows.length}</span> submissions</span>
            <span><span className="font-mono text-mint-400">{accepted}</span> accepted</span>
            {best !== null && (
              <span>best <span className="font-mono text-mist-100">{Math.round(best)} ms</span></span>
            )}
          </div>

          <div className="overflow-hidden rounded-xl border border-white/[.06]">
            {rows.map((r, i) => (
              <button
                key={r.id}
                onClick={() => void openOne(r)}
                className={`flex w-full items-center gap-3 px-3.5 py-2.5 text-left transition-colors
                            hover:bg-white/[.03] ${i > 0 ? "border-t border-white/[.04]" : ""}`}
              >
                <VerdictPill verdict={r.verdict} />
                <span className="font-mono text-[11.5px] text-mist-300">
                  {r.passed}/{r.total}
                </span>
                <span className="ml-auto font-mono text-[11px] text-mist-400">
                  {Math.round(r.elapsedMs)} ms
                </span>
                <span className="w-20 text-right text-[11px] text-mist-400">
                  {timeAgo(r.createdAt)}
                </span>
                <Icon name="code" className="h-3.5 w-3.5 text-ink-500" />
              </button>
            ))}
          </div>
        </div>
      </div>

      {open && (
        <CodeSheet sub={open} onClose={() => setOpen(null)}
                   onRestore={(src) => { onRestore(src); setOpen(null); }} />
      )}
    </div>
  );
}
