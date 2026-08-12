import { useState } from "react";
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useAppData } from "../lib/app-data";
import { useAuth } from "../lib/auth";
import { AccountMenu } from "./AccountMenu";
import { AuthModal } from "./AuthModal";
import { Icon, Spinner } from "./ui";

const NAV = [
  { to: "/", label: "Dashboard", icon: "home" },
  { to: "/learn", label: "Learn", icon: "book" },
  { to: "/problems", label: "Problems", icon: "grid" },
  { to: "/progress", label: "Progress", icon: "chart" },
];

function ApiDown({ message }: { message: string }) {
  return (
    <div className="grid h-full place-items-center px-6">
      <div className="panel max-w-md rounded-2xl px-6 py-6 text-center">
        <div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-rose-500/12">
          <Icon name="x" className="h-5 w-5 text-rose-400" />
        </div>
        <h1 className="mt-4 text-base font-bold text-white">API unreachable</h1>
        <p className="mt-2 text-[12.5px] leading-relaxed text-mist-300">{message}</p>
        <pre className="mt-4 overflow-x-auto rounded-lg bg-ink-950/70 px-3 py-2.5 text-left font-mono text-[11.5px] text-mist-300">
{`cd webapp
./dev.sh`}
        </pre>
      </div>
    </div>
  );
}

export function Shell() {
  const { meta, problems, loading, error } = useAppData();
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [picking, setPicking] = useState(false);

  const solved = problems.filter((p) => p.status === "solved").length;

  const pickRandom = async () => {
    setPicking(true);
    try {
      const { id } = await api.random();
      navigate(`/problems/${id}`);
    } catch { /* nothing matched; the button simply does nothing */ }
    finally { setPicking(false); }
  };

  if (error) return <ApiDown message={error} />;
  // Waiting for /auth/me too, so the navbar never flashes "Log in" for someone
  // who is already signed in.
  if (loading || authLoading || !meta) {
    return (
      <div className="grid h-full place-items-center">
        <Spinner className="h-6 w-6 text-volt-400" />
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col overflow-hidden">
      <header className="z-30 flex h-14 shrink-0 items-center gap-2 border-b border-white/[.06]
                         bg-ink-900/80 px-4 backdrop-blur-xl">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="grid h-7 w-7 place-items-center rounded-lg bg-volt-500 shadow-glow">
            <Icon name="spark" className="h-4 w-4 text-white" />
          </div>
          <div className="leading-none">
            <p className="text-[13.5px] font-bold tracking-tight text-white">Forge</p>
            <p className="mt-0.5 text-[10px] text-mist-400">DSA practice</p>
          </div>
        </Link>

        <nav className="ml-4 flex items-center gap-0.5">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-lg px-3 py-1.5 text-[12.5px] font-semibold transition-colors ${
                  isActive ? "bg-white/[.07] text-white" : "text-mist-400 hover:text-mist-100"
                }`}
            >
              <Icon name={item.icon} className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          {user && (
            <div className="mr-1 hidden items-center gap-1.5 md:flex">
              <Icon name="trophy" className="h-3.5 w-3.5 text-mint-400" />
              <span className="font-mono text-[12px] text-mist-300">
                {solved}<span className="text-mist-400">/{meta.stats.problems}</span>
              </span>
            </div>
          )}
          <button onClick={() => void pickRandom()} className="btn-outline !py-1.5"
                  title="Jump to a random unsolved problem">
            {picking ? <Spinner /> : <Icon name="dice" className="h-3.5 w-3.5" />}
            <span className="hidden sm:inline">Random</span>
          </button>
          <div className="ml-1 h-6 w-px bg-white/[.08]" />
          <AccountMenu />
        </div>
      </header>

      <main className="min-h-0 flex-1">
        <Outlet />
      </main>

      {/* One modal for the whole app, so any page can call requireAuth. */}
      <AuthModal />
    </div>
  );
}
