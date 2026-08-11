import {
  createContext, useCallback, useContext, useEffect, useMemo, useState,
} from "react";
import { api } from "./api";
import { useAuth } from "./auth";
import type { Meta, ProblemSummary } from "./types";

/**
 * Meta and the full problem list, fetched once and shared by every page.
 *
 * All 342 problems arrive in one request (~90 KB) and every page filters them
 * in memory. That makes filter changes and search instant, and it means a page
 * transition never shows a spinner for data the app already has.
 */
interface AppData {
  meta: Meta | null;
  problems: ProblemSummary[];
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
  patch: (id: string, changes: Partial<ProblemSummary>) => void;
  byId: Map<string, ProblemSummary>;
}

const Ctx = createContext<AppData | null>(null);

export function AppDataProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [meta, setMeta] = useState<Meta | null>(null);
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [m, list] = await Promise.all([api.meta(), api.problems()]);
      setMeta(m);
      setProblems(list);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "could not reach the API");
    } finally {
      setLoading(false);
    }
  }, []);

  // Refetch when the signed-in account changes. The list carries per-user
  // status, bookmarks and notes, so signing in or out has to re-pull it --
  // otherwise one account's ticks stay on screen for the next.
  useEffect(() => { void refresh(); }, [refresh, user?.id]);

  /**
   * Update one row without refetching the list.
   *
   * A bookmark toggle or a fresh Accepted only changes a single problem, and
   * re-pulling all 342 rows would make the star flicker.
   */
  const patch = useCallback((id: string, changes: Partial<ProblemSummary>) => {
    setProblems((prev) => prev.map((p) => (p.id === id ? { ...p, ...changes } : p)));
  }, []);

  const byId = useMemo(
    () => new Map(problems.map((p) => [p.id, p])), [problems],
  );

  const value = useMemo<AppData>(
    () => ({ meta, problems, loading, error, refresh, patch, byId }),
    [meta, problems, loading, error, refresh, patch, byId],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAppData(): AppData {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAppData must be used inside AppDataProvider");
  return ctx;
}
