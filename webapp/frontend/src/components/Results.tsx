import { useState } from "react";
import type { CaseResult, SubmitReport, TargetResult } from "../lib/types";
import { Empty, Icon, Spinner, VERDICT_META } from "./ui";

function Bar({ passed, total }: { passed: number; total: number }) {
  const pct = total ? (passed / total) * 100 : 0;
  const tone = pct === 100 ? "bg-mint-500" : pct > 0 ? "bg-amber-500" : "bg-rose-500";
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-ink-750">
      <div className={`h-full rounded-full ${tone} transition-all duration-500`}
           style={{ width: `${pct}%` }} />
    </div>
  );
}

/** A compact pass/fail strip — the fastest way to see where things broke. */
function CaseStrip({ cases }: { cases: CaseResult[] }) {
  if (cases.length === 0) return null;
  return (
    <div className="flex flex-wrap gap-1">
      {cases.map((c, i) => (
        <span
          key={i}
          title={`${c.name}: ${c.passed ? "passed" : c.error || "wrong answer"}`}
          className={`h-1.5 w-4 rounded-full ${c.passed ? "bg-mint-500/70" : "bg-rose-500"}`}
        />
      ))}
    </div>
  );
}

function CaseRow({ c }: { c: CaseResult }) {
  return (
    <div className={`rounded-lg border px-3 py-2.5 ${
      c.passed ? "border-white/[.05] bg-ink-850/40" : "border-rose-500/20 bg-rose-500/[.06]"
    }`}>
      <div className="flex items-center gap-2">
        <span className={`grid h-4 w-4 place-items-center rounded-full text-[9px] font-bold ${
          c.passed ? "bg-mint-500/20 text-mint-400" : "bg-rose-500/20 text-rose-400"
        }`}>
          {c.passed ? "✓" : "✕"}
        </span>
        <span className="font-mono text-[11.5px] font-medium text-mist-200">{c.name}</span>
      </div>

      {!c.passed && (
        <dl className="mt-2 space-y-1.5 pl-6 font-mono text-[11.5px]">
          {c.input && (
            <div className="flex gap-2">
              <dt className="w-16 shrink-0 text-mist-400">input</dt>
              <dd className="break-all text-mist-200">{c.input}</dd>
            </div>
          )}
          {c.error ? (
            <div className="flex gap-2">
              <dt className="w-16 shrink-0 text-amber-400">threw</dt>
              <dd className="break-all text-amber-300">{c.error}</dd>
            </div>
          ) : (
            <>
              <div className="flex gap-2">
                <dt className="w-16 shrink-0 text-mist-400">expected</dt>
                <dd className="break-all text-mint-400">{c.expected}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="w-16 shrink-0 text-mist-400">got</dt>
                <dd className="break-all text-rose-400">{c.got || "—"}</dd>
              </div>
            </>
          )}
        </dl>
      )}
    </div>
  );
}

function TargetBlock({ t }: { t: TargetResult }) {
  const failed = t.cases.filter((c) => !c.passed);
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? t.cases : failed.length ? failed : t.cases.slice(0, 3);

  return (
    <div className="space-y-2.5">
      <div className="flex items-center gap-3">
        <span className="font-mono text-[13px] font-semibold text-white">{t.target}</span>
        <span className={`chip ${
          t.status === "PASS" ? "bg-mint-500/12 text-mint-400"
          : t.status === "FAIL" ? "bg-rose-500/12 text-rose-400"
          : t.status === "STUB" ? "bg-ink-750 text-mist-400"
          : "bg-amber-500/12 text-amber-400"
        }`}>{t.status}</span>
        <span className="ml-auto font-mono text-[11.5px] text-mist-400">
          {t.passed}/{t.total}
        </span>
      </div>

      <Bar passed={t.passed} total={t.total} />
      <CaseStrip cases={t.cases} />

      {t.note && (
        <p className="rounded-lg bg-sky-500/[.07] px-3 py-2 text-[11.5px] leading-relaxed text-sky-300">
          <span className="font-semibold">Grading note </span>{t.note}
        </p>
      )}

      {visible.length > 0 && (
        <div className="space-y-1.5">
          {visible.map((c, i) => <CaseRow key={i} c={c} />)}
        </div>
      )}

      {t.cases.length > visible.length && (
        <button onClick={() => setShowAll(true)}
                className="btn-ghost !px-2 !py-1 text-[11px]">
          Show all {t.cases.length} recorded cases
        </button>
      )}
    </div>
  );
}

export function Results({
  report, running, error,
}: { report: SubmitReport | null; running: boolean; error: string | null }) {
  if (running) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-3 text-mist-400">
        <Spinner className="h-5 w-5 text-volt-400" />
        <p className="text-xs font-medium">Running against reference tests…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-5">
        <div className="rounded-xl border border-rose-500/25 bg-rose-500/[.07] px-4 py-3">
          <p className="text-xs font-semibold text-rose-400">Could not run</p>
          <p className="mt-1 font-mono text-[11.5px] leading-relaxed text-rose-300">{error}</p>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <Empty
        icon="flask"
        title="No run yet"
        hint="Press Run to execute your code, or Submit to grade it against the repo's reference tests."
      />
    );
  }

  const meta = VERDICT_META[report.summary.verdict];
  const ce = report.compileError;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="animate-fade-up space-y-4 px-5 py-4">
        {/* verdict header */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2">
            <span className={`grid h-6 w-6 place-items-center rounded-full bg-white/[.06] text-[12px] font-bold ${meta.tone}`}>
              {meta.icon}
            </span>
            <span className={`text-[15px] font-bold tracking-tight ${meta.tone}`}>
              {meta.label}
            </span>
          </div>
          {report.summary.total > 0 && (
            <span className="font-mono text-xs text-mist-400">
              {report.summary.passed}/{report.summary.total} cases
            </span>
          )}
          <span className="ml-auto flex items-center gap-1.5 font-mono text-[11px] text-mist-400">
            <Icon name="clock" className="h-3 w-3" />
            {report.elapsedMs} ms
          </span>
        </div>

        {report.untested && (
          <p className="rounded-xl border border-sky-500/20 bg-sky-500/[.07] px-4 py-3 text-[12px] leading-relaxed text-sky-300">
            This problem has no reference tests yet, so nothing was graded — your
            code simply ran. Two topics (Queues, Advanced Trees) are still
            uncovered; check those by hand.
          </p>
        )}

        {ce && (
          <div className="rounded-xl border border-amber-500/25 bg-amber-500/[.07] px-4 py-3">
            <p className="text-xs font-bold text-amber-400">
              {ce.type}{ce.line ? ` · line ${ce.line}` : ""}
            </p>
            <p className="mt-1.5 whitespace-pre-wrap font-mono text-[11.5px] leading-relaxed text-amber-200">
              {ce.message}
            </p>
            {ce.text && (
              <pre className="mt-2 overflow-x-auto rounded-lg bg-ink-950/60 px-3 py-2 font-mono text-[11.5px] text-mist-300">
                {ce.text}
              </pre>
            )}
          </div>
        )}

        {report.stdout && (
          <div className="space-y-1.5">
            <h4 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              stdout
            </h4>
            <pre className="scroll-thin max-h-40 overflow-auto rounded-xl border border-white/[.06]
                            bg-ink-950/60 px-3.5 py-2.5 font-mono text-[11.5px] leading-relaxed text-mist-300">
{report.stdout}
            </pre>
          </div>
        )}

        {report.targets
          .filter((t) => t.status !== "RAN")
          .map((t) => <TargetBlock key={t.target} t={t} />)}
      </div>
    </div>
  );
}
