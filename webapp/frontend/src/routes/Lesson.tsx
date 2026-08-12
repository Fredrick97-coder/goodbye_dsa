import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Markdown } from "../components/Markdown";
import { Empty, Icon, Spinner } from "../components/ui";
import { ApiError, api } from "../lib/api";
import { useAuth } from "../lib/auth";
import type { LessonDetail } from "../lib/types";

export default function Lesson() {
  const { courseId = "", moduleId = "", slug = "" } = useParams();
  const { user, requireAuth } = useAuth();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setLesson(null);
    setError(null);
    window.scrollTo(0, 0);
    let alive = true;
    void (async () => {
      try {
        const data = await api.lesson(courseId, moduleId, slug);
        if (alive) setLesson(data);
      } catch (err) {
        if (alive) setError(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => { alive = false; };
  }, [courseId, moduleId, slug, user]);

  const toggle = useCallback((advance: boolean) => {
    if (!lesson) return;
    requireAuth(() => void save(advance), "Sign in to track what you have read.");
  }, [lesson, requireAuth]);   // eslint-disable-line react-hooks/exhaustive-deps

  const save = async (advance: boolean) => {
    if (!lesson) return;
    const next = advance ? true : !lesson.completed;
    setSaving(true);
    // Optimistic: the tick should land the moment it is clicked.
    setLesson({ ...lesson, completed: next });
    try {
      await api.markLesson(courseId, moduleId, slug, next);
      if (advance && lesson.next) {
        navigate(`/learn/${courseId}/${lesson.next.moduleId}/${lesson.next.slug}`);
      }
    } catch (err) {
      setLesson({ ...lesson, completed: !next });
      setError(err instanceof ApiError ? err.message : String(err));
    } finally {
      setSaving(false);
    }
  };

  /* ←/→ move between lessons. A reader that needs the mouse to turn the page
     is a reader people stop using. */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if (e.key === "ArrowLeft" && lesson?.prev) {
        navigate(`/learn/${courseId}/${lesson.prev.moduleId}/${lesson.prev.slug}`);
      }
      if (e.key === "ArrowRight" && lesson?.next) {
        navigate(`/learn/${courseId}/${lesson.next.moduleId}/${lesson.next.slug}`);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [lesson, courseId, navigate]);

  if (error && !lesson)
    return <Empty icon="book" title="Could not load that lesson" hint={error}
                  action={<Link to={`/learn/${courseId}/${moduleId}`}
                                className="btn-outline mt-2">Back to the module</Link>} />;
  if (!lesson)
    return <div className="grid h-full place-items-center">
      <Spinner className="h-6 w-6 text-volt-400" /></div>;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <article className="mx-auto max-w-[760px] px-5 py-7">
        {/* ------------------------------------------------------ breadcrumb */}
        <nav className="flex flex-wrap items-center gap-2 text-[11.5px] text-mist-400">
          <Link to="/learn" className="hover:text-mist-200">Courses</Link>
          <span className="text-ink-600">/</span>
          <Link to={`/learn/${courseId}`} className="hover:text-mist-200">
            {lesson.courseTitle}
          </Link>
          <span className="text-ink-600">/</span>
          <Link to={`/learn/${courseId}/${moduleId}`}
                className="truncate hover:text-mist-200">{lesson.moduleTitle}</Link>
        </nav>

        <header className="mt-4">
          <p className="text-[11px] font-medium text-mist-400">
            Lesson {lesson.ordinal} of {lesson.moduleLessonCount} ·{" "}
            {lesson.minutes} min
            {lesson.codeBlocks > 0 && ` · ${lesson.codeBlocks} code blocks`}
          </p>
          <h1 className="mt-2 text-[26px] font-bold leading-tight tracking-tight text-white">
            {lesson.title}
          </h1>
        </header>

        <div className="mt-6">
          <Markdown body={lesson.body} />
        </div>

        {error && (
          <p className="mt-4 rounded-lg border border-rose-500/25 bg-rose-500/[.07]
                        px-3 py-2 text-[12px] text-rose-300">{error}</p>
        )}

        {/* --------------------------------------------------------- footer */}
        <div className="mt-10 space-y-4 border-t border-white/[.06] pt-5">
          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={() => toggle(false)}
              disabled={saving}
              className={lesson.completed ? "btn-outline" : "btn-primary"}
            >
              {saving ? <Spinner />
                : <Icon name={lesson.completed ? "reset" : "check"} className="h-4 w-4" />}
              {lesson.completed ? "Mark as unread" : "Mark as read"}
            </button>

            {lesson.next && (
              <button onClick={() => toggle(true)} disabled={saving}
                      className="btn-outline">
                Read &amp; continue <Icon name="arrowRight" className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          <div className="flex items-stretch justify-between gap-3">
            {lesson.prev ? (
              <Link to={`/learn/${courseId}/${lesson.prev.moduleId}/${lesson.prev.slug}`}
                    className="panel group min-w-0 flex-1 rounded-xl px-4 py-3
                               transition-all hover:border-volt-500/30">
                <p className="text-[10px] uppercase tracking-wider text-mist-400">
                  ← Previous
                </p>
                <p className="mt-1 truncate text-[12.5px] text-mist-200
                              group-hover:text-white">{lesson.prev.title}</p>
              </Link>
            ) : <span className="flex-1" />}

            {lesson.next ? (
              <Link to={`/learn/${courseId}/${lesson.next.moduleId}/${lesson.next.slug}`}
                    className="panel group min-w-0 flex-1 rounded-xl px-4 py-3 text-right
                               transition-all hover:border-volt-500/30">
                <p className="text-[10px] uppercase tracking-wider text-mist-400">
                  Next →
                </p>
                <p className="mt-1 truncate text-[12.5px] text-mist-200
                              group-hover:text-white">{lesson.next.title}</p>
              </Link>
            ) : (
              <Link to={`/learn/${courseId}/${moduleId}`}
                    className="panel group min-w-0 flex-1 rounded-xl px-4 py-3 text-right
                               transition-all hover:border-volt-500/30">
                <p className="text-[10px] uppercase tracking-wider text-mist-400">
                  End of the course
                </p>
                <p className="mt-1 truncate text-[12.5px] text-mist-200
                              group-hover:text-white">Back to the module</p>
              </Link>
            )}
          </div>

          <p className="text-center text-[10.5px] text-mist-400">
            ← and → move between lessons
          </p>
        </div>
      </article>
    </div>
  );
}
