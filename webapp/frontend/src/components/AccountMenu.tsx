import { useEffect, useRef, useState } from "react";
import { ApiError, auth as authApi } from "../lib/api";
import { useAuth } from "../lib/auth";
import { Icon, Spinner } from "./ui";

function initials(name: string): string {
  const parts = name.trim().split(/[\s._-]+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

/** Change-password form, shown inside the menu rather than on its own page. */
function PasswordForm({ onDone }: { onDone: (message: string) => void }) {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await authApi.changePassword(current, next);
      onDone(res.otherSessionsEnded > 0
        ? `Password changed. ${res.otherSessionsEnded} other session${
            res.otherSessionsEnded === 1 ? "" : "s"} signed out.`
        : "Password changed.");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "could not change it");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-2 px-3 pb-3">
      <input
        type="password" value={current} onChange={(e) => setCurrent(e.target.value)}
        placeholder="current password" autoComplete="current-password"
        className="w-full rounded-lg border border-white/[.08] bg-ink-950/70 px-2.5 py-2
                   text-[12px] text-mist-100 placeholder:text-ink-500
                   focus:border-volt-500/50 focus:outline-none"
      />
      <input
        type="password" value={next} onChange={(e) => setNext(e.target.value)}
        placeholder="new password (8+ characters)" autoComplete="new-password"
        className="w-full rounded-lg border border-white/[.08] bg-ink-950/70 px-2.5 py-2
                   text-[12px] text-mist-100 placeholder:text-ink-500
                   focus:border-volt-500/50 focus:outline-none"
      />
      {error && <p className="text-[11px] text-rose-300">{error}</p>}
      <button type="submit" disabled={busy || next.length < 8}
              className="btn-primary w-full justify-center !py-1.5 !text-[12px]">
        {busy ? <Spinner className="h-3.5 w-3.5" /> : null}
        Change password
      </button>
      <p className="text-[10.5px] leading-relaxed text-mist-400">
        Signs out every other device, which is the point of changing it.
      </p>
    </form>
  );
}

export function AccountMenu() {
  const { user, logout, openModal } = useAuth();
  const [open, setOpen] = useState(false);
  const [panel, setPanel] = useState<"menu" | "password">("menu");
  const [flash, setFlash] = useState<string | null>(null);
  const wrap = useRef<HTMLDivElement>(null);

  /* Close on outside click and on Escape -- a menu that only closes by clicking
     the trigger again feels broken. */
  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (wrap.current && !wrap.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  useEffect(() => {
    if (!open) { setPanel("menu"); setFlash(null); }
  }, [open]);

  if (!user) {
    return (
      <div className="flex items-center gap-2">
        <button onClick={() => openModal("login")} className="btn-ghost !py-1.5 text-[12.5px]">
          Log in
        </button>
        <button onClick={() => openModal("register")} className="btn-primary !py-1.5 text-[12.5px]">
          Sign up
        </button>
      </div>
    );
  }

  return (
    <div ref={wrap} className="relative">
      <button
        onClick={() => setOpen(!open)}
        aria-haspopup="menu"
        aria-expanded={open}
        className={`flex items-center gap-2 rounded-lg py-1 pl-1 pr-2 transition-colors ${
          open ? "bg-white/[.07]" : "hover:bg-white/[.05]"}`}
      >
        <span className="grid h-7 w-7 place-items-center rounded-lg bg-gradient-to-br
                         from-volt-500 to-sky-500 text-[11px] font-bold text-white">
          {initials(user.name)}
        </span>
        <span className="hidden max-w-[110px] truncate text-[12.5px] font-medium text-mist-200 sm:block">
          {user.name}
        </span>
        <Icon name="chevron" className={`h-3 w-3 text-mist-400 transition-transform ${
          open ? "rotate-180" : ""}`} />
      </button>

      {open && (
        <div role="menu"
             className="animate-fade-up absolute right-0 top-full z-50 mt-2 w-[268px]
                        overflow-hidden rounded-xl border border-white/[.08]
                        bg-ink-850 shadow-panel">
          <div className="border-b border-white/[.06] px-3.5 py-3">
            <p className="truncate text-[13px] font-semibold text-white">{user.name}</p>
            <p className="truncate text-[11.5px] text-mist-400">{user.email}</p>
          </div>

          {flash && (
            <p className="border-b border-white/[.06] bg-mint-500/[.08] px-3.5 py-2
                          text-[11.5px] leading-relaxed text-mint-400">
              {flash}
            </p>
          )}

          {panel === "menu" ? (
            <div className="p-1.5">
              <button
                onClick={() => setPanel("password")}
                className="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left
                           text-[12.5px] text-mist-200 transition-colors hover:bg-white/[.05]"
              >
                <Icon name="reset" className="h-3.5 w-3.5 text-mist-400" />
                Change password
              </button>
              <button
                onClick={async () => {
                  const res = await authApi.logoutEverywhere();
                  setFlash(res.otherSessionsEnded > 0
                    ? `Signed out ${res.otherSessionsEnded} other session${
                        res.otherSessionsEnded === 1 ? "" : "s"}.`
                    : "No other sessions were open.");
                }}
                className="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left
                           text-[12.5px] text-mist-200 transition-colors hover:bg-white/[.05]"
              >
                <Icon name="history" className="h-3.5 w-3.5 text-mist-400" />
                Sign out other devices
              </button>
              <div className="my-1.5 h-px bg-white/[.06]" />
              <button
                onClick={() => { setOpen(false); void logout(); }}
                className="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left
                           text-[12.5px] text-rose-400 transition-colors hover:bg-rose-500/[.08]"
              >
                <Icon name="x" className="h-3.5 w-3.5" />
                Log out
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={() => setPanel("menu")}
                className="flex w-full items-center gap-2 px-3.5 py-2 text-left text-[11.5px]
                           text-mist-400 transition-colors hover:text-mist-200"
              >
                <Icon name="arrowLeft" className="h-3 w-3" /> back
              </button>
              <PasswordForm onDone={(m) => { setFlash(m); setPanel("menu"); }} />
            </>
          )}
        </div>
      )}
    </div>
  );
}
