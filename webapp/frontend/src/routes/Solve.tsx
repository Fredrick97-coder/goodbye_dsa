import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Group, Panel, Separator } from "react-resizable-panels";
import { Editor } from "../components/Editor";
import { NotesTab } from "../components/NotesTab";
import { ProblemList } from "../components/ProblemList";
import { Results } from "../components/Results";
import { Statement } from "../components/Statement";
import { SubmissionsTab } from "../components/SubmissionsTab";
import { DifficultyBadge, Empty, Icon, Segmented, Spinner } from "../components/ui";
import { api, ApiError, drafts } from "../lib/api";
import { useAppData } from "../lib/app-data";
import { draftOwner, useAuth } from "../lib/auth";
import type { Language, ProblemDetail, SubmitReport } from "../lib/types";

type LeftTab = "description" | "submissions" | "notes";

export default function Solve() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { meta, patch, byId } = useAppData();
  const { user, requireAuth } = useAuth();
  const owner = draftOwner(user);

  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [langId, setLangId] = useState("python");
  const [source, setSource] = useState("");
  const [report, setReport] = useState<SubmitReport | null>(null);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [listOpen, setListOpen] = useState(false);
  const [leftTab, setLeftTab] = useState<LeftTab>("description");
  const [bottomTab, setBottomTab] = useState<"results" | "console">("results");
  const [historyKey, setHistoryKey] = useState(0);

  const language: Language | undefined = useMemo(
    () => meta?.languages.find((l) => l.id === langId), [meta, langId],
  );
  const summary = byId.get(id);

  /* ------------------------------------------------------ load the problem */
  useEffect(() => {
    let alive = true;
    setProblem(null);
    setReport(null);
    setRunError(null);
    setLoadError(null);
    setLeftTab("description");
    void (async () => {
      try {
        const detail = await api.problem(id);
        if (!alive) return;
        setProblem(detail);
        setSource(drafts.load(owner, id, langId) ?? detail.starterCode[langId] ?? "");
      } catch (err) {
        if (alive) setLoadError(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => { alive = false; };
    // langId is intentionally out: switching language keeps the loaded problem
    // and is handled by the effect below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  /* swap the buffer when the language changes, without refetching */
  useEffect(() => {
    if (!problem) return;
    setSource(drafts.load(owner, problem.id, langId) ?? problem.starterCode[langId] ?? "");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [langId]);

  /* persist the draft, debounced */
  const saveTimer = useRef<number | undefined>(undefined);
  useEffect(() => {
    if (!problem) return;
    window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(
      () => drafts.save(owner, problem.id, langId, source), 400);
    return () => window.clearTimeout(saveTimer.current);
  }, [source, problem, langId, owner]);

  /* ------------------------------------------------------------- execution */
  const runNow = useCallback(async (mode: "test" | "run") => {
    if (!problem || running) return;
    setRunning(true);
    setRunError(null);
    setBottomTab(mode === "run" ? "console" : "results");
    try {
      const result = await api.submit(problem.id, langId, source, mode);
      setReport(result);
      if (mode === "test" && result.submissionId !== null) {
        setHistoryKey((k) => k + 1);
        setProblem((p) => (p ? { ...p, submissionCount: p.submissionCount + 1 } : p));
        // The server owns solved-state now; mirror it locally so the sidebar
        // and the nav counter update without refetching 342 rows. A later wrong
        // answer must not un-solve a problem -- the server would still report
        // it solved, so downgrading here would just disagree with the API.
        const accepted = result.summary.verdict === "accepted";
        patch(problem.id, {
          attempts: (summary?.attempts ?? 0) + 1,
          status: accepted ? "solved"
                : summary?.status === "solved" ? "solved" : "attempted",
        });
      }
    } catch (err) {
      // A 401 here means the session expired between loading the page and
      // pressing Submit. The provider has already dropped us to signed-out, so
      // reopening the gate is the right move rather than showing a raw error.
      if (err instanceof ApiError && err.isUnauthorized) {
        requireAuth(() => { void runNow("test"); },
                    "Sign in to submit and track your progress.");
      } else {
        setRunError(err instanceof Error ? err.message : String(err));
      }
    } finally {
      setRunning(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [problem, langId, source, running, patch, summary, requireAuth]);

  /**
   * Submit is gated; Run is not.
   *
   * You can write and execute code without an account -- the prompt appears at
   * the moment your work would be recorded, and the submission is replayed
   * automatically once you are in, so the click is never wasted.
   */
  const execute = useCallback((mode: "test" | "run") => {
    if (mode === "run") { void runNow("run"); return; }
    requireAuth(() => { void runNow("test"); },
                "Sign in to submit and track your progress.");
  }, [runNow, requireAuth]);

  const reset = useCallback(() => {
    if (!problem) return;
    drafts.clear(owner, problem.id, langId);
    setSource(problem.starterCode[langId] ?? "");
    setReport(null);
    setRunError(null);
  }, [problem, langId, owner]);

  const star = () => {
    if (!problem) return;
    requireAuth(() => void toggleStar(),
                "Sign in to bookmark problems.");
  };

  const toggleStar = async () => {
    if (!problem) return;
    const next = !problem.bookmarked;
    setProblem({ ...problem, bookmarked: next });
    patch(problem.id, { bookmarked: next });
    try {
      const res = await api.toggleBookmark(problem.id);
      setProblem((p) => (p ? { ...p, bookmarked: res.bookmarked } : p));
      patch(problem.id, { bookmarked: res.bookmarked });
    } catch {
      setProblem((p) => (p ? { ...p, bookmarked: !next } : p));
      patch(problem.id, { bookmarked: !next });
    }
  };

  /* keyboard: Cmd/Ctrl+Enter submit, Cmd/Ctrl+' run */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!(e.metaKey || e.ctrlKey)) return;
      if (e.key === "Enter") { e.preventDefault(); execute("test"); }
      if (e.key === "'") { e.preventDefault(); execute("run"); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [execute]);

  /* ---------------------------------------------------------------- render */
  if (loadError)
    return (
      <Empty icon="x" title="Could not load that problem" hint={loadError}
             action={<Link to="/problems" className="btn-outline mt-2">Back to problems</Link>} />
    );

  if (!problem || !meta)
    return (
      <div className="grid h-full place-items-center">
        <Spinner className="h-6 w-6 text-volt-400" />
      </div>
    );

  const verdictTone =
    report?.summary.verdict === "accepted" ? "ring-mint-500/40"
    : report?.summary.verdict === "failed" ? "ring-rose-500/40"
    : "ring-white/[.06]";

  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* -------------------------------------------------- problem toolbar */}
      <div className="flex h-11 shrink-0 items-center gap-2 border-b border-white/[.06]
                      bg-ink-900/60 px-3">
        <button onClick={() => setListOpen(!listOpen)}
                className={`btn-ghost !px-2 !py-1.5 ${listOpen ? "bg-white/[.06] text-white" : ""}`}
                title="Switch problem">
          <Icon name="list" className="h-4 w-4" />
        </button>

        <div className="flex items-center">
          <button onClick={() => problem.prevId && navigate(`/problems/${problem.prevId}`)}
                  disabled={!problem.prevId} className="btn-ghost !px-1.5 !py-1.5" title="Previous problem">
            <Icon name="arrowLeft" className="h-3.5 w-3.5" />
          </button>
          <button onClick={() => problem.nextId && navigate(`/problems/${problem.nextId}`)}
                  disabled={!problem.nextId} className="btn-ghost !px-1.5 !py-1.5" title="Next problem">
            <Icon name="arrowRight" className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="ml-1 flex min-w-0 items-center gap-2">
          <span className="truncate text-[13px] font-semibold text-white">{problem.title}</span>
          <DifficultyBadge value={problem.difficulty} />
          {summary?.status === "solved" && (
            <span className="chip bg-mint-500/12 text-mint-400 ring-1 ring-mint-500/25">
              <Icon name="check" className="h-3 w-3" /> Solved
            </span>
          )}
        </div>

        <button onClick={star} title={problem.bookmarked ? "Remove bookmark" : "Bookmark"}
                className={`btn-ghost !px-1.5 !py-1.5 ${problem.bookmarked ? "text-amber-400" : ""}`}>
          <Icon name={problem.bookmarked ? "star" : "starOutline"} className="h-4 w-4" />
        </button>

        <div className="ml-auto flex items-center gap-2">
          <div className="relative">
            <select
              value={langId}
              onChange={(e) => setLangId(e.target.value)}
              className="appearance-none rounded-lg border border-white/[.08] bg-ink-850 py-1.5 pl-3 pr-8
                         text-[12px] font-medium text-mist-100 focus:border-volt-500/50 focus:outline-none"
            >
              {meta.languages.map((l) => (
                <option key={l.id} value={l.id} disabled={!l.available}>
                  {l.label}{l.available ? "" : " — soon"}
                </option>
              ))}
            </select>
            <Icon name="chevron" className="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-mist-400" />
          </div>

          <button onClick={reset} className="btn-ghost !px-2 !py-1.5" title="Reset to starter code">
            <Icon name="reset" className="h-4 w-4" />
          </button>
          <button onClick={() => execute("run")} disabled={running}
                  className="btn-outline !py-1.5" title="Run (⌘')">
            {running ? <Spinner /> : <Icon name="play" className="h-3.5 w-3.5" />}
            <span className="hidden sm:inline">Run</span>
          </button>
          <button onClick={() => execute("test")} disabled={running}
                  className="btn-primary !py-1.5" title="Submit (⌘↵)">
            {running ? <Spinner /> : <Icon name="check" className="h-4 w-4" />}
            <span className="hidden sm:inline">Submit</span>
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------- workspace */}
      <div className="flex min-h-0 flex-1">
        {listOpen && (
          <div className="w-[290px] shrink-0 border-r border-white/[.06]">
            <ProblemList currentId={problem.id} onClose={() => setListOpen(false)} />
          </div>
        )}

        <Group orientation="horizontal" className="flex min-w-0 flex-1">
          <Panel defaultSize="42%" minSize="18%" className="min-w-0">
            <div className="flex h-full flex-col bg-ink-900/40">
              <div className="flex h-10 shrink-0 items-center border-b border-white/[.06] px-3">
                <Segmented
                  value={leftTab}
                  onChange={setLeftTab}
                  options={[
                    { id: "description", label: "Description" },
                    { id: "submissions", label: "Submissions", badge: problem.submissionCount },
                    { id: "notes", label: "Notes" },
                  ]}
                />
                {problem.hasNote && leftTab !== "notes" && (
                  <Icon name="note" className="ml-2 h-3.5 w-3.5 text-amber-400/70" />
                )}
              </div>
              <div className="min-h-0 flex-1">
                {leftTab === "description" && <Statement problem={problem} />}
                {leftTab === "submissions" && (user ? (
                  <SubmissionsTab problemId={problem.id} reloadKey={historyKey}
                                  onRestore={setSource} />
                ) : (
                  <Empty icon="history" title="History needs an account"
                         hint="Every graded attempt is kept with the code you wrote, so you can see what changed."
                         action={<button onClick={() => requireAuth(() => {}, "Sign in to keep your submission history.")}
                                         className="btn-primary mt-1">Sign in</button>} />
                ))}
                {leftTab === "notes" && (user ? (
                  <NotesTab problemId={problem.id}
                            onSavedChange={(has) => {
                              setProblem((p) => (p ? { ...p, hasNote: has } : p));
                              patch(problem.id, { hasNote: has });
                            }} />
                ) : (
                  <Empty icon="note" title="Notes need an account"
                         hint="Sign in and your notes are saved per problem, so the pattern you spotted is there next time."
                         action={<button onClick={() => requireAuth(() => {}, "Sign in to keep notes.")}
                                         className="btn-primary mt-1">Sign in</button>} />
                ))}
              </div>
            </div>
          </Panel>

          <Separator className="w-px bg-white/[.07]" />

          <Panel minSize="30%" className="min-w-0">
            <Group orientation="vertical" className="flex h-full flex-col">
              <Panel defaultSize="62%" minSize="15%">
                <div className="flex h-full flex-col bg-ink-900">
                  <div className="flex h-9 shrink-0 items-center gap-2 border-b border-white/[.06] px-3">
                    <Icon name="doc" className="h-3.5 w-3.5 text-mist-400" />
                    <span className="font-mono text-[11.5px] text-mist-300">
                      solution.{language?.ext ?? "py"}
                    </span>
                    {!problem.tested && (
                      <span className="chip bg-amber-500/12 text-amber-400">no auto-grading</span>
                    )}
                    <span className="ml-auto hidden font-mono text-[10.5px] text-mist-400 lg:inline">
                      ⌘↵ submit · ⌘' run
                    </span>
                  </div>
                  <div className="min-h-0 flex-1">
                    {language
                      ? <Editor value={source} language={language}
                                onChange={setSource} onSubmit={() => execute("test")} />
                      : <Empty icon="doc" title="No language selected" />}
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
