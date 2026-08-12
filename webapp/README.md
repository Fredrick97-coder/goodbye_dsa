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
| **Chosen language remembered per account** | ✅ survives reload and re-login |
| `stdout` capture and a Console tab | ✅ |
| Drafts autosaved per problem, survive refresh | ✅ (localStorage) |
| Resizable panels, `⌘↵` submit, `⌘'` run | ✅ |
| TypeScript and JavaScript, graded against the same specs | ✅ 232 of 342 problems |
| Adding a language is a driver + a table row | ✅ see below |
| **Accounts, with per-user progress** | ✅ (scrypt + server-side sessions) |
| **Browse and Run without an account; the gate is at Submit** | ✅ |
| **Sandboxed execution** (container, or macOS Seatbelt locally) | ✅ verified against escape attempts |
| **Versioned schema migrations** | ✅ |
| **Env-driven configuration, with a prod safety gate** | ✅ |
| **Structured logs, request ids, error boundary, security headers** | ✅ |
| **Ops CLI: migrate / backup / vacuum / users / reset-password** | ✅ |
| **Test suite (138 tests)** | ✅ |
| **Confetti on an accepted submission** | ✅ lazy-loaded, respects reduced-motion |

## Honest limitations

**Three languages run: Python, TypeScript and JavaScript.** The remaining five
rows in the language table are visibly disabled with the reason, not a "soon".

Coverage is not uniform, and the UI says so per problem:

| | problems |
|---|---|
| Python | **340** of 342 |
| TypeScript / JavaScript | **232** of 342 |

The gap is not laziness — it is what can honestly cross a language boundary. Your
377 reference specs *are* Python: they call `math.comb`, they drive a `Stack`
through a sequence of method calls, they build a `TreeNode` out of the learner's
own class, they check "is this a valid min-heap?" with a Python predicate. For
232 problems the data is ordinary JSON and the Python reference can compute the
expected answers ahead of time, so a TypeScript solution is graded against
*exactly* the same expectations as a Python one. For the other 110 the test is
inseparable from the language, and the problem is marked **Python only** with the
specific reason (`the test drives a class through a sequence of method calls`)
rather than being silently hidden.

A problem is refused rather than partially graded: reporting "8 of 8 passed" when
two of its functions were never run would be worse than refusing.

*Types are stripped, not checked.* Node runs `.mts` natively, so
`function f(n: number): string { return n; }` executes happily. That is what
mainstream judges do, and the starter code says so in a comment instead of
letting a green tick imply your types are sound.

**Two problems have no auto-grading**, and they are the two that cannot have
any: `01-10 Complexity Analysis` asks you to analyse a function that is already
written, and `09-09 LRU Cache` specifies no interface to call. Everything else
— all 340 — is graded. The UI marks the two with an amber dot in the list,
`manual` in the Tests column, and a "no auto-grading" chip on the editor.

**Execution is sandboxed, and which sandbox is in use is never a guess.** Three
backends exist behind one contract, and `auto` picks the strongest the host can
provide:

| Backend | Isolation | Verified |
|---|---|---|
| `docker` | fresh container per submission: `--network none`, `--read-only`, `--user 65534`, `--cap-drop ALL`, `no-new-privileges`, pids/memory/CPU caps, tmpfs `/tmp` | no host filesystem, no network, no DNS; writes to the curriculum mount and to the staged source are refused |
| `seatbelt` | macOS Seatbelt profile, kernel-enforced, same process | no writes anywhere, no network, no `$HOME` or `/etc` reads, no `exec` |
| `local` | subprocess with CPU and address-space rlimits — **not a sandbox** | runaway loops and memory bombs only |

The two safe backends have genuinely **different shapes**, and it is worth being
precise about which:

* **`seatbelt` restricts the host.** The process runs on your filesystem, so the
  policy has to forbid reads, writes and `exec` there — and it does.
* **`docker` replaces the world.** Inside the container a submission *can* run
  the image's own `/bin/ls` and read the image's `/etc/passwd`, and it can write
  to the 32 MB `noexec` tmpfs. None of that reaches anything of yours: the
  container holds no host data, has no network, drops every capability and runs
  as `nobody`. An earlier version of this table claimed docker "blocks spawning
  programs", which was simply wrong — measured, not assumed.

If you want that gap closed too, a distroless base image removes the binaries
there are to spawn. It is a base-image swap in `backend/docker/*.Dockerfile`,
and it buys little against a container that already has no network, no host
mounts and no capabilities.

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
│   ├── languages.py     the language table: one row per language
│   ├── codegen.py       renders starter code from a neutral signature
│   ├── executors/       local | seatbelt | docker, behind one contract
│   ├── runners/         one driver per language + CONTRACT.md
│   ├── repo.py          bridge to python/_harness — catalog, specs, starters
│   ├── progress.py      joins repo (curriculum) with store (what you did)
│   ├── child_runner.py  runs ONE submission, emits per-case JSON
│   ├── execute.py       dispatcher: size cap, concurrency cap, backend choice
│   └── main.py          FastAPI routes and startup order
├── backend/docker/      the sandbox image (runner.Dockerfile, build.sh)
├── backend/tests/       138 tests: db, settings, auth, api, containment,
│                        languages, signature inference, codegen, the Node driver
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
`backend/.env.example` documents every one with its default.

