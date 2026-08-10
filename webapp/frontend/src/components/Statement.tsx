import { useState } from "react";
import type { ProblemDetail } from "../lib/types";
import { DifficultyBadge, Icon } from "./ui";

/** Renders `code`, **bold** and arrows from the plain-text problem fields. */
function RichText({ text }: { text: string }) {
  const withArrows = text.replace(/->/g, "→");
  const parts = withArrows.split(/(`[^`]+`|\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith("`") && part.endsWith("`"))
          return <code key={i}>{part.slice(1, -1)}</code>;
        if (part.startsWith("**") && part.endsWith("**"))
          return <strong key={i}>{part.slice(2, -2)}</strong>;
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <h3 className="text-[10px] font-bold uppercase tracking-[.14em] text-mist-400">
        {label}
      </h3>
      <div className="statement">{children}</div>
    </div>
  );
}

function Collapsible({
  label, count, children, defaultOpen = false,
}: { label: string; count?: number; children: React.ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="overflow-hidden rounded-xl border border-white/[.06] bg-ink-850/60">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-2 px-3.5 py-2.5 text-left text-xs font-semibold
                   text-mist-200 transition-colors hover:bg-white/[.03]"
      >
        <Icon name="chevron" className={`h-3.5 w-3.5 text-mist-400 transition-transform ${open ? "" : "-rotate-90"}`} />
        {label}
        {count !== undefined && (
          <span className="ml-auto rounded-md bg-ink-750 px-1.5 py-0.5 font-mono text-[10px] text-mist-400">
            {count}
          </span>
        )}
      </button>
      {open && <div className="border-t border-white/[.06] px-3.5 py-3">{children}</div>}
    </div>
  );
}

export function Statement({ problem }: { problem: ProblemDetail }) {
  return (
    <div className="scroll-thin h-full overflow-y-auto">
      <div className="animate-fade-up space-y-6 px-6 py-5">
        {/* header */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-[11px] font-medium text-mist-400">
            <span className="font-mono">{problem.id}</span>
            <span className="text-ink-600">/</span>
            <span>{problem.topicName}</span>
          </div>
          <h1 className="text-[22px] font-bold leading-tight tracking-tight text-white">
            {problem.title}
          </h1>
          <div className="flex flex-wrap items-center gap-2">
            <DifficultyBadge value={problem.difficulty} />
            {problem.tested ? (
              <span className="chip bg-sky-500/10 text-sky-400 ring-1 ring-sky-500/25">
                <Icon name="flask" className="h-3 w-3" />
                {problem.testCount} reference {problem.testCount === 1 ? "test" : "tests"}
              </span>
            ) : (
              <span className="chip bg-ink-750 text-mist-400 ring-1 ring-white/10">
                manual check only
              </span>
            )}
          </div>
        </div>

        {/* body */}
        {problem.inputDesc && (
          <Section label="Input"><RichText text={problem.inputDesc} /></Section>
        )}
        {problem.outputDesc && (
          <Section label="Output"><RichText text={problem.outputDesc} /></Section>
        )}

        {problem.example && (
          <Section label="Example">
            <pre className="scroll-thin overflow-x-auto rounded-xl border border-white/[.06]
                            bg-ink-950/60 px-4 py-3 font-mono text-[12.5px] leading-relaxed text-mint-400">
{problem.example.replace(/->/g, "→")}
            </pre>
          </Section>
        )}

        <Section label={problem.targets.length > 1 ? "Functions to write" : "Function to write"}>
          <div className="flex flex-wrap gap-2">
            {problem.targets.map((t) => (
              <span key={t} className="rounded-lg border border-volt-500/25 bg-volt-500/10
                                       px-2.5 py-1 font-mono text-[12px] text-volt-300">
                {t}
              </span>
            ))}
          </div>
        </Section>

        {problem.conventions.length > 0 && (
          <Collapsible label="How this is graded" count={problem.conventions.length}>
            <ul className="space-y-2">
              {problem.conventions.map((c, i) => {
                const [name, ...rest] = c.split(":");
                return (
                  <li key={i} className="flex gap-2 text-[12.5px] leading-relaxed text-mist-300">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-volt-400" />
                    <span><code>{name}</code>{rest.join(":")}</span>
                  </li>
                );
              })}
            </ul>
          </Collapsible>
        )}

        {problem.notes.length > 0 && (
          <Collapsible label="Notes from the test suite" count={problem.notes.length}>
            <ul className="space-y-2">
              {problem.notes.map((n, i) => (
                <li key={i} className="flex gap-2 text-[12.5px] leading-relaxed text-mist-300">
                  <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-amber-400" />
                  <RichText text={n} />
                </li>
              ))}
            </ul>
          </Collapsible>
        )}

        <div className="rounded-xl border border-white/[.06] bg-ink-850/40 px-3.5 py-3">
          <p className="text-[11.5px] leading-relaxed text-mist-400">
            Lives in{" "}
            <code className="font-mono text-[11px] text-mist-300">
              python/{String(problem.topic).padStart(2, "0")}_…/exercise.py
            </code>
            . Same problem, same tests as{" "}
            <code className="font-mono text-[11px] text-mist-300">
              python check.py {problem.topic}
            </code>
            .
          </p>
        </div>
      </div>
    </div>
  );
}
