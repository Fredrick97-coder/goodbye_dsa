import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Heatmap } from "../components/Heatmap";
import {
  Bar, DifficultyText, Empty, Icon, Ring, Spinner, StackedBar, StatCard, VerdictPill,
} from "../components/ui";
import { SignInPanel } from "../components/SignInPanel";
import { api } from "../lib/api";
import { useAppData } from "../lib/app-data";
import { useAuth } from "../lib/auth";
import { DIFF_BG, pct, pctLabel, timeAgo } from "../lib/format";
import type { Overview, TopicProgress } from "../lib/types";

const LEVEL_ORDER = ["Beginner", "Intermediate", "Advanced", "Interview Prep"];
const LEVEL_TONE: Record<string, string> = {
  Beginner: "text-mint-400",
  Intermediate: "text-sky-400",
  Advanced: "text-amber-400",
  "Interview Prep": "text-volt-300",
};

function TrackCard({ t }: { t: TopicProgress }) {
  const done = t.solved === t.total && t.total > 0;
  return (
    <Link
      to={`/problems?topic=${t.topic}`}
      className="panel group flex flex-col gap-2.5 rounded-xl px-4 py-3.5 transition-all
                 hover:border-volt-500/30 hover:bg-ink-850/80"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="font-mono text-[10px] text-mist-400">
            {String(t.topic).padStart(2, "0")}
          </p>
          <p className="mt-0.5 truncate text-[13px] font-semibold text-mist-100
                        transition-colors group-hover:text-white">
            {t.name}
          </p>
        </div>
        {done ? (
          <span className="grid h-5 w-5 shrink-0 place-items-center rounded-full bg-mint-500/15 text-mint-400">
            <Icon name="check" className="h-3 w-3" />
          </span>
        ) : (
          <span className="shrink-0 font-mono text-[11px] text-mist-400">
            {pct(t.solved, t.total)}%
          </span>
        )}
      </div>

      <Bar value={t.solved} total={t.total}
           tone={done ? "bg-mint-500" : "bg-volt-500"} className="h-1" />

      <div className="flex items-center gap-2 text-[10.5px] text-mist-400">
        <span className="font-mono text-mist-300">{t.solved}/{t.total}</span>
        {t.attempted > 0 && <span className="text-amber-400/80">{t.attempted} in progress</span>}
        {t.tested < t.total && (
          <span className="ml-auto" title={`${t.total - t.tested} problems have no reference tests`}>
            {t.tested}/{t.total} graded
          </span>
        )}
      </div>
    </Link>
  );
}

