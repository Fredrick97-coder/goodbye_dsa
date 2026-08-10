import type { Meta, ProblemDetail, ProblemSummary, SubmitReport } from "./types";

// Vite proxies /api to the FastAPI server (see vite.config.ts), so the same
// relative URLs work in dev and in a production build behind one origin.
const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} on ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  meta: () => get<Meta>("/meta"),
  problems: () => get<ProblemSummary[]>("/problems"),
  problem: (id: string) => get<ProblemDetail>(`/problems/${id}`),

  async submit(
    problemId: string,
    language: string,
    source: string,
    mode: "test" | "run" = "test",
  ): Promise<SubmitReport> {
    const res = await fetch(`${BASE}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problemId, language, source, mode }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(body.detail ?? `HTTP ${res.status}`);
    }
    return res.json();
  },
};

/** Drafts live in localStorage so a refresh never loses work. */
export const drafts = {
  key: (problemId: string, lang: string) => `forge:draft:${problemId}:${lang}`,
  load(problemId: string, lang: string): string | null {
    try { return localStorage.getItem(this.key(problemId, lang)); }
    catch { return null; }
  },
  save(problemId: string, lang: string, source: string) {
    try { localStorage.setItem(this.key(problemId, lang), source); } catch { /* quota */ }
  },
  clear(problemId: string, lang: string) {
    try { localStorage.removeItem(this.key(problemId, lang)); } catch { /* ignore */ }
  },
};

/** Solved-state is local for now; it moves server-side with auth. */
export const progress = {
  KEY: "forge:solved",
  all(): Record<string, { at: number; ms: number }> {
    try { return JSON.parse(localStorage.getItem(this.KEY) ?? "{}"); }
    catch { return {}; }
  },
  mark(problemId: string, ms: number) {
    const all = this.all();
    all[problemId] = { at: Date.now(), ms };
    try { localStorage.setItem(this.KEY, JSON.stringify(all)); } catch { /* ignore */ }
  },
};
