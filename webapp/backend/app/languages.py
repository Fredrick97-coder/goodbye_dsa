"""
The language registry: one row per language, read by the executor and the UI.

This is the table LeetCode-style platforms keep so that adding a language is a
configuration change rather than a code change. Everything language-specific
lives here or in that language's driver file. Nothing else in the codebase
branches on "is this Python?".

**To add a language** you need exactly three things:

1. A **driver** in `app/runners/` that reads `{source, plan, mode}` as JSON on
   stdin and writes the report JSON on stdout. The contract is documented in
   `runners/CONTRACT.md`, and `ts_runner.mjs` is ~300 lines of reference.
2. A **row here**: how to run it, which image, how its types are spelled, how a
   function is written.
3. A **container image** with that runtime, if you want it sandboxed.

The type map is data because that is what keeps starter-code generation honest:
the neutral signature is inferred from the test data (see
`_harness/signature.py`), so a new language renders every existing problem
without anyone writing 342 stubs by hand.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .settings import settings

RUNNERS = Path(__file__).resolve().parent / "runners"


@dataclass(frozen=True)
class Language:
    id: str
    label: str
    ext: str                       # solution.<ext>
    monaco: str                    # Monaco's language id
    driver: Optional[str]          # file in runners/, None = not implemented yet
    runtime: str                   # "python" | "node" | ...
    #: argv to run the driver. `{driver}` and `{workdir}` are substituted.
    command: List[str] = field(default_factory=list)
    #: Neutral type name -> how this language spells it.
    types: Dict[str, str] = field(default_factory=dict)
    #: How a list of T is written. `{0}` is the element type.
    list_form: str = "{0}[]"
    dict_form: str = "Record<{0}, {1}>"
    comment: str = "//"
    #: Template for a function stub. Placeholders: name, params, ret, body.
    function_form: str = ""
    param_form: str = "{name}: {type}"
    #: How the return type is spelled where `{ret}` sits in `function_form`.
    #: Trailing-position languages want ": {0}" or " -> {0}"; languages that put
    #: the type before the name just want "{0}". Data, not a branch in codegen.
    return_form: str = "{0}"
    #: Value returned by an untouched stub, per neutral return type.
    placeholders: Dict[str, str] = field(default_factory=dict)
    docker_image: str = ""
    #: Explains a gap rather than leaving the UI to say "soon" forever.
    todo: str = ""

    @property
    def implemented(self) -> bool:
        return self.driver is not None


# --------------------------------------------------------------- the table

_TS_TYPES = {"int": "number", "float": "number", "bool": "boolean",
             "string": "string", "any": "unknown", "void": "void"}
_TS_PLACEHOLDERS = {"int": "0", "float": "0", "bool": "false", "string": '""',
                    "list": "[]", "dict": "{}", "any": "null", "void": ""}

_NODE_COMMAND = ["node", "--experimental-strip-types", "--no-warnings",
                 "{driver}", "{workdir}"]

LANGUAGES: List[Language] = [
    Language(
        id="python", label="Python 3", ext="py", monaco="python",
        driver="child_runner.py", runtime="python",
        command=["{python}", "-I", "{driver}", "{python_root}"],
        types={"int": "int", "float": "float", "bool": "bool", "string": "str",
               "any": "Any", "void": "None"},
        list_form="List[{0}]", dict_form="Dict[{0}, {1}]", comment="#",
        function_form="def {name}({params}){ret}:\n{body}",
        param_form="{name}: {type}",
        placeholders={"int": "0", "float": "0.0", "bool": "False",
                      "string": '""', "list": "[]", "dict": "{}",
                      "any": "None", "void": "None"},
        docker_image="forge-runner:latest",
        return_form=" -> {0}",
    ),
    Language(
        id="typescript", label="TypeScript", ext="mts", monaco="typescript",
        driver="ts_runner.mjs", runtime="node", command=_NODE_COMMAND,
        types=_TS_TYPES, placeholders=_TS_PLACEHOLDERS,
        function_form="export function {name}({params}){ret} {{\n{body}\n}}",
        docker_image="forge-runner-node:latest",
        return_form=": {0}",
    ),
    # The same driver, because Node strips the types anyway. This row is the
    # cheapest possible demonstration that the seam is real: one extra table
    # entry, no new code.
    Language(
        id="javascript", label="JavaScript", ext="mjs", monaco="javascript",
        driver="ts_runner.mjs", runtime="node", command=_NODE_COMMAND,
        types={k: "" for k in _TS_TYPES},        # no annotations in JS
        placeholders=_TS_PLACEHOLDERS,
        function_form="export function {name}({params}) {{\n{body}\n}}",
        param_form="{name}",
        docker_image="forge-runner-node:latest",
        return_form="",
    ),
    # Not implemented. Each needs a driver and an image; the type maps are here
    # already so that writing the driver is the only remaining work.
    Language(
        id="java", label="Java", ext="java", monaco="java", driver=None,
        runtime="jvm",
        types={"int": "int", "float": "double", "bool": "boolean",
               "string": "String", "any": "Object", "void": "void"},
        list_form="{0}[]", dict_form="Map<{0}, {1}>",
        function_form="public static {ret} {name}({params}) {{\n{body}\n}}",
        param_form="{type} {name}",
        todo="needs a driver (JSON in, report out) and a JDK image; the type "
             "map is already here",
    ),
    Language(
        id="go", label="Go", ext="go", monaco="go", driver=None, runtime="go",
        types={"int": "int", "float": "float64", "bool": "bool",
               "string": "string", "any": "any", "void": ""},
        list_form="[]{0}", dict_form="map[{0}]{1}", comment="//",
        function_form="func {name}({params}){ret} {{\n{body}\n}}",
        param_form="{name} {type}",
        todo="needs a driver and a Go image",
        return_form=" {0}",
    ),
    Language(
        id="cpp", label="C++", ext="cpp", monaco="cpp", driver=None,
        runtime="native",
        types={"int": "int", "float": "double", "bool": "bool",
               "string": "std::string", "any": "auto", "void": "void"},
        list_form="std::vector<{0}>", dict_form="std::map<{0}, {1}>",
        function_form="{ret} {name}({params}) {{\n{body}\n}}",
        param_form="{type} {name}",
        todo="needs a driver, a compile step and a toolchain image",
    ),
    Language(
        id="rust", label="Rust", ext="rs", monaco="rust", driver=None,
        runtime="native",
        types={"int": "i64", "float": "f64", "bool": "bool",
               "string": "String", "any": "serde_json::Value", "void": "()"},
        list_form="Vec<{0}>", dict_form="HashMap<{0}, {1}>",
        function_form="pub fn {name}({params}){ret} {{\n{body}\n}}",
        param_form="{name}: {type}",
        todo="needs a driver, a compile step and a toolchain image",
        return_form=" -> {0}",
    ),
    Language(
        id="csharp", label="C#", ext="cs", monaco="csharp", driver=None,
        runtime="dotnet",
        types={"int": "int", "float": "double", "bool": "bool",
               "string": "string", "any": "object", "void": "void"},
        list_form="{0}[]", dict_form="Dictionary<{0}, {1}>",
        function_form="public static {ret} {name}({params}) {{\n{body}\n}}",
        param_form="{type} {name}",
        todo="needs a driver and a .NET image",
    ),
]

BY_ID: Dict[str, Language] = {lang.id: lang for lang in LANGUAGES}


def get(language_id: str) -> Optional[Language]:
    return BY_ID.get(language_id)


# ------------------------------------------------------------- availability

_runtime_cache: Dict[str, tuple] = {}


def runtime_available(runtime: str) -> tuple:
    """(usable, detail). Cached: probing spawns a process."""
    if runtime in _runtime_cache:
        return _runtime_cache[runtime]

    if runtime == "python":
        result = (True, "in-process interpreter")
    elif runtime == "node":
        binary = shutil.which("node")
        if not binary:
            result = (False, "node is not on PATH")
        else:
            try:
                out = subprocess.run([binary, "--version"], capture_output=True,
                                     text=True, timeout=8)
                version = (out.stdout or "").strip().lstrip("v")
                major = int(version.split(".")[0]) if version else 0
                # Type stripping landed in 22.6. Below that a .mts file is a
                # syntax error, which would look like the learner's fault.
                result = ((major >= 22, f"node {version}") if major
                          else (False, "could not read node --version"))
                if major and major < 22:
                    result = (False, f"node {version} cannot run TypeScript "
                                     f"(needs 22.6+)")
            except Exception as exc:                        # noqa: BLE001
                result = (False, f"probing node failed: {exc}")
    else:
        result = (False, f"no runtime probe for {runtime!r}")

    _runtime_cache[runtime] = result
    return result


def reset_probe_cache() -> None:
    _runtime_cache.clear()


def status() -> List[Dict[str, object]]:
    """What the UI shows in the language picker, and /api/health reports."""
    out = []
    for lang in LANGUAGES:
        if not lang.implemented:
            usable, detail = False, lang.todo
        elif not (RUNNERS / lang.driver).exists():
            usable, detail = False, f"driver {lang.driver} is missing"
        else:
            usable, detail = runtime_available(lang.runtime)
        out.append({
            "id": lang.id, "label": lang.label, "ext": lang.ext,
            "monaco": lang.monaco, "runtime": lang.runtime,
            "available": bool(usable), "detail": detail,
        })
    return out


def resolve_command(lang: Language, *, driver: str, python_root: str,
                    workdir: str, python: str) -> List[str]:
    """
    Fill a language's argv template.

    Keeping the command as data with named holes is what lets one backend launch
    Python, Node or a future compiler without knowing anything about them.
    """
    subs = {"driver": driver, "python_root": python_root,
            "workdir": workdir, "python": python}
    out: List[str] = []
    for part in lang.command:
        for key, value in subs.items():
            part = part.replace("{" + key + "}", value)
        out.append(part)
    return out


def image_for(lang: Language) -> str:
    """The container image, overridable per runtime for deployment."""
    if lang.runtime == "python":
        return settings.docker_image
    return lang.docker_image or settings.docker_image
