import {
  createContext, useCallback, useContext, useEffect, useMemo, useRef, useState,
} from "react";
import {
  auth as authApi, drafts, localPrefs, setUnauthorizedHandler,
} from "./api";
import type { Preferences, User } from "./types";

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

const DEFAULT_PREFS: Preferences = { language: "python" };

interface AuthState {
  user: User | null;
  /** Per-account settings; defaults while signed out. */
  preferences: Preferences;
  /**
   * Persist one preference. Signed in it goes to the database, signed out to
   * localStorage, so the picker behaves the same either way.
   */
  setPreference: <K extends keyof Preferences>(
    key: K, value: Preferences[K]) => void;
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
  const [preferences, setPreferences] = useState<Preferences>(
    () => ({ ...DEFAULT_PREFS, ...localPrefs.load() }));
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState<"login" | "register" | null>(null);
  const [reason, setReason] = useState<string | null>(null);
  const pending = useRef<PendingAction>(null);

  /* ---------------------------------------------------- boot: who is this? */
  useEffect(() => {
    let alive = true;
    void (async () => {
      try {
        const { user: me, preferences: server } = await authApi.me();
        if (!alive) return;
        setUserState(me);
        // Only an ACCOUNT's preferences override what is already loaded from
        // localStorage. Signed out the server just echoes defaults, and taking
        // those was overwriting the visitor's own choice on every page load.
        if (me && server) setPreferences({ ...DEFAULT_PREFS, ...server });
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

  /**
   * Reconcile local and server preferences at sign-in.
   *
   * The account wins, except where it has never chosen: someone who picked
   * TypeScript and *then* signed up should not be dropped back to Python.
   */
  const mergePrefs = useCallback(async (server?: Preferences) => {
    const local = localPrefs.load();
    const merged: Preferences = { ...DEFAULT_PREFS, ...server };
    const pushable: Partial<Preferences> = {};
    for (const key of Object.keys(DEFAULT_PREFS) as (keyof Preferences)[]) {
      const chosenLocally = local[key];
      if (chosenLocally && merged[key] === DEFAULT_PREFS[key]
          && chosenLocally !== merged[key]) {
        merged[key] = chosenLocally as Preferences[typeof key];
        pushable[key] = chosenLocally as Preferences[typeof key];
      }
    }
    setPreferences(merged);
    if (Object.keys(pushable).length > 0) {
      // Fire and forget: a failure here costs a preference, not the sign-in.
      try { await authApi.savePreferences(pushable); } catch { /* ignore */ }
    }
  }, []);

  const finishAuth = useCallback((next: User, server?: Preferences) => {
    adopt(next);
    void mergePrefs(server);
    setModal(null);
    setReason(null);
    // Run whatever the visitor was trying to do when they hit the gate. The
    // ref is cleared first so a failing action cannot re-fire it.
    const action = pending.current;
    pending.current = null;
    action?.();
  }, [adopt, mergePrefs]);

  const login = useCallback(async (email: string, password: string) => {
    const { user: next, preferences: server } = await authApi.login(email, password);
    finishAuth(next, server);
  }, [finishAuth]);

  const register = useCallback(async (email: string, password: string,
                                      name?: string) => {
    const { user: next, preferences: server } =
      await authApi.register(email, password, name);
    finishAuth(next, server);
  }, [finishAuth]);

  const logout = useCallback(async () => {
    try { await authApi.logout(); } finally {
      setUserState(null);
      pending.current = null;
      // The signed-out session keeps the same choice rather than snapping back
      // to Python, which would look like the app forgetting.
      localPrefs.save(preferences);
    }
  }, [preferences]);

  const setPreference = useCallback(<K extends keyof Preferences>(
    key: K, value: Preferences[K],
  ) => {
    setPreferences((prev) => {
      if (prev[key] === value) return prev;
      const next = { ...prev, [key]: value };
      localPrefs.save(next);
      return next;
    });
    if (user) {
      // Fire and forget. The UI has already moved; a failed save means the
      // choice is not remembered next session, which is not worth a dialog.
      void authApi.savePreferences({ [key]: value } as Partial<Preferences>)
        .catch(() => {});
    }
  }, [user]);

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
    user, preferences, setPreference, loading, modal, openModal, closeModal,
    requireAuth, reason, login, register, logout, setUser: setUserState,
  }), [user, preferences, setPreference, loading, modal, openModal, closeModal,
       requireAuth, reason, login, register, logout]);

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
