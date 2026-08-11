# Forge — a coding-practice platform for this repo

A LeetCode-style platform that serves **this repository's own 342 problems** and
grades submissions against **its own 377 reference specs**. Nothing is
duplicated: the problem text is parsed from the `exercise.py` files and the tests
are the same specs that `python check.py` runs.

```
Dashboard  /            rings, streak, heatmap, suggested next, 22 topic tracks
Problems   /problems    full problem set — status, filters, search, bookmarks
Solve      /problems/03-07   statement | editor + results, with Submissions & Notes
Progress   /progress    activity heatmap, per-difficulty, per-topic, full history
```

```
┌───────────────────────────────────────────────────────────────────┐
│ Forge │ Dashboard · Problems · Progress        88/342 · Random    │
├───────────────────────────────────────────────────────────────────┤
│ ☰ ← → Longest Palindromic Substring  Hard ✓Solved ★  Py · Run ·▶  │
├──────────┬──────────────────────────┬─────────────────────────────┤
│ switcher │ Description │ Submissions │  Monaco editor             │
│ (topic-  │ Notes       │             ├─────────────────────────────┤
│  scoped) │ statement, grading rules  │  Test Results │ Console    │
└──────────┴──────────────────────────┴─────────────────────────────┘
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

## What works today

| Feature | Status |
|---|---|
| 342 problems across 22 topics, four pages, real URLs | ✅ |
| Problem set: status / difficulty / topic / graded / bookmarked filters, all in the URL | ✅ |
| Starter code pulled from the real `exercise.py` stub | ✅ |
| Grading against the repo's reference specs | ✅ (340 of 342 problems) |
| Per-case results: input / expected / got | ✅ |
| Randomized trials, not just the fixed examples | ✅ |
| Verdicts: Accepted / Wrong Answer / Runtime Error / Not Attempted | ✅ |
| **Submission history per problem, with the code you wrote** | ✅ (SQLite) |
| **Solved / attempted state, server-side** | ✅ (SQLite) |
| **Streaks, activity heatmap, per-topic and per-difficulty progress** | ✅ |
| **Per-problem notes, autosaved** | ✅ |
| **Bookmarks, random unsolved problem, prev/next navigation** | ✅ |
| `stdout` capture and a Console tab | ✅ |
| Drafts autosaved per problem, survive refresh | ✅ (localStorage) |
| Resizable panels, `⌘↵` submit, `⌘'` run | ✅ |
| Languages other than Python | ⛔ see below |
| **Accounts, with per-user progress** | ✅ (scrypt + server-side sessions) |
| **Browse and Run without an account; the gate is at Submit** | ✅ |
| **Sandboxed execution** (container, or macOS Seatbelt locally) | ✅ verified against escape attempts |
| **Versioned schema migrations** | ✅ |
| **Env-driven configuration, with a prod safety gate** | ✅ |
| **Structured logs, request ids, error boundary, security headers** | ✅ |
| **Ops CLI: migrate / backup / vacuum / users / reset-password** | ✅ |
| **Test suite (102 tests)** | ✅ |

## Honest limitations

**Only Python executes.** The language dropdown lists all eight languages the
repo has folders for, but the seven others are visibly disabled rather than
silently broken. The reason is structural: the reference tests *are* Python —
they import your function and compare against `math.comb`, `itertools`, or a
brute-force reference. Supporting Java or C++ means a second test format
(stdin/stdout fixtures per problem), not just another compiler. The API returns
a clear `400` explaining this rather than pretending.

**Two problems have no auto-grading**, and they are the two that cannot have
any: `01-10 Complexity Analysis` asks you to analyse a function that is already
written, and `09-09 LRU Cache` specifies no interface to call. Everything else
— all 340 — is graded. The UI marks the two with an amber dot in the list,
`manual` in the Tests column, and a "no auto-grading" chip on the editor.

**Execution is sandboxed, and which sandbox is in use is never a guess.** Three
backends exist behind one contract, and `auto` picks the strongest the host can
provide:

| Backend | Isolation | Verified to block |
|---|---|---|
| `docker` | fresh container per submission: `--network none`, `--read-only`, `--user 65534`, `--cap-drop ALL`, `no-new-privileges`, pids/memory/CPU caps, tmpfs `/tmp` | writing the curriculum mount, network, `$HOME` reads, spawning programs |
| `seatbelt` | macOS Seatbelt profile, kernel-enforced, on the same process | filesystem writes anywhere, network, `$HOME` reads, `exec` of anything but the interpreter |
| `local` | subprocess with CPU and address-space rlimits — **not a sandbox** | runaway loops and memory bombs only |