export default function Dashboard() {
  const { meta, problems } = useAppData();
  const { user } = useAuth();
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) { setData(null); setError(null); return; }
    // Aborted on cleanup, so logging out cancels the request rather than
    // letting it return 401 into a component that no longer wants it.
    const ac = new AbortController();
    void (async () => {
      try { setData(await api.overview(ac.signal)); setError(null); }
      catch (err) {
        if (ac.signal.aborted) return;
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => ac.abort();
  }, [problems, user]);   // re-pull after a submit patches the list

  // Signed out there is no progress to show, so pitch the account instead of
  // rendering a dashboard full of zeroes.
  if (!user)
    return (
      <div className="scroll-thin h-full overflow-y-auto px-5 py-6">
        <SignInPanel
          title="Track your progress"
          blurb={meta
            ? `${meta.stats.problems} problems across ${meta.topics.length} topics, ${meta.stats.tested} of them auto-graded. An account remembers which ones you have solved.`
            : "An account remembers which problems you have solved."}
          bullets={[
            "Solved and attempted state, per problem",
            "Every graded submission kept with the code you wrote",
            "Streaks, an activity heatmap, and per-topic progress",
            "Bookmarks and per-problem notes",
          ]}
        />
        <div className="mx-auto mt-4 max-w-lg text-center">
          <Link to="/problems" className="btn-ghost text-[12.5px]">
            Or browse all {meta?.stats.problems ?? ""} problems first
            <Icon name="arrowRight" className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    );

  if (error)
    return <Empty icon="x" title="Could not load progress" hint={error} />;
  if (!data || !meta)
    return <div className="grid h-full place-items-center"><Spinner className="h-6 w-6 text-volt-400" /></div>;

  const { totals, byDifficulty, byTopic, activity, recent, resume, nextUp } = data;
  const untouched = totals.problems - totals.solved - totals.attempted;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl space-y-6 px-5 py-6">
        {/* ------------------------------------------------------- headline */}
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-[22px] font-bold tracking-tight text-white">
              {totals.solved === 0 ? "Let's get started"
                : totals.solved === totals.problems ? "Curriculum complete"
                : "Keep going"}
            </h1>
            <p className="mt-1 text-[12.5px] text-mist-400">
              {totals.problems} problems across {meta.topics.length} topics ·{" "}
              {totals.tested} auto-graded against {meta.stats.specCount} reference tests
            </p>
          </div>
          <Link to="/problems" className="btn-primary">
            <Icon name="grid" className="h-4 w-4" /> Browse problems
          </Link>
        </div>

        {/* ---------------------------------------------------------- stats */}
        <div className="grid gap-4 lg:grid-cols-[auto_minmax(0,1fr)]">
          <div className="panel flex items-center gap-5 rounded-2xl px-6 py-5">
            <Ring solved={totals.solved} total={totals.problems} />
            <div className="space-y-2.5">
              {byDifficulty.map((d) => (
                <div key={d.difficulty} className="min-w-[150px]">
                  <div className="flex items-baseline justify-between gap-3">
                    <DifficultyText value={d.difficulty} />
                    <span className="font-mono text-[11.5px] text-mist-300">
                      {d.solved}<span className="text-mist-400">/{d.total}</span>
                    </span>
                  </div>
                  <Bar value={d.solved} total={d.total}
                       tone={DIFF_BG[d.difficulty]} className="mt-1 h-1" />
                </div>
              ))}
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <StatCard icon="flame" label="Current streak" tone="text-amber-400"
                      value={`${activity.streak}d`}
                      sub={`longest ${activity.longestStreak}d · ${activity.activeDays} active days`} />
            <StatCard icon="history" label="Submissions" tone="text-sky-400"
                      value={activity.totalSubmissions}
                      sub={`${totals.attempted} problems in progress`} />
            <StatCard icon="trophy" label="Solved" tone="text-mint-400"
                      value={totals.solved}
                      sub={`${pctLabel(totals.solved, totals.problems)} of the curriculum`} />
            <StatCard icon="doc" label="Untouched" tone="text-mist-400"
                      value={untouched} sub="not started yet" />
          </div>
        </div>

        {/* --------------------------------------------------------- resume */}
        {resume ? (
          <Link to={`/problems/${resume.id}`}
                className="panel group flex items-center gap-4 rounded-2xl px-5 py-4
                           transition-all hover:border-volt-500/30">
            <div className="min-w-0 flex-1">
              <p className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
                Pick up where you left off
              </p>
              <p className="mt-1.5 truncate text-[15px] font-semibold text-mist-100
                            group-hover:text-white">{resume.title}</p>
              <p className="mt-0.5 flex items-center gap-2 text-[11.5px] text-mist-400">
                <span className="font-mono">{resume.id}</span>
                <DifficultyText value={resume.difficulty} />
                <span className="truncate">{resume.topicName}</span>
                <span>· last tried {timeAgo(resume.at)}</span>
              </p>
            </div>
            <VerdictPill verdict={resume.verdict} />
            <Icon name="arrowRight" className="h-4 w-4 shrink-0 text-mist-400 group-hover:text-volt-300" />
          </Link>
        ) : (
          <div className="panel rounded-2xl px-5 py-4">
            <p className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Start here
            </p>
            <p className="mt-2 text-[12.5px] leading-relaxed text-mist-400">
              Nothing in progress. The suggested problems below are all
              auto-graded, so Submit gives real feedback rather than silence.
            </p>
          </div>
        )}

        {/* ------------------------------------------------- next and recent */}
        <div className="grid items-start gap-4 lg:grid-cols-2">
          <div className="panel rounded-2xl px-5 py-4">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Suggested next
            </h2>
            <div className="mt-3 space-y-1">
              {nextUp.length === 0 ? (
                <p className="text-[12.5px] text-mist-400">
                  Every auto-graded problem is solved. What is left has no
                  reference tests — filter for those on the problems page.
                </p>
              ) : nextUp.map((p) => (
                <Link key={p.id} to={`/problems/${p.id}`}
                      className="group flex items-center gap-3 rounded-lg px-2.5 py-2
                                 transition-colors hover:bg-white/[.04]">
                  <span className="font-mono text-[10.5px] text-mist-400">{p.id}</span>
                  <span className="min-w-0 flex-1 truncate text-[12.5px] text-mist-200
                                   group-hover:text-white">{p.title}</span>
                  <span className="truncate text-[11px] text-mist-400">{p.topicName}</span>
                  <DifficultyText value={p.difficulty} />
                </Link>
              ))}
            </div>
          </div>

          <div className="panel rounded-2xl px-5 py-4">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Recent submissions
            </h2>
            <div className="mt-3 space-y-1">
              {recent.length === 0 ? (
                <p className="text-[12.5px] text-mist-400">No graded submissions yet.</p>
              ) : recent.slice(0, 6).map((s) => (
                <Link key={s.id} to={`/problems/${s.problemId}`}
                      className="flex items-center gap-2.5 rounded-lg px-2.5 py-2
                                 transition-colors hover:bg-white/[.04]">
                  <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${
                    s.verdict === "accepted" ? "bg-mint-400"
                    : s.verdict === "failed" ? "bg-rose-400" : "bg-amber-400"}`} />
                  <span className="min-w-0 flex-1 truncate text-[12.5px] text-mist-300">
                    {s.title ?? s.problemId}
                  </span>
                  <span className="font-mono text-[10.5px] text-mist-400">
                    {s.passed}/{s.total}
                  </span>
                  <span className="w-16 text-right text-[10.5px] text-mist-400">
                    {timeAgo(s.createdAt)}
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------- composition */}
        <div className="panel rounded-2xl px-5 py-4">
          <div className="flex items-baseline justify-between">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Activity
            </h2>
            <p className="text-[11px] text-mist-400">
              last 26 weeks · {activity.activeDays} active days
            </p>
          </div>
          <div className="mt-4">
            {activity.days.length === 0 ? (
              <p className="py-4 text-center text-[12.5px] text-mist-400">
                The grid fills in as you submit.
              </p>
            ) : <Heatmap days={activity.days} weeks={26} />}
          </div>

          <div className="mt-6 flex items-baseline justify-between">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Overall
            </h2>
            <p className="text-[11px] text-mist-400">
              <span className="text-mint-400">solved</span> ·{" "}
              <span className="text-amber-400">in progress</span> ·{" "}
              <span className="text-mist-400">untouched</span>
            </p>
          </div>
          <div className="mt-3">
            <StackedBar total={totals.problems} segments={[
              { value: totals.solved, tone: "bg-mint-500", label: "solved" },
              { value: totals.attempted, tone: "bg-amber-500", label: "in progress" },
              { value: untouched, tone: "bg-ink-750", label: "untouched" },
            ]} />
          </div>
        </div>

        {/* --------------------------------------------------------- tracks */}
        <div className="space-y-5">
          {LEVEL_ORDER.map((level) => {
            const group = byTopic.filter((t) => t.level === level);
            if (group.length === 0) return null;
            const solved = group.reduce((n, t) => n + t.solved, 0);
            const total = group.reduce((n, t) => n + t.total, 0);
            return (
              <section key={level}>
                <div className="mb-3 flex items-center gap-3">
                  <h2 className={`text-[12px] font-bold uppercase tracking-[.14em] ${LEVEL_TONE[level]}`}>
                    {level}
                  </h2>
                  <span className="font-mono text-[11px] text-mist-400">
                    {solved}/{total}
                  </span>
                  <div className="h-px flex-1 bg-white/[.06]" />
                </div>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {group.map((t) => <TrackCard key={t.topic} t={t} />)}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
