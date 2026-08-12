import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Bar, Empty, Icon, Spinner } from "../components/ui";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { pct } from "../lib/format";
import type { CourseDetail, ModuleSummary } from "../lib/types";

const LEVEL_TONE: Record<string, string> = {
  Beginner: "text-mint-400",
  Intermediate: "text-sky-400",
  Advanced: "text-amber-400",
  "Interview Prep": "text-volt-300",
};

function ModuleRow({ courseId, module: m, signedIn }: {
  courseId: string; module: ModuleSummary; signedIn: boolean;
}) {
  const readAll = m.lessonsRead === m.lessonCount && m.lessonCount > 0;
  const locked = m.unlocked === false;
  return (
    <Link
      to={`/learn/${courseId}/${m.id}`}
      title={locked ? m.lockedReason ?? "locked" : undefined}
      className={`group grid grid-cols-[34px_minmax(0,1fr)_auto] items-center gap-4
                 border-b border-white/[.04] px-5 py-3.5 transition-colors
                 sm:grid-cols-[34px_minmax(0,1fr)_130px_96px] ${
        locked ? "hover:bg-white/[.015]" : "hover:bg-white/[.025]"}`}
    >
      <span className={`grid h-7 w-7 place-items-center rounded-lg font-mono text-[11px] ${
        locked ? "bg-ink-850 text-ink-500"
        : readAll ? "bg-mint-500/15 text-mint-400" : "bg-ink-800 text-mist-400"}`}>
        {locked ? <Icon name="lock" className="h-3.5 w-3.5" />
          : readAll ? <Icon name="check" className="h-3.5 w-3.5" /> : m.id}
      </span>

      <div className="min-w-0">
        <p className={`truncate text-[13.5px] font-medium ${
          locked ? "text-mist-400" : "text-mist-100 group-hover:text-white"}`}>
          {m.title}
        </p>
        <p className="mt-0.5 flex flex-wrap items-center gap-x-3 text-[11px] text-mist-400">
          {locked ? (
            <span className="truncate text-amber-400/80">{m.lockedReason}</span>
          ) : (
            <>
              <span>{m.lessonCount} lessons</span>
              <span>{m.minutes} min</span>
              {m.problemTotal > 0 && <span>{m.problemTotal} problems</span>}
              {m.hasProject && <span className="text-volt-300/70">project</span>}
            </>
          )}
        </p>
      </div>

      <div className="hidden sm:block">
        {signedIn ? (
          <div className="space-y-1">
            <Bar value={m.lessonsRead} total={m.lessonCount} tone="bg-sky-500"
                 className="h-1" />
            {m.problemTotal > 0 && (
              <Bar value={m.problemsSolved} total={m.problemTotal}
                   tone="bg-mint-500" className="h-1" />
            )}
          </div>
        ) : (
          <span className={`text-[11px] font-medium ${LEVEL_TONE[m.level] ?? ""}`}>
            {m.level}
          </span>
        )}
      </div>

      <div className="hidden text-right sm:block">
        {signedIn ? (
          <span className="font-mono text-[11px] text-mist-400">
            {m.lessonsRead}/{m.lessonCount}
          </span>
        ) : (
          <Icon name="arrowRight" className="ml-auto h-3.5 w-3.5 text-ink-500
                                             group-hover:text-volt-300" />
        )}
      </div>
    </Link>
  );
}

export default function Course() {
  const { courseId = "" } = useParams();
  const { user } = useAuth();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setCourse(null);
    void (async () => {
      try { setCourse(await api.course(courseId)); }
      catch (err) { setError(err instanceof Error ? err.message : String(err)); }
    })();
  }, [courseId, user]);

  if (error) return <Empty icon="book" title="Could not load that course" hint={error} />;
  if (!course)
    return <div className="grid h-full place-items-center">
      <Spinner className="h-6 w-6 text-volt-400" /></div>;

  const levels = course.levels.filter(
    (level) => course.modules.some((m) => m.level === level));

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-4xl px-5 py-7">
        <Link to="/learn" className="btn-ghost !px-0 text-[12px] text-mist-400">
          <Icon name="arrowLeft" className="h-3.5 w-3.5" /> All courses
        </Link>

        <h1 className="mt-3 text-[22px] font-bold tracking-tight text-white">
          {course.title}
        </h1>
        <p className="mt-1.5 max-w-2xl text-[13px] leading-relaxed text-mist-400">
          {course.subtitle}
        </p>

        <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 text-[11.5px] text-mist-400">
          <span><span className="font-mono text-mist-200">{course.moduleCount}</span> modules</span>
          <span><span className="font-mono text-mist-200">{course.lessonCount}</span> lessons</span>
          {course.problemTotal ? (
            <span><span className="font-mono text-mist-200">{course.problemTotal}</span> problems</span>
          ) : null}
          {user && (
            <span className="text-sky-400">
              {pct(course.lessonsRead, course.lessonCount)}% read
            </span>
          )}
        </div>

        {course.progression?.enabled && user && (
          <p className="mt-4 flex flex-wrap items-center gap-2 rounded-xl border
                        border-white/[.06] bg-ink-850/40 px-4 py-2.5 text-[11.5px]
                        text-mist-400">
            <Icon name="lock" className="h-3.5 w-3.5 text-amber-400/80" />
            <span>
              <span className="font-mono text-mist-200">
                {course.progression.modulesUnlocked}/{course.progression.moduleCount}
              </span>{" "}
              modules open. The next opens when you have read this one's lessons
              and solved{" "}
              {Math.round(course.progression.rule.requireProblems * 100)}% of its
              problems — or unlock it anyway from the module page.
            </span>
          </p>
        )}

        {course.resume && (
          <Link
            to={`/learn/${course.id}/${course.resume.moduleId}/${course.resume.slug}`}
            className="panel group mt-6 flex items-center gap-4 rounded-2xl px-5 py-4
                       transition-all hover:border-volt-500/30"
          >
            <div className="min-w-0 flex-1">
              <p className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
                {course.lessonsRead > 0 ? "Next up" : "Start here"}
              </p>
              <p className="mt-1.5 truncate text-[14px] font-semibold text-mist-100
                            group-hover:text-white">
                {course.resume.title}
              </p>
              <p className="mt-0.5 truncate text-[11.5px] text-mist-400">
                {course.resume.moduleTitle} · lesson {course.resume.ordinal} ·{" "}
                {course.resume.minutes} min
              </p>
            </div>
            <Icon name="arrowRight" className="h-4 w-4 shrink-0 text-mist-400
                                               group-hover:text-volt-300" />
          </Link>
        )}

        <div className="mt-6 space-y-6">
          {levels.map((level) => {
            const group = course.modules.filter((m) => m.level === level);
            const read = group.reduce((n, m) => n + m.lessonsRead, 0);
            const total = group.reduce((n, m) => n + m.lessonCount, 0);
            return (
              <section key={level}>
                <div className="mb-2 flex items-center gap-3">
                  <h2 className={`text-[11.5px] font-bold uppercase tracking-[.14em] ${
                    LEVEL_TONE[level] ?? "text-mist-400"}`}>{level}</h2>
                  {user && (
                    <span className="font-mono text-[11px] text-mist-400">
                      {read}/{total}
                    </span>
                  )}
                  <div className="h-px flex-1 bg-white/[.06]" />
                </div>
                <div className="panel overflow-hidden rounded-xl">
                  {group.map((m) => (
                    <ModuleRow key={m.id} courseId={course.id} module={m}
                               signedIn={Boolean(user)} />
                  ))}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