`FORGE_ENV=prod` **refuses to start on `local`** unless you set
`FORGE_ALLOW_UNSAFE_EXECUTOR=1`. A deployment that silently degraded to the
unsandboxed runner because the Docker socket was missing would look healthy and
be wide open, so it is fatal rather than a warning. `/api/health` reports the
resolved backend and whether it is sandboxed.

The container image is deliberately almost empty — a Python interpreter and
nothing else. The curriculum and the runner script are bind-mounted read-only, so
adding a problem never means rebuilding it:

```bash
backend/docker/build.sh          # ~70 MB, python:3.12-alpine
```

*Measured overhead: ~150 ms per submission for the container versus ~40 ms for a
bare subprocess. Worth it.*

## What counts as a submission

Pressing **Run** never records anything — it is a scratchpad. Pressing **Submit**
records the attempt *unless* the verdict is `stub`, i.e. you submitted untouched
starter code. Both rules exist so the history and the "attempted" count mean
something: with 394 stubs in the repo, recording empty submits would drown the
two problems you actually got wrong.

Stub detection is AST-based (`empty_bodies` in `child_runner.py`) because
`inspect.getsource` cannot see code that arrived as a string and was `exec`'d.

## Architecture

```
webapp/
├── backend/app/
│   ├── settings.py      every knob, from FORGE_* env vars, validated at import
│   ├── db.py            connections, pragmas, retries, migrations, backup
│   ├── store.py         queries only — no driver details, no pragmas
│   ├── auth.py          scrypt, sessions, rate limiting, the CSRF guard
│   ├── observability.py logging, request ids, error boundary, headers
│   ├── cli.py           operational commands
│   ├── executors/       local | seatbelt | docker, behind one contract
│   ├── repo.py          bridge to python/_harness — catalog, specs, starters
│   ├── progress.py      joins repo (curriculum) with store (what you did)
│   ├── child_runner.py  runs ONE submission, emits per-case JSON
│   ├── execute.py       dispatcher: size cap, concurrency cap, backend choice
│   └── main.py          FastAPI routes and startup order
├── backend/docker/      the sandbox image (runner.Dockerfile, build.sh)
├── backend/tests/       102 tests: db, settings, auth, api, containment
└── frontend/src/
    ├── lib/{api,types,format}.ts, app-data.tsx   one fetch, shared by all pages
    ├── lib/auth.tsx      who is signed in, and the requireAuth gate
    ├── routes/{Dashboard,Problems,Solve,Progress}.tsx
    └── components/{Shell,AuthModal,AccountMenu,SignInPanel,Statement,
                    Editor,Results,SubmissionsTab,NotesTab,ProblemList,
                    Heatmap,ui}.tsx
```

Four deliberate choices:

- **The repo is the single source of truth.** `repo.py` reads `_harness.catalog`
  and `_harness.specs`. Add a problem or a spec to `python/` and it appears here
  with no changes to the webapp.
- **Progress is server-side.** localStorage keeps drafts only. Solved-state,
  history, streaks and notes live in `backend/data/forge.db`, so they survive a
  cache clear and can be queried across problems.
- **Every user-scoped function takes its user id explicitly.** Nothing defaults
  to an ambient "current user" -- a query that quietly fell back to one would be
  a single refactor away from showing one account's progress to another.
- **Vite proxies `/api` to the backend**, so the browser sees one origin. No CORS
  in dev, no hardcoded `localhost:8000` in the frontend.

The whole problem list (342 rows, ~90 KB) is fetched once into `app-data.tsx` and
filtered in memory, so filters and search are instant and page transitions never
spin.

## API

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | — | create an account, sets the session cookie |
| POST | `/api/auth/login` | — | sign in |
| POST | `/api/auth/logout` | — | end this session |
| GET | `/api/auth/me` | — | current user, or `{"user": null}` |
| POST | `/api/auth/password` | ✔ | change password, ends other sessions |
| POST | `/api/auth/name` | ✔ | change display name |
| POST | `/api/auth/logout-everywhere` | ✔ | keep this session, drop the rest |
| GET | `/api/health` | — | config, schema version, db stats, executor; **503** if degraded |
| GET | `/api/ready` | — | cheap readiness probe for a load balancer |
| GET | `/api/meta` | — | languages, topics, totals |
| GET | `/api/problems` | — | list; `?topic=&difficulty=&tested=&status=&bookmarked=&q=` |
| GET | `/api/problems/random` | — | a random unsolved, auto-graded problem |
| GET | `/api/problems/{id}` | — | detail + starter code + grading notes + prev/next |
| POST | `/api/submit` | run: — · test: ✔ | `{problemId, language, source, mode}` → report |
| GET | `/api/submissions` | ✔ | history; `?problemId=&limit=` |
| GET | `/api/submissions/{id}` | ✔ | one submission, including its source |
| GET | `/api/progress` | ✔ | dashboard aggregate: totals, difficulty, topics, activity |
| GET | `/api/activity` | ✔ | daily buckets for the heatmap; `?days=` |
| GET·POST | `/api/bookmarks[/{id}]` | ✔ | list / toggle |
| GET·PUT | `/api/notes/{id}` | ✔ | read / save (an empty body deletes) |

