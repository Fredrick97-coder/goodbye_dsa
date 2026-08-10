# Forge — a coding-practice workspace for this repo

A LeetCode-style workspace that serves **this repository's own 342 problems**
and grades submissions against **its own ~296 reference tests**. Nothing is
duplicated: the problem text is parsed from the `exercise.py` files and the
tests are the same specs that `python check.py` runs.

```
┌──────────────────────────────────────────────────────────────┐
│  header: brand · problem · language · Reset · Run · Submit   │
├───────────┬──────────────────────┬───────────────────────────┤
│  problem  │  statement           │  Monaco editor            │
│  list     │  (input/output,      ├───────────────────────────┤
│  + filters│   example, grading)  │  Test Results │ Console   │
└───────────┴──────────────────────┴───────────────────────────┘
```

## Run it

```bash
./dev.sh                     # starts both, Ctrl-C stops both
```

Then open **http://localhost:5173**.

First run installs frontend deps automatically. To do it by hand:

```bash
cd backend  && pip install -r requirements.txt
cd frontend && npm install
```

The API needs no separate install if you already have `fastapi` and `uvicorn`.

## What works today

| Feature | Status |
|---|---|
| 342 problems across 22 topics, grouped and filterable | ✅ |
| Search by title, topic, or function name | ✅ |
| Starter code pulled from the real `exercise.py` stub | ✅ |
| Grading against the repo's reference specs | ✅ (275 problems) |
| Per-case results: input / expected / got | ✅ |
| Randomized trials, not just fixed cases | ✅ |
| Verdicts: Accepted / Wrong Answer / Runtime Error / Not Attempted | ✅ |
| `stdout` capture and a Console tab | ✅ |
| Drafts autosaved per problem, survive refresh | ✅ |
| Solved-state and progress in the sidebar | ✅ (localStorage) |
| Resizable panels, `⌘↵` submit, `⌘'` run | ✅ |
| Languages other than Python | ⛔ see below |
| Accounts, server-side progress | ⛔ next step |

## Honest limitations

**Only Python executes.** The language dropdown lists all eight languages the
repo has folders for, but the seven others are visibly disabled rather than
silently broken. The reason is structural: the reference tests *are* Python —
they import your function and compare against `math.comb`, `itertools`, or a
brute-force reference. Supporting Java or C++ means a second test format
(stdin/stdout fixtures per problem), not just another compiler. The API
returns a clear `400` explaining this rather than pretending.

**Two topics have no auto-grading.** Queues (05) and Advanced Trees (17) have
no specs yet, so they load and run but are not graded. The UI marks them with
an amber dot in the list and a "no auto-grading" chip on the editor.

**Execution is isolated, not sandboxed.** Each submission runs in a fresh
subprocess with a 10s wall clock, 5s CPU limit and a 512 MB address-space cap,
so infinite loops and memory bombs are contained — verified. But nothing stops
submitted code from reading your files or opening a socket. That is acceptable
for a single-user tool on `127.0.0.1`, which is what this is. **Before exposing
it to anyone else**, the child process must move into a real boundary: a
network-less container with a read-only filesystem, gVisor/Firecracker, or a
hosted judge such as Judge0 or Piston. The seam for this is one function —
`run_submission()` in `backend/app/execute.py`.

*Note: on macOS `RLIMIT_AS` is not always enforced, so a huge allocation may
hit the wall-clock timeout instead of a clean `MemoryError`. Both are contained;
only the error message differs.*

## Architecture

```
webapp/
├── backend/app/
│   ├── repo.py          bridge to python/_harness — catalog, specs, starters
│   ├── child_runner.py  runs ONE submission, emits per-case JSON
│   ├── execute.py       subprocess + timeouts + signal handling
│   └── main.py          FastAPI routes
└── frontend/src/
    ├── lib/{api,types}.ts
    └── components/{Statement,Editor,Results,ProblemList,ui}.tsx
```

Two deliberate choices:

- **The repo is the single source of truth.** `repo.py` reads `_harness.catalog`
  and `_harness.specs`. Add a problem or a spec to `python/` and it appears here
  with no changes to the webapp.
- **Vite proxies `/api` to the backend**, so the browser sees one origin. No CORS
  in dev, no hardcoded `localhost:8000` in the frontend.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | liveness |
| GET | `/api/meta` | languages, topics, totals |
| GET | `/api/problems` | list; `?topic=&difficulty=&tested=&q=` |
| GET | `/api/problems/{id}` | detail + starter code + grading notes |
| POST | `/api/submit` | `{problemId, language, source, mode}` → report |

`mode` is `test` (grade it) or `run` (just execute and show stdout).
Interactive docs at **http://127.0.0.1:8000/docs**.

## Adding authentication later

The seams are already in place:

1. `frontend/src/lib/api.ts` — `progress` and `drafts` are the only two
   localStorage users. Swap their bodies for `fetch` calls and the UI is done.
2. `backend/app/main.py` — add a dependency for the current user and a
   `submissions` table. The grading path does not change.
3. `POST /api/submit` already returns everything a history record needs:
   verdict, passed/total, elapsed ms, and per-case detail.

## Design notes

Deliberately not a LeetCode clone: a cool slate base (`#070a12`) with a single
electric violet accent (`#6d4aff`), Inter for UI and JetBrains Mono for code,
and a hand-written Monaco theme matched to the palette. Verdict state is echoed
as a coloured ring on the results panel so it reads at a glance.

Layout, colours and fonts are all in `frontend/tailwind.config.js` and
`frontend/src/index.css`.
