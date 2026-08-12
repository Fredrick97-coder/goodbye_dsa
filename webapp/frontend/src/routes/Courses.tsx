import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Bar, Empty, Icon, Spinner } from "../components/ui";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { pct } from "../lib/format";
import type { CourseSummary } from "../lib/types";

function hours(minutes: number): string {
  if (minutes < 90) return `${minutes} min`;
  return `${(minutes / 60).toFixed(minutes % 60 === 0 ? 0 : 1)} hours`;
}

function CourseCard({ course }: { course: CourseSummary }) {
  const { user } = useAuth();
  const readPct = pct(course.lessonsRead, course.lessonCount);
  const solvedPct = pct(course.problemsSolved ?? 0, course.problemTotal ?? 0);

  return (
    <Link
      to={`/learn/${course.id}`}
      className="panel group flex flex-col gap-4 rounded-2xl px-6 py-5 transition-all
                 hover:border-volt-500/30 hover:bg-ink-850/80"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h2 className="text-[17px] font-bold tracking-tight text-white
                         group-hover:text-volt-200">{course.title}</h2>
          <p className="mt-1.5 max-w-lg text-[12.5px] leading-relaxed text-mist-400">
            {course.subtitle}
          </p>
        </div>
        <Icon name="arrowRight"
              className="mt-1 h-4 w-4 shrink-0 text-mist-400 transition-transform
                         group-hover:translate-x-0.5 group-hover:text-volt-300" />
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11.5px] text-mist-400">
        <span><span className="font-mono text-mist-200">{course.moduleCount}</span> modules</span>
        <span><span className="font-mono text-mist-200">{course.lessonCount}</span> lessons</span>
        {course.problemTotal ? (
          <span><span className="font-mono text-mist-200">{course.problemTotal}</span> problems</span>
        ) : null}
        <span className="flex items-center gap-1">
          <Icon name="clock" className="h-3 w-3" />{hours(course.minutes)} of reading
        </span>
      </div>

      {course.practiceLanguages.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {course.practiceLanguages.map((l) => (
            <span key={l} className="chip bg-ink-800 text-mist-300 ring-1 ring-white/[.06]">
              {l}
            </span>
          ))}
        </div>
      )}

      {user && (
        <div className="space-y-2 border-t border-white/[.06] pt-3.5">
          <div className="flex items-center gap-3">
            <span className="w-16 text-[11px] text-mist-400">Reading</span>
            <Bar value={course.lessonsRead} total={course.lessonCount}
                 tone="bg-sky-500" className="h-1" />
            <span className="w-16 text-right font-mono text-[11px] text-mist-300">
              {course.lessonsRead}/{course.lessonCount}
            </span>
          </div>
          {course.problemTotal ? (
            <div className="flex items-center gap-3">
              <span className="w-16 text-[11px] text-mist-400">Practice</span>
              <Bar value={course.problemsSolved ?? 0} total={course.problemTotal}
                   tone="bg-mint-500" className="h-1" />
              <span className="w-16 text-right font-mono text-[11px] text-mist-300">
                {course.problemsSolved}/{course.problemTotal}
              </span>
            </div>
          ) : null}
          {readPct + solvedPct === 0 && (
            <p className="text-[11px] text-mist-400">Not started yet.</p>
          )}
        </div>
      )}
    </Link>
  );
}

export default function Courses() {
  const [courses, setCourses] = useState<CourseSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try { setCourses(await api.courses()); }
      catch (err) { setError(err instanceof Error ? err.message : String(err)); }
    })();
  }, []);

  if (error) return <Empty icon="book" title="Could not load courses" hint={error} />;
  if (!courses)
    return <div className="grid h-full place-items-center">
      <Spinner className="h-6 w-6 text-volt-400" /></div>;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-4xl px-5 py-8">
        <h1 className="text-[22px] font-bold tracking-tight text-white">Courses</h1>
        <p className="mt-1.5 text-[13px] text-mist-400">
          Read the theory, run the examples, then solve the problems for that topic.
        </p>

        <div className="mt-6 space-y-4">
          {courses.map((c) => <CourseCard key={c.id} course={c} />)}
        </div>

        {courses.length === 1 && (
          <p className="mt-6 text-center text-[11.5px] leading-relaxed text-mist-400">
            More courses drop in as directories with a{" "}
            <code className="font-mono text-mist-300">course.json</code> —
            nothing here is specific to data structures.
          </p>
        )}
      </div>
    </div>
  );
}
