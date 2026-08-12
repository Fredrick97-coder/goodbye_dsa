import { lazy, Suspense } from "react";
import { Spinner } from "./ui";

/**
 * Renders a lesson's markdown.
 *
 * Everything here is lazy-loaded. `react-markdown` plus `remark-gfm` plus a
 * highlighter is ~130 KB, and it is only ever needed on the reader route — a
 * visitor who came to practise should not pay for it.
 *
 * The content uses tables heavily (436 rows across the course), which is why
 * `remark-gfm` is not optional: without it the complexity tables render as
 * literal pipes.
 *
 * `rehype-raw` is deliberately NOT used, so embedded HTML stays inert. The
 * lessons are authored in this repo and are not user input, but a renderer that
 * executes whatever is in a content file is the wrong default to establish —
 * especially if courses ever come from anywhere else.
 */
const Renderer = lazy(() => import("./MarkdownRenderer"));

export function Markdown({ body }: { body: string }) {
  return (
    <Suspense
      fallback={
        <div className="flex items-center gap-2 py-8 text-mist-400">
          <Spinner className="h-4 w-4" />
          <span className="text-[12.5px]">rendering…</span>
        </div>
      }
    >
      <Renderer body={body} />
    </Suspense>
  );
}
