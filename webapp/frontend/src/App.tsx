import { useCallback, useEffect, useMemo, useRef, useState } from "react";
// react-resizable-panels v4 renamed the API: Group/Panel/Separator, with
// `orientation` instead of `direction` and percentage sizes as strings.
import { Group, Panel, Separator } from "react-resizable-panels";
import { Editor } from "./components/Editor";
import { ProblemList } from "./components/ProblemList";
import { Results } from "./components/Results";
import { Statement } from "./components/Statement";
import { Empty, Icon, Segmented, Spinner } from "./components/ui";
import { api, drafts, progress } from "./lib/api";
import type {
  Language, Meta, ProblemDetail, ProblemSummary, SubmitReport,
} from "./lib/types";

const LAST_KEY = "forge:last";

export default function App() {
  const [meta, setMeta] = useState<Meta | null>(null);
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [langId, setLangId] = useState("python");
  const [source, setSource] = useState("");
  const [report, setReport] = useState<SubmitReport | null>(null);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);
  const [bootError, setBootError] = useState<string | null>(null);
  const [listOpen, setListOpen] = useState(true);
  const [bottomTab, setBottomTab] = useState<"results" | "console">("results");
  const [solved, setSolved] = useState(progress.all());

  const language: Language | undefined = useMemo(
    () => meta?.languages.find((l) => l.id === langId),
    [meta, langId],
  );

  /* ------------------------------------------------------------- boot */
  useEffect(() => {
    (async () => {
      try {
        const [m, list] = await Promise.all([api.meta(), api.problems()]);
        setMeta(m);
        setProblems(list);
        const last = localStorage.getItem(LAST_KEY);
        const first = list.find((p) => p.id === last) ?? list.find((p) => p.tested) ?? list[0];
        if (first) void load(first.id);
      } catch (err) {
        setBootError(
          err instanceof Error ? err.message : "could not reach the API",
        );
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* --------------------------------------------------- load a problem */
  const load = useCallback(async (id: string) => {
    setReport(null);
    setRunError(null);
    try {
      const detail = await api.problem(id);
      setProblem(detail);
      localStorage.setItem(LAST_KEY, id);
      const saved = drafts.load(id, langId);
      setSource(saved ?? detail.starterCode[langId] ?? "");
    } catch (err) {
      setRunError(err instanceof Error ? err.message : String(err));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [langId]);

  /* persist the draft, debounced */
  const saveTimer = useRef<number | undefined>(undefined);
  useEffect(() => {
    if (!problem) return;
    window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(
      () => drafts.save(problem.id, langId, source), 400,
    );
    return () => window.clearTimeout(saveTimer.current);
  }, [source, problem, langId]);

  /* ------------------------------------------------------------ actions */
  const execute = useCallback(async (mode: "test" | "run") => {
    if (!problem || running) return;
    setRunning(true);
    setRunError(null);
    setBottomTab(mode === "run" ? "console" : "results");
    try {
      const result = await api.submit(problem.id, langId, source, mode);
      setReport(result);
      if (result.summary.verdict === "accepted") {
        progress.mark(problem.id, result.elapsedMs);
        setSolved(progress.all());
      }
    } catch (err) {
      setRunError(err instanceof Error ? err.message : String(err));
    } finally {
      setRunning(false);
    }
  }, [problem, langId, source, running]);

  const reset = useCallback(() => {
    if (!problem) return;
    drafts.clear(problem.id, langId);
    setSource(problem.starterCode[langId] ?? "");
    setReport(null);
    setRunError(null);
  }, [problem, langId]);

  /* keyboard: Cmd/Ctrl+Enter submit, Cmd/Ctrl+' run */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!(e.metaKey || e.ctrlKey)) return;
      if (e.key === "Enter") { e.preventDefault(); void execute("test"); }
      if (e.key === "'") { e.preventDefault(); void execute("run"); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [execute]);

  /* ------------------------------------------------------------- render */
  if (bootError) {
    return (
      <div className="grid h-full place-items-center px-6">
        <div className="panel max-w-md rounded-2xl px-6 py-6 text-center">
          <div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-rose-500/12">
            <Icon name="x" className="h-5 w-5 text-rose-400" />
          </div>
          <h1 className="mt-4 text-base font-bold text-white">API unreachable</h1>
          <p className="mt-2 text-[12.5px] leading-relaxed text-mist-300">{bootError}</p>
          <pre className="mt-4 overflow-x-auto rounded-lg bg-ink-950/70 px-3 py-2.5 text-left font-mono text-[11.5px] text-mist-300">
{`cd webapp/backend
python3 -m uvicorn app.main:app --reload`}
          </pre>
        </div>
      </div>
    );
  }

  if (!meta) {
    return (
      <div className="grid h-full place-items-center gap-3">
        <Spinner className="h-6 w-6 text-volt-400" />
      </div>
    );
  }

  const verdictTone =
    report?.summary.verdict === "accepted" ? "ring-mint-500/40"
    : report?.summary.verdict === "failed" ? "ring-rose-500/40"
    : "ring-white/[.06]";

  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* ------------------------------------------------------- top bar */}
      <header className="z-30 flex h-14 shrink-0 items-center gap-3 border-b border-white/[.06]
                         bg-ink-900/80 px-3 backdrop-blur-xl">
        <button onClick={() => setListOpen(!listOpen)} className="btn-ghost !px-2"
                title="Toggle problem list">
          <Icon name="list" className="h-4 w-4" />
        </button>

        <div className="flex items-center gap-2">
          <div className="grid h-7 w-7 place-items-center rounded-lg bg-volt-500 shadow-glow">
            <Icon name="spark" className="h-4 w-4 text-white" />
          </div>
          <div className="leading-none">
            <p className="text-[13px] font-bold tracking-tight text-white">Forge</p>
            <p className="mt-0.5 text-[10px] text-mist-400">
              {meta.stats.problems} problems · {meta.stats.specCount} tests
            </p>
          </div>
        </div>

        {problem && (
          <div className="ml-2 hidden min-w-0 items-center gap-2 md:flex">
            <span className="text-ink-600">/</span>
            <span className="truncate text-[13px] font-semibold text-mist-100">
              {problem.title}
            </span>
          </div>
        )}

        <div className="ml-auto flex items-center gap-2">
          {/* language picker: unavailable ones are visibly disabled, not hidden */}
          <div className="relative">
            <select
              value={langId}
              onChange={(e) => setLangId(e.target.value)}
              className="appearance-none rounded-lg border border-white/[.08] bg-ink-850 py-1.5 pl-3 pr-8
                         text-[12.5px] font-medium text-mist-100 focus:border-volt-500/50 focus:outline-none"
            >
              {meta.languages.map((l) => (
                <option key={l.id} value={l.id} disabled={!l.available}>
                  {l.label}{l.available ? "" : " — soon"}
                </option>
              ))}
            </select>
            <Icon name="chevron" className="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mist-400" />
          </div>

          <button onClick={reset} className="btn-ghost !px-2" title="Reset to starter code">
            <Icon name="reset" className="h-4 w-4" />
          </button>

          <button onClick={() => void execute("run")} disabled={running || !problem}
                  className="btn-outline" title="Run (⌘')">
            {running ? <Spinner /> : <Icon name="play" className="h-3.5 w-3.5" />}
            <span className="hidden sm:inline">Run</span>
          </button>

          <button onClick={() => void execute("test")} disabled={running || !problem}
                  className="btn-primary" title="Submit (⌘↵)">
            {running ? <Spinner /> : <Icon name="check" className="h-4 w-4" />}
            <span className="hidden sm:inline">Submit</span>
          </button>
        </div>
      </header>

      {/* ------------------------------------------------------ workspace */}
      <div className="flex min-h-0 flex-1">
        {listOpen && (
          <div className="w-[300px] shrink-0 border-r border-white/[.06]">
            <ProblemList
              problems={problems}
              meta={meta}
              currentId={problem?.id ?? null}
              solved={solved}
              onPick={(id) => void load(id)}
              onClose={() => setListOpen(false)}
            />
          </div>
        )}

        <Group orientation="horizontal" className="flex min-w-0 flex-1">
          {/* problem statement */}
          <Panel defaultSize="40%" minSize="18%" className="min-w-0">
            <div className="h-full bg-ink-900/40">
              {problem
                ? <Statement problem={problem} />
                : <Empty icon="doc" title="Pick a problem" hint="Choose one from the list to get started." />}
            </div>
          </Panel>

          <Separator className="w-px bg-white/[.07]" />

          {/* editor + results */}
          <Panel minSize="30%" className="min-w-0">
            <Group orientation="vertical" className="flex h-full flex-col">
              <Panel defaultSize="62%" minSize="15%">
                <div className="flex h-full flex-col bg-ink-900">
                  <div className="flex h-9 shrink-0 items-center gap-2 border-b border-white/[.06] px-3">
                    <Icon name="doc" className="h-3.5 w-3.5 text-mist-400" />
                    <span className="font-mono text-[11.5px] text-mist-300">
                      solution.{language?.ext ?? "py"}
                    </span>
                    {problem && !problem.tested && (
                      <span className="chip ml-auto bg-amber-500/12 text-amber-400">
                        no auto-grading
                      </span>
                    )}
                    <span className="ml-auto hidden font-mono text-[10.5px] text-mist-400 lg:inline">
                      ⌘↵ submit · ⌘' run
                    </span>
                  </div>
                  <div className="min-h-0 flex-1">
                    {problem && language
                      ? <Editor value={source} language={language}
                                onChange={setSource} onSubmit={() => void execute("test")} />
                      : <Empty icon="doc" title="No problem loaded" />}
                  </div>
                </div>
              </Panel>

              <Separator className="h-px bg-white/[.07]" />

              <Panel defaultSize="38%" minSize="10%">
                <div className={`flex h-full flex-col bg-ink-900/60 ring-1 ring-inset ${verdictTone} transition-colors`}>
                  <div className="flex h-9 shrink-0 items-center gap-3 border-b border-white/[.06] px-3">
                    <Segmented
                      value={bottomTab}
                      onChange={setBottomTab}
                      options={[
                        { id: "results", label: "Test Results" },
                        { id: "console", label: "Console" },
                      ]}
                    />
                    {report && bottomTab === "results" && report.summary.total > 0 && (
                      <span className="ml-auto font-mono text-[11px] text-mist-400">
                        {report.summary.passed}/{report.summary.total}
                      </span>
                    )}
                  </div>
                  <div className="min-h-0 flex-1">
                    {bottomTab === "results" ? (
                      <Results report={report} running={running} error={runError} />
                    ) : (
                      <div className="scroll-thin h-full overflow-auto px-4 py-3">
                        {report?.stdout ? (
                          <pre className="whitespace-pre-wrap font-mono text-[12px] leading-relaxed text-mist-300">
{report.stdout}
                          </pre>
                        ) : (
                          <p className="font-mono text-[12px] text-mist-400">
                            {running ? "running…" : "No output. Add print() and press Run."}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </Panel>
            </Group>
          </Panel>
        </Group>
      </div>
    </div>
  );
}
