/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "SF Mono", "Menlo", "Consolas", "monospace"],
      },
      colors: {
        // A cool slate base with a single electric accent. Deliberately not
        // LeetCode green / HackerRank green -- this is its own identity.
        ink: {
          950: "#070a12", 900: "#0b0f1a", 850: "#0f1420",
          800: "#141a28", 750: "#1a2131", 700: "#222b3d",
          600: "#2e3950", 500: "#414f6b", 400: "#5c6b8a",
        },
        mist: { 400: "#7d8ba8", 300: "#9aa7c0", 200: "#c3ccdd", 100: "#e6ebf4" },
        volt: { 600: "#4c2bd9", 500: "#6d4aff", 400: "#8a6dff", 300: "#a894ff" },
        mint: { 500: "#12b981", 400: "#2ed3a0" },
        rose: { 500: "#f2456b", 400: "#ff6b88" },
        amber: { 500: "#f5a524", 400: "#ffbe4d" },
        sky: { 500: "#2c9ceb", 400: "#54b3f5" },
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(109,74,255,.35), 0 8px 30px -8px rgba(109,74,255,.45)",
        panel: "0 1px 0 0 rgba(255,255,255,.04) inset, 0 12px 40px -20px rgba(0,0,0,.8)",
      },
      keyframes: {
        "fade-up": { from: { opacity: 0, transform: "translateY(6px)" }, to: { opacity: 1, transform: "none" } },
        shimmer: { "100%": { transform: "translateX(100%)" } },
        "pulse-ring": { "0%": { boxShadow: "0 0 0 0 rgba(109,74,255,.5)" }, "70%": { boxShadow: "0 0 0 10px rgba(109,74,255,0)" }, "100%": { boxShadow: "0 0 0 0 rgba(109,74,255,0)" } },
      },
      animation: {
        "fade-up": "fade-up .28s cubic-bezier(.2,.8,.2,1) both",
        shimmer: "shimmer 1.6s infinite",
        "pulse-ring": "pulse-ring 1.4s cubic-bezier(.4,0,.6,1) infinite",
      },
    },
  },
  plugins: [],
};
