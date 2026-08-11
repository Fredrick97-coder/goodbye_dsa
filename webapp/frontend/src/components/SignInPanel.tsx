import { useAuth } from "../lib/auth";
import { Icon } from "./ui";

/**
 * What a signed-out visitor sees where their own data would be.
 *
 * Deliberately not a wall: the copy says what an account gets you, and the
 * problem set stays one click away, because browsing is the thing that makes
 * someone want an account in the first place.
 */
export function SignInPanel({
  title, blurb, bullets,
}: { title: string; blurb: string; bullets: string[] }) {
  const { openModal } = useAuth();
  return (
    <div className="panel mx-auto mt-10 max-w-lg rounded-2xl px-7 py-7 text-center">
      <div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-volt-500 shadow-glow">
        <Icon name="spark" className="h-5 w-5 text-white" />
      </div>
      <h1 className="mt-4 text-[19px] font-bold tracking-tight text-white">{title}</h1>
      <p className="mx-auto mt-2 max-w-sm text-[13px] leading-relaxed text-mist-400">
        {blurb}
      </p>

      <ul className="mx-auto mt-5 max-w-xs space-y-2 text-left">
        {bullets.map((b) => (
          <li key={b} className="flex gap-2.5 text-[12.5px] leading-relaxed text-mist-300">
            <Icon name="check" className="mt-0.5 h-3.5 w-3.5 shrink-0 text-mint-400" />
            {b}
          </li>
        ))}
      </ul>

      <div className="mt-6 flex flex-wrap justify-center gap-2">
        <button onClick={() => openModal("register")} className="btn-primary">
          Create an account
        </button>
        <button onClick={() => openModal("login")} className="btn-outline">
          I already have one
        </button>
      </div>

      <p className="mt-4 text-[11px] leading-relaxed text-mist-400">
        Everything stays on this machine — the account lives in{" "}
        <code className="font-mono text-mist-300">backend/data/forge.db</code>.
      </p>
    </div>
  );
}
