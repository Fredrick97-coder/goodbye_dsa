/**
 * Grades ONE TypeScript submission against a test plan.
 *
 * Invoked as:  node --experimental-strip-types ts_runner.mjs <workdir>
 * with {source, plan, mode} as JSON on stdin, and the report as JSON on stdout.
 *
 * The report shape is identical to child_runner.py's, because the API, the
 * verdict logic and the whole frontend consume it without knowing which
 * language produced it. Any divergence here would be a grading bug that only
 * shows up in one language.
 *
 * Node runs TypeScript by *stripping* types, not checking them: `function
 * f(n: number): string { return n; }` executes happily. That is what mainstream
 * judges do, and it is stated in the UI rather than implied -- a learner should
 * not think a green tick means their types are sound.
 *
 * **Grading happens in a worker thread, and this file is both sides of it.**
 * The reason is time limits. `child_runner.py` gets `RLIMIT_CPU` from the OS, but
 * Node has no equivalent, and `while (true) {}` blocks the event loop so hard
 * that a `setTimeout` watchdog on the same thread never fires -- the submission
 * simply ran until the container backstop, twenty seconds later, while the error
 * message claimed ten. A worker can be terminated from the outside, so the main
 * thread stays responsive and enforces the limit itself.
 */

import { pathToFileURL } from "node:url";
import {
  Worker, isMainThread, parentPort, workerData,
} from "node:worker_threads";

const REPR_LIMIT = 220;

function short(value) {
  let text;
  try {
    text = value === undefined ? "undefined" : JSON.stringify(value);
    if (text === undefined) text = String(value);
  } catch {
    text = String(value);
  }
  return text.length <= REPR_LIMIT ? text : text.slice(0, REPR_LIMIT - 3) + "...";
}

/* ------------------------------------------------------------- comparison */

/**
 * Deep equality with a numeric tolerance.
 *
 * `tol` exists because a float answer computed in Python and one computed in
 * JavaScript will not agree bit for bit, and pretending otherwise would fail
 * correct solutions on the last decimal place.
 */
function deepEqual(a, b, tol) {
  if (typeof a === "number" && typeof b === "number") {
    if (Number.isNaN(a) && Number.isNaN(b)) return true;
    if (tol != null) return Math.abs(a - b) <= tol;
    // An integer expectation from Python may arrive as 3 and be produced as 3.0;
    // in JS those are the same value, so plain === is right here.
    return a === b;
  }
  // Python's True/False serialise to JSON booleans; a solution returning 1 for
  // true is wrong, so no coercion.
  if (a === null || b === null) return a === b;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  if (Array.isArray(a)) {
    if (a.length !== b.length) return false;
    return a.every((v, i) => deepEqual(v, b[i], tol));
  }
  if (typeof a === "object" && typeof b === "object") {
    const ka = Object.keys(a).sort();
    const kb = Object.keys(b).sort();
    if (ka.length !== kb.length || !ka.every((k, i) => k === kb[i])) return false;
    return ka.every((k) => deepEqual(a[k], b[k], tol));
  }
  return a === b;
}

/** Total order over JSON values, so "sorted" means the same thing both sides. */
function compareValues(a, b) {
  const rank = (v) => (v === null ? 0 : typeof v === "boolean" ? 1
    : typeof v === "number" ? 2 : typeof v === "string" ? 3
    : Array.isArray(v) ? 4 : 5);
  const ra = rank(a), rb = rank(b);
  if (ra !== rb) return ra - rb;
  if (ra === 2) return a - b;
  if (ra === 3) return a < b ? -1 : a > b ? 1 : 0;
  if (ra === 4) {
    for (let i = 0; i < Math.min(a.length, b.length); i++) {
      const c = compareValues(a[i], b[i]);
      if (c !== 0) return c;
    }
    return a.length - b.length;
  }
  if (ra === 1) return (a ? 1 : 0) - (b ? 1 : 0);
  return compareValues(JSON.stringify(a), JSON.stringify(b));
}

const sortCopy = (xs) => [...xs].sort(compareValues);

/** Mirrors _harness/spec.py's normalisers, name for name. */
function normalise(value, mode) {
  if (value == null) return value;
  switch (mode) {
    case "sorted":
      return Array.isArray(value) ? sortCopy(value) : value;
    case "sorted_pairs":
      return Array.isArray(value)
        ? sortCopy(value.map((item) => (Array.isArray(item) ? [...item] : item)))
        : value;
    case "sorted_inner":
      return Array.isArray(value)
        ? sortCopy(value.map((item) => (Array.isArray(item) ? sortCopy(item) : item)))
        : value;
    default:
      return value;
  }
}

function matches(got, want, target) {
  const g = normalise(got, target.compare);
  const w = normalise(want, target.compare);
  return deepEqual(g, w, target.tol);
}

/* ------------------------------------------------------------------ report */

function fatal(kind, message) {
  return {
    ok: false,
    compileError: { type: kind, message, line: null, offset: null, text: "" },
    stdout: "",
    targets: [],
  };
}