`backend/.env` is read automatically if present, and **real environment
variables win over it** — a container or systemd unit setting `FORGE_DB_PATH`
must not be overridden by a stale file baked into an image. It is gitignored;
`.env.example` is the tracked template. (`FORGE_SKIP_DOTENV=1` ignores it
entirely, which is what the test suite does so its results never depend on an
untracked local file.)

Two settings have no safe default and are therefore **required in production**:

- `FORGE_ALLOWED_ORIGINS` — the app refuses to guess. Guessing means either a
  broken deployment or an allowlist wide enough to be no allowlist.
- a sandboxed `FORGE_EXECUTOR` — see above.

Values are validated at import, so a typo is a startup failure with a message
rather than a subtly wrong runtime. `FORGE_SESSION_DAYS=forever` will not boot.

Settings that are legal but probably a mistake are logged at startup and
returned by `/api/health` under `warnings` — chiefly
`FORGE_TRUST_PROXY_HEADERS=1` with no proxy in front, which makes the login rate
limit bypassable by rotating `X-Forwarded-For`.

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
cd backend && python3 -m pytest tests -q        # 138 tests, ~35s
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

## Preferences

The chosen language is stored per account (`preferences` table, migration 4) and
arrives with `/api/auth/me`, so the app boots already knowing it — no second
round trip and no flash of the wrong language.

Three rules make it behave the way people expect:

* **The preference is the source of truth; per-problem availability only filters
  it.** Opening a Python-only problem shows Python for as long as that problem is
  on screen, and does *not* overwrite the saved choice. Getting this backwards
  meant one Python-only problem silently reset the language for the rest of the
  session while the account still had TypeScript saved.
* **Only an explicit switch writes.** The automatic fallback never persists.
* **Signed out it still works**, in localStorage, and is handed to the account on
  sign-in *if that account has never chosen* — so picking TypeScript and then
  signing up does not drop you back to Python.

Values are validated against the same whitelist the submit path uses, so `rust`
cannot be saved as a preference while it has no driver — the two cannot disagree
about what is runnable.

Adding a preference is a whitelist entry in `store.PREFERENCE_KEYS`, not a
migration: the table is key/value for exactly that reason.

## Adding a language

The platform is built the way LeetCode-style judges are: the problem definition,
the test data and the starter code are language-neutral, and each language brings
a **driver** plus a **table row**. Three languages currently share two drivers.

Concretely, four separable pieces:

| Piece | Where | Language-specific? |
|---|---|---|
| Test data | `python/_harness/fixtures.py` — serialises your specs to JSON | no |
| Signature | `python/_harness/signature.py` — inferred from that data | no |
| Starter code | `app/codegen.py` — one renderer | no, driven by the table |
| Execution | `app/runners/<driver>` + a row in `app/languages.py` | **yes** |

So adding Go looks like this:

1. **Write the driver.** `app/runners/go_runner.go`: read `{source, plan, mode}`
   as JSON on stdin, call the submitted functions, compare with the four
   comparison modes, write the report JSON to stdout. The contract, including the
   `STUB` rule that keeps "not attempted" honest, is in
   `app/runners/CONTRACT.md`; `ts_runner.mjs` is the reference.
2. **Fill in the row.** `languages.py` already has Go's type map, list syntax and
   function shape — it just has `driver=None`. Set the driver, the command and the
   image.
3. **Add the image.** A `go-runner.Dockerfile` plus one line in
   `docker/build.sh`.

You do **not** touch: the API, the frontend, the executors, the specs, or any of
the 342 problems. Starter code for every portable problem is generated from the
inferred signature the moment the row is live, which is why enabling JavaScript
cost one table entry and zero lines of new code.

The type maps are data for exactly this reason — nothing in `codegen.py` branches
on which language it is rendering, and there is a test that fails if a row cannot
render every neutral type.

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

### The confetti

An accepted submission fires a Lottie burst from both bottom corners. The
animation is **generated, not downloaded**:

```bash
cd frontend && python3 scripts/gen_confetti.py     # -> src/assets/confetti.json
```

Three reasons it is generated. It uses this app's palette rather than a stock
asset's, so the celebration looks like part of the product; there is no
attribution question attached to it; and particle count, gravity, spin and
duration are parameters at the top of the script, so tuning the feel is editing
three numbers rather than hunting for a different file. The motion is a sampled
projectile simulation — expressing gravity through bezier easing would be
guesswork, whereas sampling a real trajectory looks right because it is.

Both the player (`lottie_light`, 169 KB) and the animation (339 KB, 28 KB
gzipped) load **only on the first accepted submission** and are cached after
that, so the initial bundle grows by about 1 KB. It respects
`prefers-reduced-motion` by not playing at all, and the overlay is
`pointer-events-none` and destroys itself on completion, so it can never
intercept a click or leak an animation loop.

*Two things were wrong on the first attempt and are worth not re-introducing: at
2400 px/s launch speed the apex was ~1900 px above a 900 px canvas, so the
fastest half of the confetti left the screen and the middle of the animation
looked empty; and 68 particles across a wide viewport read as "some paper fell"
rather than a burst. It is now 120 particles that all stay in frame.*
