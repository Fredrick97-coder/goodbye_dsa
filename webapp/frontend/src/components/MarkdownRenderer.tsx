import hljs from "highlight.js/lib/core";
import javascript from "highlight.js/lib/languages/javascript";
import python from "highlight.js/lib/languages/python";
import typescript from "highlight.js/lib/languages/typescript";
import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Icon } from "./ui";

/**
 * Only the languages the content actually uses are registered.
 *
 * `highlight.js/lib/core` plus three grammars is ~40 KB; the full bundle with
 * 190 languages is ~900 KB for markup nobody here writes.
 */
hljs.registerLanguage("python", python);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("javascript", javascript);

const ALIASES: Record<string, string> = {
  py: "python", python3: "python", ts: "typescript", js: "javascript",
  mts: "typescript", mjs: "javascript",
};

function Code({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);
  const resolved = ALIASES[language] || language;

  const html = useMemo(() => {
    if (resolved && hljs.getLanguage(resolved)) {
      try {
        return hljs.highlight(code, { language: resolved }).value;
      } catch {
        /* fall through to plain text */
      }
    }
    return null;
  }, [code, resolved]);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1400);
    } catch { /* clipboard denied; the code is still selectable */ }
  };

  return (
    <div className="group relative my-4">
      <div className="flex items-center justify-between rounded-t-xl border border-b-0
                      border-white/[.07] bg-ink-950/80 px-3.5 py-1.5">
        <span className="font-mono text-[10.5px] uppercase tracking-wider text-mist-400">
          {resolved || "text"}
        </span>
        <button
          onClick={copy}
          className="flex items-center gap-1.5 rounded-md px-1.5 py-0.5 text-[10.5px]
                     text-mist-400 opacity-0 transition-all hover:text-mist-100
                     group-hover:opacity-100"
        >
          <Icon name={copied ? "check" : "copy"} className="h-3 w-3" />
          {copied ? "copied" : "copy"}
        </button>
      </div>
      <pre className="scroll-thin overflow-x-auto rounded-b-xl border border-white/[.07]
                      bg-ink-950/60 px-4 py-3">
        <code className="hljs font-mono text-[12.5px] leading-relaxed"
              // Highlighted output from highlight.js, which escapes its input.
              // The alternative is no highlighting at all in a course about code.
              {...(html ? { dangerouslySetInnerHTML: { __html: html } } : {})}>
          {html ? undefined : code}
        </code>
      </pre>
    </div>
  );
}

/** Deep-links: every heading gets an id so a lesson section can be linked. */
function slugFor(children: React.ReactNode): string {
  const text = String(children ?? "");
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export default function MarkdownRenderer({ body }: { body: string }) {
  const host = useRef<HTMLDivElement>(null);

  /* Scroll the anchor into view once the content is on screen. */
  useEffect(() => {
    const hash = window.location.hash.slice(1);
    if (!hash || !host.current) return;
    const target = host.current.querySelector(`#${CSS.escape(hash)}`);
    target?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [body]);

  return (
    <div ref={host} className="lesson">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({ className, children, ...props }) {
            const text = String(children ?? "").replace(/\n$/, "");
            const match = /language-(\w+)/.exec(className || "");
            // No language class and no newline means it is inline code.
            if (!match && !text.includes("\n")) {
              return <code className="inline-code" {...props}>{text}</code>;
            }
            return <Code language={match?.[1] ?? ""} code={text} />;
          },
          // The lesson title is rendered by the page, so an h1 inside the body
          // (rare, but present in a few modules) is demoted rather than
          // competing with it.
          h1: ({ children }) => (
            <h2 id={slugFor(children)} className="lesson-h2">{children}</h2>
          ),
          h2: ({ children }) => (
            <h2 id={slugFor(children)} className="lesson-h2">{children}</h2>
          ),
          h3: ({ children }) => (
            <h3 id={slugFor(children)} className="lesson-h3">{children}</h3>
          ),
          h4: ({ children }) => <h4 className="lesson-h4">{children}</h4>,
          table: ({ children }) => (
            <div className="scroll-thin my-4 overflow-x-auto rounded-xl border border-white/[.07]">
              <table className="lesson-table">{children}</table>
            </div>
          ),
          blockquote: ({ children }) => (
            <blockquote className="lesson-quote">{children}</blockquote>
          ),
          a: ({ children, href }) => (
            <a href={href} target={href?.startsWith("http") ? "_blank" : undefined}
               rel="noreferrer" className="lesson-link">{children}</a>
          ),
          hr: () => <hr className="my-6 border-white/[.07]" />,
        }}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}
