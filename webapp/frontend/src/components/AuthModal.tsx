import { useEffect, useRef, useState } from "react";
import { ApiError } from "../lib/api";
import { useAuth } from "../lib/auth";
import { Icon, Spinner } from "./ui";

/** Mirrors the server's rule in auth.check_password, so the UI never lies. */
const MIN_PASSWORD = 8;

function strength(password: string): { score: number; label: string; tone: string } {
  // Deliberately about length and variety rather than a scolding rulebook: the
  // server enforces the one hard rule, and this only tells you where you stand.
  let score = 0;
  if (password.length >= MIN_PASSWORD) score++;
  if (password.length >= 14) score++;
  if (/[a-z]/.test(password) && /[A-Z0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password) || /\s/.test(password)) score++;
  const labels = ["too short", "weak", "fair", "good", "strong"];
  const tones = ["bg-rose-500", "bg-rose-500", "bg-amber-500", "bg-sky-500",
                 "bg-mint-500"];
  return { score, label: labels[score], tone: tones[score] };
}

function Field({
  label, type, value, onChange, autoComplete, placeholder, hint, autoFocus, id,
}: {
  label: string; type: string; value: string; onChange: (v: string) => void;
  autoComplete: string; placeholder?: string; hint?: React.ReactNode;
  autoFocus?: boolean; id: string;
}) {
  return (
    <label htmlFor={id} className="block">
      <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[.1em] text-mist-400">
        {label}
      </span>
      <input
        id={id}
        type={type}
        value={value}
        autoFocus={autoFocus}
        autoComplete={autoComplete}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border border-white/[.09] bg-ink-950/70 px-3 py-2.5
                   text-[13px] text-mist-100 placeholder:text-ink-500
                   focus:border-volt-500/60 focus:outline-none focus:ring-2 focus:ring-volt-500/20"
      />
      {hint && <span className="mt-1.5 block text-[11px] text-mist-400">{hint}</span>}
    </label>
  );
}

export function AuthModal() {
  const { modal, closeModal, openModal, login, register, reason } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const dialog = useRef<HTMLDivElement>(null);

  const isRegister = modal === "register";

  /* Clear transient state whenever the modal opens or switches mode, so a stale
     error from a previous attempt never greets the next one. */
  useEffect(() => {
    setError(null);
    setBusy(false);
    if (modal) setPassword("");
  }, [modal]);

  /* Escape closes; focus is trapped inside so Tab cannot wander behind it. */
  useEffect(() => {
    if (!modal) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); closeModal(); return; }
      if (e.key !== "Tab" || !dialog.current) return;
      const focusable = dialog.current.querySelectorAll<HTMLElement>(
        "input, button, a[href]");
      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      } else if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [modal, closeModal]);

  if (!modal) return null;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    setError(null);
    try {
      if (isRegister) await register(email, password, name || undefined);
      else await login(email, password);
      // On success the provider closes the modal and replays the pending
      // action, so there is nothing to do here.
    } catch (err) {
      setError(err instanceof ApiError ? err.message
               : err instanceof Error ? err.message : "something went wrong");
      setBusy(false);
    }
  };

  const pw = strength(password);
  const canSubmit = email.trim().length > 0 &&
    password.length >= (isRegister ? MIN_PASSWORD : 1);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4"
      role="presentation"
      onMouseDown={(e) => { if (e.target === e.currentTarget) closeModal(); }}
    >
      <div className="absolute inset-0 bg-ink-950/80 backdrop-blur-sm" />

      <div
        ref={dialog}
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-title"
        className="panel animate-fade-up relative w-full max-w-[400px] rounded-2xl
                   px-6 py-6 shadow-panel"
      >
        <button
          onClick={closeModal}
          aria-label="Close"
          className="btn-ghost absolute right-3 top-3 !p-1.5"
        >
          <Icon name="x" className="h-4 w-4" />
        </button>

        <div className="mb-5">
          <div className="mb-3 grid h-9 w-9 place-items-center rounded-xl bg-volt-500 shadow-glow">
            <Icon name="spark" className="h-4.5 w-4.5 text-white" />
          </div>
          <h2 id="auth-title" className="text-[17px] font-bold tracking-tight text-white">
            {isRegister ? "Create your account" : "Sign in to Forge"}
          </h2>
          <p className="mt-1 text-[12.5px] leading-relaxed text-mist-400">
            {reason ?? (isRegister
              ? "Your solutions, streak and notes are saved to your account."
              : "Welcome back — pick up where you left off.")}
          </p>
        </div>

        <form onSubmit={submit} className="space-y-3.5" noValidate>
          {isRegister && (
            <Field
              id="auth-name" label="Name" type="text" value={name}
              onChange={setName} autoComplete="name"
              placeholder="optional"
              hint="Shown in the app. Defaults to your email name."
            />
          )}

          <Field
            id="auth-email" label="Email" type="email" value={email}
            onChange={setEmail} autoComplete="email" autoFocus={!isRegister}
            placeholder="you@example.com"
          />

          <Field
            id="auth-password" label="Password" type="password" value={password}
            onChange={setPassword}
            autoComplete={isRegister ? "new-password" : "current-password"}
            placeholder={isRegister ? `at least ${MIN_PASSWORD} characters` : ""}
          />

          {isRegister && password.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="flex h-1 flex-1 gap-1">
                {[0, 1, 2, 3].map((i) => (
                  <div key={i} className={`h-full flex-1 rounded-full transition-colors ${
                    i < pw.score ? pw.tone : "bg-ink-750"}`} />
                ))}
              </div>
              <span className="w-16 text-right text-[10.5px] text-mist-400">
                {pw.label}
              </span>
            </div>
          )}

          {error && (
            <p role="alert" className="rounded-lg border border-rose-500/25 bg-rose-500/[.08]
                                       px-3 py-2 text-[12px] leading-relaxed text-rose-300">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={busy || !canSubmit}
            className="btn-primary w-full justify-center !py-2.5"
          >
            {busy ? <Spinner /> : <Icon name="check" className="h-4 w-4" />}
            {isRegister ? "Create account" : "Sign in"}
          </button>
        </form>

        <div className="mt-4 border-t border-white/[.06] pt-4 text-center">
          <p className="text-[12px] text-mist-400">
            {isRegister ? "Already have an account?" : "New here?"}{" "}
            <button
              onClick={() => openModal(isRegister ? "login" : "register")}
              className="font-semibold text-volt-300 transition-colors hover:text-volt-400"
            >
              {isRegister ? "Sign in" : "Create one"}
            </button>
          </p>
        </div>

        <p className="mt-3 text-center text-[10.5px] leading-relaxed text-mist-400">
          Runs entirely on your machine — the account lives in
          {" "}<code className="font-mono text-mist-300">backend/data/forge.db</code>{" "}
          and nothing is sent anywhere.
        </p>
      </div>
    </div>
  );
}