`mode` is `test` (grade it) or `run` (just execute and show stdout).
Interactive docs at **http://127.0.0.1:8000/docs**.

`/api/problems/random` is declared before `/api/problems/{id}` on purpose —
FastAPI matches in order, so the reverse would read "random" as a problem id.

## Accounts

Sign-in is required to *record* anything, and nothing else. You can read every
problem, open the editor, type, and press **Run** with no account at all — the
prompt appears at **Submit**, which is the first moment your work would be
stored. The pending submission is replayed automatically once you are in, so the
click is never wasted.

| Public | Signed in |
|---|---|
| problem list, statements, starter code | grading (`mode="test"`) |
| `Run` (executes, records nothing) | submission history, with your code |
| topic and difficulty filters | solved / attempted state, streaks, heatmap |
| | bookmarks and per-problem notes |

### How it works

* **Passwords** are hashed with **scrypt** from the standard library
  (n=2¹⁵ → 32 MB, ~50 ms per verification), with a per-user random salt. The
  parameters are stored inside the hash string, so they can be raised later
  without invalidating anyone's password — `needs_rehash` upgrades a hash
  transparently on the next successful login.
* **Sessions are opaque and server-side**: 32 random bytes in an HttpOnly,
  SameSite=Lax cookie, stored only as a SHA-256 hash. That is what makes logout,
  "sign out other devices", and revocation real. A JWT cannot be revoked before
  it expires without a server-side blocklist, at which point it is a session
  with extra steps.
* `Secure` is set on the cookie unless the request is plain-http localhost, so
  it is correct the moment this is served over TLS — no config flag to forget.
* **Login failures are uniform.** Same message and the same scrypt cost whether
  the email is unknown or the password is wrong, so timing and wording cannot be
  used to enumerate accounts.
* **Rate limited** to 8 failures per client per 15 minutes on login, register
  and password change.
* **Changing your password ends every other session**, which is the entire point
  of changing it. The tab you changed it in stays signed in.
* **Cross-origin state changes are refused** (`Origin` check) on top of
  SameSite=Lax. A missing `Origin` is allowed so `curl` still works — browsers
  always send it on the cross-site requests that matter.
* **Every query is scoped by the session's user id**, never by a client
  parameter. Asking for another account's submission returns 404, not their code.

### What is deliberately not here

* **No email verification and no password reset.** Both need a mail path, and
  this runs on `127.0.0.1` with a SQLite file — a reset link nobody can receive
  is worse than none. Reset a forgotten password by deleting the row.
* **The rate limiter is in-process**, so it resets when the server restarts.
  Honest for one process; move it into SQLite before running multi-worker.
* **No roles or sharing.** Accounts exist to separate progress, not to
  collaborate.

### Still missing for a public rollout

* **No email verification or password reset.** Both need a mail path. Until then
  `app.cli reset-password` is the operator-run substitute, and it ends every
  session for that account exactly as a self-service change would.
* **No abuse controls beyond rate limiting.** There is nothing stopping one
  account from submitting in a loop; `FORGE_EXEC_MAX_CONCURRENT` caps the damage
  to the host but does not attribute it per user.
* **No metrics endpoint.** The logs are structured and carry durations, which is
  enough to answer questions after the fact, but there is no `/metrics` to scrape.

## Configuration

Everything is environment variables prefixed `FORGE_`, read once at startup.
`backend/.env.example` documents every one with its default; there is no config
file to forget to copy.

Two settings have no safe default and are therefore **required in production**:

- `FORGE_ALLOWED_ORIGINS` — the app refuses to guess. Guessing means either a
  broken deployment or an allowlist wide enough to be no allowlist.
- a sandboxed `FORGE_EXECUTOR` — see above.

Values are validated at import, so a typo is a startup failure with a message
rather than a subtly wrong runtime. `FORGE_SESSION_DAYS=forever` will not boot.

## Running it for real

