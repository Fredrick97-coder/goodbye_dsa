import type {
  Activity, Meta, Note, Overview, ProblemDetail, ProblemSummary,
  Submission, SubmitReport, User,
} from "./types";

// Vite proxies /api to the FastAPI server (see vite.config.ts), so the same
// relative URLs work in dev and in a production build behind one origin.
const BASE = "/api";

/**
 * An HTTP failure that keeps its status code.
 *
 * The UI has to tell "you are not signed in" apart from "that went wrong", so
 * the status has to survive being thrown -- a bare Error with a message would
 * force the caller to string-match.
 */
export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
  get isUnauthorized() { return this.status === 401; }
}

/** Notified whenever the server says the session is gone. */
type UnauthorizedHandler = () => void;
let onUnauthorized: UnauthorizedHandler | null = null;
export function setUnauthorizedHandler(fn: UnauthorizedHandler | null) {
  onUnauthorized = fn;
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  // `credentials: same-origin` is the default, and the session cookie rides on
  // it; Vite proxies /api so the browser really is same-origin here.
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const message = body?.detail ?? `${res.status} ${res.statusText} on ${path}`;
    if (res.status === 401 && !path.startsWith("/auth/")) {
      // A session that expired mid-visit should drop the UI to signed-out
      // rather than leave a stale name in the navbar.
      onUnauthorized?.();
    }
    throw new ApiError(res.status, message);
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

export const auth = {
  me: () => req<{ user: User | null; sessions?: number }>("/auth/me"),

  register: (email: string, password: string, name?: string) =>
    req<{ user: User }>("/auth/register", json({ email, password, name })),

  login: (email: string, password: string) =>
    req<{ user: User }>("/auth/login", json({ email, password })),

  logout: () => req<{ ok: boolean }>("/auth/logout", { method: "POST" }),

  changeName: (name: string) =>
    req<{ user: User }>("/auth/name", json({ name })),

  changePassword: (currentPassword: string, newPassword: string) =>
    req<{ ok: boolean; otherSessionsEnded: number }>(
      "/auth/password", json({ currentPassword, newPassword })),

  logoutEverywhere: () =>
    req<{ ok: boolean; otherSessionsEnded: number }>(
      "/auth/logout-everywhere", { method: "POST" }),
};

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

  submissions: (problemId?: string, limit = 50, signal?: AbortSignal) =>
    req<Submission[]>(`/submissions${qs({ problemId, limit })}`, { signal }),

  submission: (id: number) => req<Submission>(`/submissions/${id}`),

  overview: (signal?: AbortSignal) => req<Overview>("/progress", { signal }),

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
 *
 * Keys are namespaced by account so two people sharing a browser profile do not
 * read each other's half-written solutions. Work done before signing in lives
 * under `anon` and is copied across on sign-in, so the code you typed while the
 * sign-in modal was open is never lost.
 */
const ANON = "anon";

export const drafts = {
  key: (owner: string, problemId: string, lang: string) =>
    `forge:draft:${owner}:${problemId}:${lang}`,

  load(owner: string, problemId: string, lang: string): string | null {
    try {
      const mine = localStorage.getItem(this.key(owner, problemId, lang));
      if (mine !== null) return mine;
      // Fall back to anything typed before signing in.
      return owner === ANON
        ? null
        : localStorage.getItem(this.key(ANON, problemId, lang));
    } catch { return null; }
  },

  save(owner: string, problemId: string, lang: string, source: string) {
    try { localStorage.setItem(this.key(owner, problemId, lang), source); }
    catch { /* quota */ }
  },

  clear(owner: string, problemId: string, lang: string) {
    try { localStorage.removeItem(this.key(owner, problemId, lang)); }
    catch { /* ignore */ }
  },

  /** Copy the anonymous buffers into an account's namespace after sign-in. */
  adopt(owner: string) {
    if (owner === ANON) return;
    try {
      const prefix = `forge:draft:${ANON}:`;
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (!k?.startsWith(prefix)) continue;
        const target = `forge:draft:${owner}:${k.slice(prefix.length)}`;
        if (localStorage.getItem(target) === null) {
          localStorage.setItem(target, localStorage.getItem(k) ?? "");
        }
      }
    } catch { /* ignore */ }
  },

  ANON,
};