/** Only the main thread writes to stdout; see the module docstring. */
function emit(report) {
  process.stdout.write(JSON.stringify(report));
}

/* --------------------------------------------------------------- stub check */

/**
 * Is this function still an unwritten stub?
 *
 * Mirrors the AST check on the Python side, but source-based: a body that is
 * empty, or only a `return` / `return undefined` / `throw new Error("...")`, is
 * "not attempted" rather than "wrong". Getting this right is what makes the
 * verdict say Not Attempted instead of accusing an untouched starter of being
 * incorrect.
 */
function looksUnwritten(source, name) {
  const pattern = new RegExp(
    `(?:export\\s+)?(?:async\\s+)?function\\s+${name}\\s*(?:<[^>]*>)?\\s*\\([^)]*\\)` +
    `\\s*(?::[^{]*)?\\{([\\s\\S]*?)\\n\\}`, "m");
  const found = source.match(pattern);
  if (!found) return false;
  const body = found[1]
    .replace(/\/\/[^\n]*/g, "")
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .trim();
  if (body === "") return true;
  // The generated starter ends in a typed placeholder so the file compiles:
  // `return "";` for a string, `return 0;` for a number, `return [];` for an
  // array. A body consisting of nothing but one of those is an untouched stub,
  // not an attempt -- and no problem here is solved by a bare literal.
  return /^(return(\s+(undefined|null|""|''|``|0|-1|\[\]|\{\}|false|true|NaN))?\s*;?|throw\s+new\s+Error\([^)]*\)\s*;?)$/
    .test(body);
}

/* -------------------------------------------------------------------- main */

async function grade(job) {
  const { source, plan, mode = "test" } = job;

  // The PARENT wrote the file and told us where; the driver never writes to
  // disk. That is what lets this run under a sandbox profile that forbids all
  // writes, and it is why the extension is .mts -- Node reads .mts as
  // ES-module TypeScript regardless of any package.json above it, whereas a
  // bare .ts is read as CommonJS and fails on the first `export`.
  const file = job.sourceFile;
  if (!file) {
    return (fatal("BadJob", "the job did not say where the source was staged"));
    return;
  }


  // Interception stays on through grading and is lifted only to emit. Restoring
  // it after the import meant a console.log inside a graded function wrote
  // straight into the report channel and produced unparseable output.
  let module_;
  try {
    module_ = await import(pathToFileURL(file).href);
  } catch (err) {
    const report = fatal(err instanceof SyntaxError ? "SyntaxError" : err.constructor.name,
                         String(err.message).split("\n")[0]);
      return report;
    return;
  }

  const report = { ok: true, compileError: null, stdout: "", targets: [] };

  if (mode === "run") {
    report.targets = [{ target: "(run)", status: "RAN", cases: [],
                        passed: 0, total: 0, note: "" }];
      return report;
    return;
  }

  if (!plan || !plan.targets || plan.targets.length === 0) {
    report.untested = true;
    return report;
    return;
  }

  for (const target of plan.targets) {
    // Accept the exact name from the problem statement, and the camelCase form
    // a TypeScript developer would reach for. Guessing wrong should not read as
    // "your function is missing".
    const camel = target.name.replace(/_([a-z0-9])/g, (_, c) => c.toUpperCase());
    const fn = module_[target.name] ?? module_[camel]
      ?? module_.default?.[target.name] ?? module_.default?.[camel];

    const out = { target: target.name, note: target.note || "", cases: [],
                  passed: 0, total: 0, status: "PASS" };

    if (typeof fn !== "function") {
      out.status = "MISSING";
      out.total = 1;
      out.cases.push({ name: target.name, passed: false, input: "", expected: "",
                       got: "", error: `export a function named ${target.name}` +
                                       ` (or ${camel})` });
      report.targets.push(out);
      continue;
    }

    const unwritten = looksUnwritten(source, target.name)
      || looksUnwritten(source, camel);
    let stubLike = 0, realProgress = 0, shown = 0;

    for (let i = 0; i < target.cases.length; i++) {
      const { args, expected } = target.cases[i];
      const label = i < 0 ? "" : `case ${i + 1}`;
      // structuredClone so a solution that mutates its input cannot corrupt the
      // next case -- and so `inplace` can compare against a pristine copy.
      const callArgs = structuredClone(args);
      let got, threw = null;
      try {
        got = fn(...callArgs);
        if (got instanceof Promise) got = await got;
        if (target.inplace && got === undefined) got = callArgs[0];
      } catch (err) {
        threw = `${err?.constructor?.name ?? "Error"}: ${err?.message ?? err}`;
      }

      out.total += 1;

      if (threw) {
        out.status = "ERROR";
        if (shown < 3) {
          shown += 1;
          out.cases.push({ name: label, passed: false, input: short(args),
                           expected: short(expected), got: "", error: threw });
        }
        continue;
      }

      if (matches(got, expected, target)) {
        out.passed += 1;
        const couldBeStub = got === undefined
          || (target.inplace && deepEqual(got, args, target.tol));
        if (!couldBeStub) realProgress += 1;
        continue;
      }

      if (got === undefined || (target.inplace && deepEqual(got, args, target.tol))) {
        stubLike += 1;
      }
      if (shown < 3) {
        shown += 1;
        out.cases.push({ name: label, passed: false, input: short(args),
                         expected: short(expected), got: short(got), error: "" });
      }
    }

    if (out.status !== "ERROR") {
      if (out.passed === out.total && out.total > 0) {
        // ...unless nothing that passed required an implementation, which is
        // the same rule the Python runner applies.
        out.status = (unwritten && realProgress === 0) ? "STUB" : "PASS";
      } else if (unwritten) {
        // The SOURCE is the authority for "not attempted", mirroring
        // _body_is_empty on the Python side. Value-based detection cannot work
        // here: a Python stub returns None, but a TypeScript starter has to
        // return a typed placeholder (`""`, `0`, `[]`) for the file to compile,
        // and those are ordinary values.
        out.status = "STUB";
      } else if (stubLike > 0 && stubLike === out.total - out.passed) {
        // Fallback for a shape the regex cannot read -- an arrow function
        // assigned to a const, say -- where every failing case produced nothing.
        out.status = "STUB";
      } else {
        out.status = "FAIL";
      }
    }
    report.targets.push(out);
  }

  return report;
}


