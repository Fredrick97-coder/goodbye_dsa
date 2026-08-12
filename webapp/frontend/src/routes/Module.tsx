import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Empty, Icon, Spinner, StateMark } from "../components/ui";
import { DifficultyText } from "../components/ui";
import { Markdown } from "../components/Markdown";
import { ApiError, api } from "../lib/api";
import { useAuth } from "../lib/auth";
import type { ModuleDetail } from "../lib/types";

/** The module's examples.py, run in the same sandbox a submission uses. */
function Examples({ courseId, moduleId }: { courseId: string; moduleId: string }) {
  const { requireAuth } = useAuth();
  const [output, setOutput] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const run = () => requireAuth(() => void go(), "Sign in to run the examples.");

  const go = async () => {
    setBusy(true);
    setError(null);
    try {
      const res = await api.runExamples(courseId, moduleId);
      setOutput(res.stdout || "(the examples printed nothing)");
      if (res.error) setError(res.error);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="panel rounded-xl px-5 py-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="min-w-0 flex-1">
          <h3 className="text-[13.5px] font-semibold text-white">Worked examples</h3>
          <p className="mt-0.5 text-[11.5px] leading-relaxed text-mist-400">
            Runs this module's <code className="font-mono text-mist-300">examples.py</code>{" "}
            in the sandbox and shows what it prints — the same isolated runner
            that grades submissions.
          </p>
        </div>
        <button onClick={run} disabled={busy} className="btn-outline !py-1.5">
          {busy ? <Spinner /> : <Icon name="play" className="h-3.5 w-3.5" />}
          {output ? "Run again" : "Run examples"}
        </button>
      </div>

      {error && (
        <p className="mt-3 rounded-lg border border-amber-500/25 bg-amber-500/[.07]
                      px-3 py-2 text-[11.5px] leading-relaxed text-amber-200">
          {error}
        </p>
      )}
      {output && (
        <pre className="scroll-thin mt-3 max-h-[420px] overflow-auto rounded-xl
                        border border-white/[.06] bg-ink-950/70 px-4 py-3
                        font-mono text-[11.5px] leading-relaxed text-mist-300">
{output}
        </pre>
      )}
    </div>
  );
}

export default function Module() {
  const { courseId = "", moduleId = "" } = useParams();
  const { user } = useAuth();
  const [module, setModule] = useState<ModuleDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setModule(null);
    window.scrollTo(0, 0);
    void (async () => {
      try { setModule(await api.module(courseId, moduleId)); }
      catch (err) { setError(err instanceof Error ? err.message : String(err)); }
    })();
  }, [courseId, moduleId, user]);

  if (error) return <Empty icon="book" title="Could not load that module" hint={error} />;
  if (!module)
    return <div className="grid h-full place-items-center">
      <Spinner className="h-6 w-6 text-volt-400" /></div>;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-4xl px-5 py-7">
        <Link to={`/learn/${courseId}`} className="btn-ghost !px-0 text-[12px] text-mist-400">
          <Icon name="arrowLeft" className="h-3.5 w-3.5" /> {module.courseTitle}
        </Link>

        <div className="mt-3 flex items-baseline gap-3">
          <span className="font-mono text-[13px] text-mist-400">{module.id}</span>
          <h1 className="text-[21px] font-bold leading-tight tracking-tight text-white">
            {module.title}
          </h1>
        </div>
        <p className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11.5px] text-mist-400">
          <span>{module.level}</span>
          <span>{module.lessonCount} lessons · {module.minutes} min</span>
          {module.problemTotal > 0 && (
            <span>{module.problemsSolved}/{module.problemTotal} problems solved</span>
          )}
          {user && <span className="text-sky-400">
            {module.lessonsRead}/{module.lessonCount} read</span>}
        </p>

        {module.intro && (
          <div className="mt-5 rounded-xl border border-white/[.06] bg-ink-850/40 px-5 py-4">
            <Markdown body={module.intro} />
          </div>
        )}

        {/* ------------------------------------------------------- lessons */}
        <h2 className="mt-8 text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
          Lessons
        </h2>
        <div className="panel mt-2.5 overflow-hidden rounded-xl">
          {module.lessons.map((lesson) => (
            <Link
              key={lesson.slug}
              to={`/learn/${courseId}/${moduleId}/${lesson.slug}`}
              className="group flex items-center gap-3.5 border-b border-white/[.04]
                         px-4 py-3 transition-colors last:border-b-0 hover:bg-white/[.025]"
            >
              <span className={`grid h-5 w-5 shrink-0 place-items-center rounded-full
                                text-[10px] font-bold ${
                lesson.completed ? "bg-mint-500/20 text-mint-400"
                                 : "bg-ink-750 text-mist-400"}`}>
                {lesson.completed ? "✓" : lesson.ordinal}
              </span>
              <span className="min-w-0 flex-1 truncate text-[13px] text-mist-100
                               group-hover:text-white">
                {lesson.title}
              </span>
              {lesson.codeBlocks > 0 && (
                <span title={`${lesson.codeBlocks} code blocks`}
                      className="hidden items-center gap-1 font-mono text-[10.5px]
                                 text-mist-400 sm:flex">
                  <Icon name="code" className="h-3 w-3" />{lesson.codeBlocks}
                </span>
              )}
              <span className="w-12 shrink-0 text-right font-mono text-[10.5px] text-mist-400">
                {lesson.minutes} min
              </span>
            </Link>
          ))}
        </div>

        {/* ------------------------------------------------------ examples */}
        {module.hasExamples && (
          <div className="mt-5">
            <Examples courseId={courseId} moduleId={moduleId} />
          </div>
        )}

        {/* ------------------------------------------------------ practice */}
        {module.practice.length > 0 && (
          <>
            <div className="mt-8 flex items-baseline justify-between">
              <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
                Practice
              </h2>
              <Link to={`/problems?topic=${Number(moduleId)}`}
                    className="text-[11.5px] text-volt-300 hover:text-volt-200">
                open in the problem set →
              </Link>
            </div>
            <div className="panel mt-2.5 overflow-hidden rounded-xl">
              {module.practice.map((p) => (
                <Link key={p.id} to={`/problems/${p.id}`}
                      className="group flex items-center gap-3 border-b border-white/[.04]
                                 px-4 py-2.5 transition-colors last:border-b-0
                                 hover:bg-white/[.025]">
                  <StateMark state={p.status} />
                  <span className="font-mono text-[10.5px] text-mist-400">{p.id}</span>
                  <span className="min-w-0 flex-1 truncate text-[12.5px] text-mist-100
                                   group-hover:text-white">{p.title}</span>
                  {!p.tested && (
                    <span title="no reference tests"
                          className="h-1.5 w-1.5 rounded-full bg-amber-500/60" />
                  )}
                  <DifficultyText value={p.difficulty} />
                </Link>
              ))}
            </div>
          </>
        )}

        {module.hasProject && (
          <p className="mt-5 rounded-xl border border-white/[.06] bg-ink-850/40 px-5 py-3.5
                        text-[12px] leading-relaxed text-mist-400">
            This module also has a{" "}
            <code className="font-mono text-mist-300">project.py</code> — four
            real applications built on what you just read. Run it locally:{" "}
            <code className="font-mono text-mist-300">
              python python/{module.id}_*/project.py
            </code>
          </p>
        )}

        {/* ------------------------------------------------------- module nav */}
        <div className="mt-8 flex items-center justify-between gap-3 border-t
                        border-white/[.06] pt-5">
          {module.prevModule ? (
            <Link to={`/learn/${courseId}/${module.prevModule}`} className="btn-outline">
              <Icon name="arrowLeft" className="h-3.5 w-3.5" /> Module {module.prevModule}
            </Link>
          ) : <span />}
          {module.nextModule ? (
            <Link to={`/learn/${courseId}/${module.nextModule}`} className="btn-outline">
              Module {module.nextModule} <Icon name="arrowRight" className="h-3.5 w-3.5" />
            </Link>
          ) : <span />}
        </div>
      </div>
    </div>
  );
}
