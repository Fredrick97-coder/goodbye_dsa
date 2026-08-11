import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Heatmap } from "../components/Heatmap";
import {
  Bar, DifficultyText, Empty, Icon, Ring, Spinner, StatCard, VerdictPill,
} from "../components/ui";
import { SignInPanel } from "../components/SignInPanel";
import { api } from "../lib/api";
import { useAppData } from "../lib/app-data";
import { useAuth } from "../lib/auth";
import { DIFF_BG, pct, pctLabel, timestamp } from "../lib/format";
import type { Overview, Submission } from "../lib/types";

export default function Progress() {
  const { byId } = useAppData();
  const { user } = useAuth();
  const [data, setData] = useState<Overview | null>(null);
  const [history, setHistory] = useState<Submission[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) { setData(null); return; }
    const ac = new AbortController();
    void (async () => {
      try {
        const [overview, subs] = await Promise.all([
          api.overview(ac.signal), api.submissions(undefined, 200, ac.signal),
        ]);
        setData(overview);
        setHistory(subs);
      } catch (err) {
        if (ac.signal.aborted) return;
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => ac.abort();
  }, [user]);

  if (!user)
    return (
      <div className="scroll-thin h-full overflow-y-auto px-5 py-6">
        <SignInPanel
          title="Your progress lives in your account"
          blurb="Streaks, the activity heatmap and your full submission history are built from real graded submissions, so they need somewhere to live."
          bullets={[
            "A 12-month activity heatmap",
            "Current and longest streak",
            "Progress by difficulty and by topic",
            "Every submission, with its verdict and your code",
          ]}
        />
      </div>
    );

  if (error) return <Empty icon="x" title="Could not load progress" hint={error} />;
  if (!data)
    return <div className="grid h-full place-items-center"><Spinner className="h-6 w-6 text-volt-400" /></div>;

  const { totals, byDifficulty, byTopic, activity } = data;
  const accepted = history.filter((h) => h.verdict === "accepted").length;

  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl space-y-6 px-5 py-6">
        <div>
          <h1 className="text-[21px] font-bold tracking-tight text-white">Progress</h1>
          <p className="mt-1 text-[12.5px] text-mist-400">
            Everything here comes from real graded submissions stored on the
            server — clearing the browser will not change it.
          </p>
        </div>

        {/* ------------------------------------------------------ top stats */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard icon="trophy" label="Solved" tone="text-mint-400"
                    value={`${totals.solved}`}
                    sub={`${pctLabel(totals.solved, totals.problems)} of ${totals.problems}`} />
          <StatCard icon="history" label="Submissions" tone="text-sky-400"
                    value={activity.totalSubmissions}
                    sub={history.length ? `${pct(accepted, history.length)}% accepted (last ${history.length})` : "none yet"} />
          <StatCard icon="flame" label="Streak" tone="text-amber-400"
                    value={`${activity.streak}d`} sub={`longest ${activity.longestStreak}d`} />
          <StatCard icon="grid" label="In progress" tone="text-volt-300"
                    value={totals.attempted} sub="attempted, not yet solved" />
        </div>

        {/* ------------------------------------------------------- heatmap */}
        <div className="panel rounded-2xl px-5 py-4">
          <div className="mb-4 flex items-baseline justify-between">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Activity
            </h2>
            <p className="text-[11px] text-mist-400">
              {activity.activeDays} active {activity.activeDays === 1 ? "day" : "days"}
              {" · last 12 months"}
            </p>
          </div>
          {activity.days.length === 0 ? (
            <p className="py-6 text-center text-[12.5px] text-mist-400">
              No submissions yet — the grid fills in as you solve.
            </p>
          ) : <Heatmap days={activity.days} weeks={52} />}
        </div>

        {/* --------------------------------------------- rings + difficulty */}
        <div className="grid gap-4 lg:grid-cols-[auto_minmax(0,1fr)]">
          <div className="panel grid place-items-center rounded-2xl px-8 py-6">
            <Ring solved={totals.solved} total={totals.problems} size={150} />
          </div>
          <div className="panel rounded-2xl px-5 py-4">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              By difficulty
            </h2>
            <div className="mt-4 space-y-4">
              {byDifficulty.map((d) => (
                <div key={d.difficulty}>
                  <div className="flex items-baseline justify-between">
                    <DifficultyText value={d.difficulty} />
                    <span className="font-mono text-[11.5px] text-mist-300">
                      {d.solved}<span className="text-mist-400">/{d.total}</span>
                      <span className="ml-2 text-mist-400">{pct(d.solved, d.total)}%</span>
                    </span>
                  </div>
                  <Bar value={d.solved} total={d.total} tone={DIFF_BG[d.difficulty]}
                       className="mt-1.5 h-1.5" />
                  {d.attempted > 0 && (
                    <p className="mt-1 text-[10.5px] text-amber-400/80">
                      {d.attempted} attempted but not solved
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------- topic table */}
        <div className="panel overflow-hidden rounded-2xl">
          <div className="border-b border-white/[.06] px-5 py-3">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              By topic
            </h2>
          </div>
          {byTopic.map((t) => (
            <Link key={t.topic} to={`/problems?topic=${t.topic}`}
                  className="grid grid-cols-[34px_minmax(0,1fr)_120px_54px] items-center gap-3
                             border-b border-white/[.035] px-5 py-2.5 transition-colors
                             hover:bg-white/[.025]">
              <span className="font-mono text-[11px] text-mist-400">
                {String(t.topic).padStart(2, "0")}
              </span>
              <span className="truncate text-[12.5px] text-mist-100">{t.name}</span>
              <div className="flex items-center gap-2">
                <Bar value={t.solved} total={t.total}
                     tone={t.solved === t.total ? "bg-mint-500" : "bg-volt-500"} className="h-1" />
              </div>
              <span className="text-right font-mono text-[11px] text-mist-300">
                {t.solved}/{t.total}
              </span>
            </Link>
          ))}
        </div>

        {/* ------------------------------------------------------- history */}
        <div className="panel overflow-hidden rounded-2xl">
          <div className="flex items-baseline justify-between border-b border-white/[.06] px-5 py-3">
            <h2 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
              Submission history
            </h2>
            <p className="text-[11px] text-mist-400">most recent {history.length}</p>
          </div>
          {history.length === 0 ? (
            <p className="px-5 py-10 text-center text-[12.5px] text-mist-400">
              Nothing yet. Graded submissions land here; pressing Run does not
              count, and neither does submitting untouched starter code.
            </p>
          ) : history.map((h) => {
            const p = byId.get(h.problemId);
            return (
              <Link key={h.id} to={`/problems/${h.problemId}`}
                    className="grid grid-cols-[130px_minmax(0,1fr)_60px_70px_auto] items-center gap-3
                               border-b border-white/[.035] px-5 py-2.5 transition-colors
                               hover:bg-white/[.025]">
                <VerdictPill verdict={h.verdict} />
                <span className="min-w-0 truncate text-[12.5px] text-mist-200">
                  <span className="mr-2 font-mono text-[10.5px] text-mist-400">{h.problemId}</span>
                  {p?.title ?? h.problemId}
                </span>
                <span className="font-mono text-[11px] text-mist-300">{h.passed}/{h.total}</span>
                <span className="font-mono text-[11px] text-mist-400">
                  {Math.round(h.elapsedMs)} ms
                </span>
                <span className="flex items-center gap-1.5 text-right text-[11px] text-mist-400">
                  <Icon name="clock" className="h-3 w-3" />{timestamp(h.createdAt)}
                </span>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