/* ------------------------------------------------------------ main thread */

/**
 * Read the job, run the grading in a worker, and enforce the time limit.
 *
 * The worker's stdout is piped rather than inherited, so anything the
 * submission prints is captured instead of corrupting the report channel.
 */
async function main() {
  let job;
  try {
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    job = JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch (err) {
    process.stdout.write(JSON.stringify(
      fatal("BadJob", `could not read the job: ${err.message}`)));
    return;
  }

  const limitMs = Math.max(1, Number(job.cpuSeconds) || 5) * 1000;
  const maxStdout = Number(job.maxStdoutBytes) || 8000;
  const printed = [];
  // Truncation has to be visible; a silently halved demo reads as a crash.
  const clip = (text) => text.length <= maxStdout ? text
    : `${text.slice(0, maxStdout)}\n\n... output truncated at ` +
      `${maxStdout.toLocaleString()} bytes ...`;

  const worker = new Worker(new URL(import.meta.url), {
    workerData: job,
    stdout: true,
    stderr: true,
    // A submission cannot be allowed to raise its own limits.
    resourceLimits: {
      maxOldGenerationSizeMb: Math.max(64, Number(job.memoryMb) || 512),
    },
  });
  worker.stdout.on("data", (c) => printed.push(c.toString("utf8")));
  worker.stderr.on("data", (c) => printed.push(c.toString("utf8")));

  const done = await new Promise((resolve) => {
    let settled = false;
    const finish = (value) => { if (!settled) { settled = true; resolve(value); } };

    const timer = setTimeout(() => {
      // terminate() stops the isolate even mid-loop, which is the whole reason
      // the grading runs over here.
      void worker.terminate();
      finish({ timedOut: true });
    }, limitMs);

    worker.on("message", (report) => { clearTimeout(timer); finish({ report }); });
    worker.on("error", (err) => {
      clearTimeout(timer);
      finish({ report: fatal(err?.constructor?.name ?? "Error",
                             String(err?.message ?? err).split("\n")[0]) });
    });
    worker.on("exit", (code) => {
      clearTimeout(timer);
      // The worker ended without posting a report. By far the most common cause
      // is the submission calling process.exit() -- naming that is more useful
      // than reporting an exit code the learner did not choose.
      finish({ report: fatal(
        "Aborted",
        `your code ended the process before the tests finished (exit ${code}) ` +
        `-- calling process.exit() or exit() will do this`) });
    });
  });

  const stdout = clip(printed.join(""));
  if (done.timedOut) {
    const report = fatal(
      "TimeLimit",
      `killed after ${limitMs / 1000}s -- an infinite loop, or a solution too ` +
      `slow for this problem's input sizes`);
    report.stdout = stdout;
    process.stdout.write(JSON.stringify(report));
    return;
  }

  const report = done.report;
  if (!report.stdout) report.stdout = stdout;
  process.stdout.write(JSON.stringify(report));
}

if (isMainThread) {
  try {
    await main();
  } catch (err) {
    process.stdout.write(JSON.stringify(fatal(
      "HarnessError", String(err?.stack ?? err).slice(0, 1500))));
  }
} else {
  // Worker side: grade and hand the report back. Nothing is written to stdout
  // here except whatever the submission itself prints.
  try {
    parentPort.postMessage(await grade(workerData));
  } catch (err) {
    parentPort.postMessage(fatal("HarnessError",
                                 String(err?.stack ?? err).slice(0, 1500)));
  }
}
