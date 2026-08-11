import {
  createContext, useCallback, useContext, useEffect, useMemo, useRef, useState,
} from "react";
import { auth as authApi, drafts, setUnauthorizedHandler } from "./api";
import type { User } from "./types";

/**
 * Who is signed in, and the one place that changes.
 *
 * The session itself lives in an HttpOnly cookie the browser cannot read, so
 * this context is not the source of truth -- the server is. What it holds is the
 * answer the server last gave, refreshed on boot and after every auth action,
 * plus a `requireAuth` gate that any action can await.
 */

/** A gated action: what to run once the visitor is signed in. */
type PendingAction = (() => void) | null;

interface AuthState {
  user: User | null;
  /** Still asking the server who this is. Guards a signed-out flash on reload. */
  loading: boolean;
  modal: "login" | "register" | null;
  openModal: (mode: "login" | "register") => void;
  closeModal: () => void;
  /**
   * Run `action` if signed in; otherwise open the modal and run it after a
   * successful sign-in. Returns true when it ran immediately.
   */
  requireAuth: (action: () => void, reason?: string) => boolean;
  reason: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  setUser: (user: User) => void;
}

const Ctx = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUserState] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState<"login" | "register" | null>(null);
  const [reason, setReason] = useState<string | null>(null);
  const pending = useRef<PendingAction>(null);

  /* ---------------------------------------------------- boot: who is this? */
  useEffect(() => {
    let alive = true;
    void (async () => {
      try {
        const { user: me } = await authApi.me();
        if (!alive) return;
        setUserState(me);
        if (me) drafts.adopt(me.id);
      } catch {
        if (alive) setUserState(null);      // API down: treat as signed out
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  /* A session that expires mid-visit drops the UI to signed-out immediately,
     rather than leaving a stale name in the navbar and failing every action. */
  useEffect(() => {
    setUnauthorizedHandler(() => {
      setUserState(null);
      pending.current = null;
    });
    return () => setUnauthorizedHandler(null);
  }, []);

  const adopt = useCallback((next: User) => {
    drafts.adopt(next.id);
    setUserState(next);
  }, []);

  const finishAuth = useCallback((next: User) => {
    adopt(next);
    setModal(null);
    setReason(null);
    // Run whatever the visitor was trying to do when they hit the gate. The
    // ref is cleared first so a failing action cannot re-fire it.
    const action = pending.current;
    pending.current = null;
    action?.();
  }, [adopt]);

  const login = useCallback(async (email: string, password: string) => {
    const { user: next } = await authApi.login(email, password);
    finishAuth(next);
  }, [finishAuth]);

  const register = useCallback(async (email: string, password: string,
                                      name?: string) => {
    const { user: next } = await authApi.register(email, password, name);
    finishAuth(next);
  }, [finishAuth]);

  const logout = useCallback(async () => {
    try { await authApi.logout(); } finally {
      setUserState(null);
      pending.current = null;
    }
  }, []);

  const openModal = useCallback((mode: "login" | "register") => {
    setModal(mode);
  }, []);

  const closeModal = useCallback(() => {
    setModal(null);
    setReason(null);
    pending.current = null;    // dismissing the modal abandons the action
  }, []);

  const requireAuth = useCallback((action: () => void, why?: string) => {
    if (user) { action(); return true; }
    pending.current = action;
    setReason(why ?? null);
    setModal("login");
    return false;
  }, [user]);

  const value = useMemo<AuthState>(() => ({
    user, loading, modal, openModal, closeModal, requireAuth, reason,
    login, register, logout, setUser: setUserState,
  }), [user, loading, modal, openModal, closeModal, requireAuth, reason,
       login, register, logout]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}

/** The localStorage namespace for the current viewer's drafts. */
export function draftOwner(user: User | null): string {
  return user ? user.id : drafts.ANON;
}