```bash
# 1. build the sandbox image
backend/docker/build.sh

# 2. check the configuration before taking traffic
cd backend
FORGE_ENV=prod \
FORGE_ALLOWED_ORIGINS=https://forge.example \
FORGE_DB_PATH=/var/lib/forge/forge.db \
python3 -m app.cli check

# 3. serve it
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Put a TLS-terminating reverse proxy in front, serve `frontend/dist` as static
files from the same origin, and proxy `/api` to uvicorn. Same origin means the
session cookie needs no `Domain` and CORS does nothing — which is the simplest
correct arrangement.

**One worker is the right starting point.** SQLite in WAL mode allows one writer
with concurrent readers; this workload is overwhelmingly reads. `--workers 2` also
works (the rate limiter and sessions are in the database, not in process memory),
but the write lock is then shared, so measure before assuming it helps.

If `FORGE_TRUST_PROXY_HEADERS=1`, be certain your proxy *overwrites*
`X-Forwarded-For` rather than appending to whatever the client sent — otherwise
rate limiting is bypassable with a header.

## Ops

```bash
python3 -m app.cli check              # config, schema, executors, health
python3 -m app.cli migrate            # bring the schema to head (idempotent)
python3 -m app.cli backup [path]      # consistent copy, safe while running
python3 -m app.cli vacuum             # reclaim space
python3 -m app.cli users              # accounts, submission counts, sessions
python3 -m app.cli delete-user EMAIL   # account + all its data (cascade)
python3 -m app.cli reset-password EMAIL
python3 -m app.cli purge-sessions
```

`backup` uses SQLite's online backup API, not a file copy: `cp` on a WAL database
can capture a torn state because the newest committed data lives in the `-wal`
file. Schedule it however you schedule anything — it needs no downtime.

**Schema changes** are forward-only migrations in `db.MIGRATIONS`, versioned with
`PRAGMA user_version` (stored in the file header, so it cannot drift from the
schema it describes). Append a tuple, never edit a shipped one. This is the
mechanism the extra material will use when you add it; `/api/health` returns 503
if the running code expects a newer schema than the file has, so a half-finished
rollout fails its health check instead of serving errors.

## Tests

```bash
cd backend && python3 -m pytest tests -q        # 102 tests, ~30s
```

Each test gets its own database file and its own reloaded configuration, so they
are order-independent. `scrypt` is turned down to 2¹² for the suite — with a
matching test asserting production still uses 2¹⁵, because a fast test suite is
worthless if it tests a weaker password hash than you ship.

The containment tests (`test_executors.py`) attempt to write to the curriculum
mount, open a socket, read `$HOME`, and spawn `/bin/ls` — against every sandbox
the host offers. They *skip with a stated reason* when a backend is unavailable
rather than passing quietly, so "all green" can never hide "the sandbox was never
exercised".

## If you outgrow SQLite

The move to Postgres is contained on purpose. Everything SQLite-specific lives in
`app/db.py`: `connect()`, the pragmas, the retry predicate, and the migration
runner's use of `user_version`. `store.py` above it only issues SQL and never
touches a driver detail or a pragma.

What the swap involves:

1. `db.py` — replace the connection helpers with a pool (`psycopg_pool`), keep the
   same `transaction()` / `reading()` / `query_all()` surface, and move the schema
   version into a table since `user_version` is SQLite's.
2. `store.py` — `?` placeholders become `%s`; `INSERT OR REPLACE` becomes
   `INSERT ... ON CONFLICT DO UPDATE` (the notes upsert already uses that form);
   `AUTOINCREMENT` becomes `GENERATED BY DEFAULT AS IDENTITY`.
3. Nothing else. `auth.py`, the routes, the executors and the whole frontend are
   untouched, because none of them know where the data lives.

The signal that it is time: sustained write contention, or wanting more than one
machine. Read volume alone will not do it.

## Resetting your data

```bash
rm backend/data/forge.db      # then restart the API; the schema is recreated
```

That also deletes every account. To reset one forgotten password without losing
the rest, delete just that user (their submissions and sessions go with them,
via `ON DELETE CASCADE`):

```bash
sqlite3 backend/data/forge.db "DELETE FROM users WHERE email = 'you@example.com';"
```

## Design notes

Deliberately not a LeetCode clone: a cool slate base (`#070a12`) with a single
electric violet accent (`#6d4aff`), Inter for UI and JetBrains Mono for code, and
a hand-written Monaco theme matched to the palette. Verdict state is echoed as a
coloured ring around the results panel so it reads at a glance.

Layout, colours and fonts are all in `frontend/tailwind.config.js` and
`frontend/src/index.css`.
