import { useEffect, useRef, useState } from "react";
// Type-only import: erased at compile time, so naming these costs the bundle
// nothing. `lottie_light.d.ts` re-exports a default, which is why the player's
// type is `LottiePlayer` rather than `typeof import(...)`.
import type { AnimationItem, LottiePlayer } from "lottie-web";

/**
 * A one-shot confetti burst, played over the whole app.
 *
 * Three decisions worth knowing about:
 *
 * **The player and the animation are lazy-loaded.** `lottie_light` is ~168 KB
 * minified and the animation JSON another ~190 KB (13 KB gzipped). Importing
 * them at the top level would make every visitor pay for a celebration most of
 * them have not earned yet, so both arrive by dynamic import the first time a
 * submission passes, and stay cached after that.
 *
 * **`lottie_light`, not the full build.** The animation is only shape layers --
 * no images, no text, no expressions -- which is exactly what the light build
 * renders. The full player is 306 KB for features this file does not use.
 *
 * **It respects `prefers-reduced-motion`.** Someone who has asked their system
 * for less motion should not get 68 spinning rectangles; they get nothing, and
 * the verdict banner still tells them they passed.
 */

/**
 * Module-level cache.
 *
 * The player and the JSON are fetched once per page load, not once per solve --
 * without this, a learner working through a topic re-downloads and re-parses
 * ~200 KB on every accepted submission.
 */
let cached: Promise<{ lottie: LottiePlayer; data: unknown }> | null = null;

function load() {
  if (!cached) {
    cached = Promise.all([
      import("lottie-web/build/player/lottie_light"),
      import("../assets/confetti.json"),
    ]).then(([player, json]) => ({
      lottie: player.default,
      data: (json as { default: unknown }).default ?? json,
    }));
  }
  return cached;
}

function prefersReducedMotion(): boolean {
  return typeof window !== "undefined"
    && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches === true;
}

export function Confetti({ onDone }: { onDone: () => void }) {
  const host = useRef<HTMLDivElement>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (prefersReducedMotion()) { onDone(); return; }

    let animation: AnimationItem | null = null;
    let alive = true;

    void load().then(({ lottie, data }) => {
      // Unmounted while the chunk was in flight, or the ref never attached.
      if (!alive || !host.current) return;
      animation = lottie.loadAnimation({
        container: host.current,
        renderer: "svg",
        loop: false,
        autoplay: true,
        animationData: data as object,
        rendererSettings: {
          // `slice` fills the viewport at any aspect ratio, so the burst always
          // reaches the edges instead of letterboxing on a wide window.
          preserveAspectRatio: "xMidYMid slice",
          // The overlay is decorative and must never intercept a click, even
          // for the split second it is on screen.
          className: "pointer-events-none",
          progressiveLoad: false,
        },
      });
      animation.addEventListener("complete", () => { if (alive) onDone(); });
    }).catch(() => {
      // A missing chunk must not swallow the verdict. Fail quiet and closed.
      if (alive) { setFailed(true); onDone(); }
    });

    return () => {
      alive = false;
      // destroy() removes the SVG and the rAF loop; without it, navigating away
      // mid-burst leaves the animation running for nothing.
      animation?.destroy();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (failed) return null;

  return (
    <div
      ref={host}
      aria-hidden
      className="pointer-events-none fixed inset-0 z-[60] select-none"
    />
  );
}
