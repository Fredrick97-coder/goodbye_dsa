import { useState } from "react";
import { Link } from "react-router-dom";
import { ApiError, api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { Icon, Spinner } from "./ui";

/**
 * What a learner sees at a gate.
 *
 * It always states the requirement AND offers the way past it. A lock that only
 * says "locked" is hostile; a lock with no override is a cage. The skip is
 * recorded, so the choice belongs to the learner rather than being a loophole.
 */
export function LockedPanel({
  title, reason, courseId, moduleId, onUnlocked, compact = false,
}: {
  title: string;
  reason: string | null;
  courseId: string;
  moduleId: string;
  onUnlocked: () => void;
  compact?: boolean;
}) {
  const { user, requireAuth } = useAuth();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const skip = () => requireAuth(() => void go(), "Sign in to unlock modules.");

  const go = async () => {
    setBusy(true);
    setError(null);
    try {
      await api.unlockModule(courseId, moduleId);
      onUnlocked();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className={`panel rounded-2xl text-center ${compact ? "px-5 py-6" : "px-7 py-9"}`}>
      <div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-amber-500/12">
        <Icon name="lock" className="h-5 w-5 text-amber-400" />
      </div>
      <h2 className={`mt-4 font-bold tracking-tight text-white ${
        compact ? "text-[15px]" : "text-[18px]"}`}>{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-[12.5px] leading-relaxed text-mist-400">
        {reason ?? "Finish the earlier modules to open this one."}
      </p>

      {error && (
        <p className="mx-auto mt-3 max-w-md rounded-lg border border-rose-500/25
                      bg-rose-500/[.07] px-3 py-2 text-[11.5px] text-rose-300">
          {error}
        </p>
      )}

      <div className="mt-5 flex flex-wrap justify-center gap-2">
        <Link to={`/learn/${courseId}`} className="btn-primary">
          <Icon name="book" className="h-4 w-4" /> Back to the course
        </Link>
        {user ? (
          <button onClick={skip} disabled={busy} className="btn-outline">
            {busy ? <Spinner /> : <Icon name="arrowRight" className="h-3.5 w-3.5" />}
            Unlock anyway
          </button>
        ) : (
          <button onClick={skip} className="btn-outline">Sign in</button>
        )}
      </div>

      {user && (
        <p className="mt-3 text-[10.5px] leading-relaxed text-mist-400">
          Already know this material? Skipping is fine and is remembered.
        </p>
      )}
    </div>
  );
}
