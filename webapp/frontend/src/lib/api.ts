import type {
  Activity, Meta, Note, Overview, ProblemDetail, ProblemSummary,
  Submission, SubmitReport,
} from "./types";

// Vite proxies /api to the FastAPI server (see vite.config.ts), so the same
// relative URLs work in dev and in a production build behind one origin.
const BASE = "/api";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `${res.status} ${res.statusText} on ${path}`);
  }
  return res.json() as Promise<T>;
}

const json = (body: unknown): RequestInit => ({
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

/** Drop empty/false filter values so the query string stays readable. */
function qs(params: Record<string, string | number | boolean | undefined | null>) {
  const search = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "" || v === false) continue;
    search.set(k, String(v));
  }
  const s = search.toString();
  return s ? `?${s}` : "";
}

export interface ProblemQuery {
  // An index signature keeps this assignable to qs()'s param type while the
  // named keys still document what the endpoint actually accepts.
  [key: string]: string | number | boolean | undefined | null;
  topic?: number | null;
  difficulty?: string | null;
  tested?: boolean;
  status?: string | null;
  bookmarked?: boolean;
  q?: string;
}

export const api = {
  meta: () => req<Meta>("/meta"),

  problems: (query: ProblemQuery = {}) =>
    req<ProblemSummary[]>(`/problems${qs(query)}`),

  problem: (id: string) => req<ProblemDetail>(`/problems/${id}`),

  random: (difficulty?: string | null, unsolved = true) =>
    req<{ id: string }>(`/problems/random${qs({ difficulty, unsolved })}`),

  submit: (problemId: string, language: string, source: string,
           mode: "test" | "run" = "test") =>
    req<SubmitReport>("/submit", json({ problemId, language, source, mode })),

  submissions: (problemId?: string, limit = 50) =>
    req<Submission[]>(`/submissions${qs({ problemId, limit })}`),

  submission: (id: number) => req<Submission>(`/submissions/${id}`),

  overview: () => req<Overview>("/progress"),

  activity: (days = 365) => req<Activity>(`/activity${qs({ days })}`),

  toggleBookmark: (id: string) =>
    req<{ problemId: string; bookmarked: boolean }>(`/bookmarks/${id}`,
      { method: "POST" }),

  note: (id: string) => req<Note>(`/notes/${id}`),

  saveNote: (id: string, body: string) =>
    req<Note>(`/notes/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ body }),
    }),
};

/**
 * Drafts stay in localStorage on purpose.
 *
 * Unsaved keystrokes are not worth a round trip per character, and losing a
 * draft to a network blip would be worse than losing it to a cache clear.
 * Solved-state, by contrast, is server-side -- see store.py.
 */
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
