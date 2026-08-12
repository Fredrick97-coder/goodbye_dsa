"""
The language layer: registry, signature inference, codegen, and the Node driver.

These tests exist because "add a language" is meant to be a data change. If the
neutral signature model or the codegen quietly acquires a per-language branch,
something here starts failing.
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from app import codegen, languages


# ------------------------------------------------------------------ registry

def test_every_row_is_self_consistent():
    for lang in languages.LANGUAGES:
        assert lang.id and lang.label and lang.ext, lang.id
        assert lang.monaco, lang.id
        # A row with a driver must say how to run it; a row without one must
        # explain what is missing rather than leaving the UI to say "soon".
        if lang.implemented:
            assert lang.command, f"{lang.id} has a driver but no command"
            assert (languages.RUNNERS / lang.driver).exists(), lang.driver
        else:
            assert lang.todo, f"{lang.id} is unimplemented with no explanation"


def test_every_row_can_render_every_neutral_type():
    """A missing type mapping would silently render as `unknown` for a learner."""
    neutral = ["int", "float", "bool", "string", "any", "void",
               "list[int]", "list[list[int]]", "list[string]",
               "dict[string,int]", "tuple[int]"]
    for lang in languages.LANGUAGES:
        for t in neutral:
            rendered = codegen.render_type(t, lang)
            assert "{" not in rendered, f"{lang.id} left a template hole in {t}"
            # Empty is a legitimate rendering: Go and JavaScript spell "no
            # return type" as nothing at all, and JS has no annotations.
            if lang.id == "javascript" or t == "void":
                continue
            assert rendered, f"{lang.id} cannot render {t}"


def test_command_templates_have_no_unfilled_holes():
    for lang in languages.LANGUAGES:
        if not lang.implemented:
            continue
        argv = languages.resolve_command(
            lang, driver="/d", python_root="/r", workdir="/w", python="/p")
        assert argv, lang.id
        for part in argv:
            assert "{" not in part, f"{lang.id}: {part} was not substituted"


def test_python_is_always_available():
    status = {row["id"]: row for row in languages.status()}
    assert status["python"]["available"] is True


# ----------------------------------------------------------------- signature

def _sig(cases, source="", inplace=False):
    sys.path.insert(0, str(__import__("app.settings", fromlist=["settings"])
                          .settings.python_root))
    from _harness import signature
    return signature.build("f", cases, source, inplace).as_dict()


def test_types_are_inferred_from_the_data():
    got = _sig([{"args": ["abc"], "expected": "cba"}])
    assert got["params"][0]["type"] == "string"
    assert got["returns"] == "string"


def test_int_widens_to_float_when_the_data_says_so():
    got = _sig([{"args": [1], "expected": 1},
                {"args": [2.5], "expected": 2.5}])
    assert got["params"][0]["type"] == "float"


def test_nested_lists_are_inferred():
    got = _sig([{"args": [[[1, 2], [3]]], "expected": [1, 2, 3]}])
    assert got["params"][0]["type"] == "list[list[int]]"
    assert got["returns"] == "list[int]"


def test_bool_is_not_confused_with_int():
    got = _sig([{"args": [[1, 2]], "expected": True}])
    assert got["returns"] == "bool"


def test_annotation_sharpens_an_empty_list_but_cannot_contradict_data():
    source = "def f(xs: List[int]) -> List[int]:\n    pass\n"
    sharpened = _sig([{"args": [[]], "expected": []}], source)
    assert sharpened["params"][0]["type"] == "list[int]"

    # The data says strings; an annotation claiming ints must not win.
    lying = "def f(xs: List[int]) -> List[int]:\n    pass\n"
    got = _sig([{"args": [["a"]], "expected": ["a"]}], lying)
    assert got["params"][0]["type"] == "list[string]"


def test_parameter_names_come_from_the_python_source():
    source = "def f(haystack: str, needle: str) -> int:\n    pass\n"
    got = _sig([{"args": ["abc", "b"], "expected": 1}], source)
    assert [p["name"] for p in got["params"]] == ["haystack", "needle"]


def test_inplace_returns_void():
    got = _sig([{"args": [[3, 1]], "expected": [1, 3]}], inplace=True)
    assert got["returns"] == "void"


# ------------------------------------------------------------------- codegen

@pytest.mark.parametrize("lang_id", ["python", "typescript", "javascript",
                                     "java", "go", "rust", "cpp", "csharp"])
def test_stub_renders_for_every_language(lang_id):
    lang = languages.get(lang_id)
    signature = {"name": "merge", "returns": "list[int]", "inplace": False,
                 "params": [{"name": "a", "type": "list[int]"},
                            {"name": "b", "type": "list[int]"}], "doc": ""}
    stub = codegen.stub_for(signature, lang)
    assert "merge" in stub
    assert "{" not in stub.split("\n")[0].replace("{{", "") or lang.comment in stub
    # every stub must mention both parameters
    assert "a" in stub and "b" in stub


def test_typescript_stub_compiles_shape():
    lang = languages.get("typescript")
    signature = {"name": "count", "returns": "int", "inplace": False,
                 "params": [{"name": "s", "type": "string"}], "doc": ""}
    stub = codegen.stub_for(signature, lang)
    assert stub.startswith("export function count(s: string): number {")
    assert "return 0;" in stub          # a placeholder so the file runs as given


def test_placeholders_match_the_return_type():
    ts = languages.get("typescript")
    assert codegen.placeholder_for("string", ts) == '""'
    assert codegen.placeholder_for("list[int]", ts) == "[]"
    assert codegen.placeholder_for("bool", ts) == "false"


# --------------------------------------------------------------- the driver

NODE_AVAILABLE, NODE_DETAIL = languages.runtime_available("node")
needs_node = pytest.mark.skipif(not NODE_AVAILABLE,
                                reason=f"node unusable: {NODE_DETAIL}")

PLAN = {
    "problemId": "00-00",
    "targets": [{
        "name": "reverse_string", "compare": "exact", "tol": None,
        "inplace": False, "note": "",
        "cases": [{"args": ["hello"], "expected": "olleh"},
                  {"args": [""], "expected": ""},
                  {"args": ["ab"], "expected": "ba"}],
    }],
    "excluded": [], "complete": True,
}


def _run_driver(source, tmp_path, mode="test", cpu_seconds=5):
    """Invoke the Node driver exactly as an executor would."""
    path = tmp_path / "solution.mts"
    path.write_text(source, encoding="utf-8")
    job = json.dumps({"source": source, "sourceFile": str(path), "plan": PLAN,
                      "mode": mode, "cpuSeconds": cpu_seconds, "memoryMb": 256})
    lang = languages.get("typescript")
    argv = languages.resolve_command(
        lang, driver=str(languages.RUNNERS / lang.driver),
        python_root="", workdir=str(tmp_path), python=sys.executable)
    proc = subprocess.run(argv, input=job, capture_output=True, text=True,
                          timeout=60)
    assert proc.stdout.strip(), f"driver wrote nothing; stderr={proc.stderr[:300]}"
    return json.loads(proc.stdout)


@needs_node
def test_driver_accepts_a_correct_solution(tmp_path):
    report = _run_driver(
        'export function reverse_string(s: string): string {\n'
        '  return [...s].reverse().join("");\n}\n', tmp_path)
    assert report["targets"][0]["status"] == "PASS"
    assert report["targets"][0]["passed"] == 3


@needs_node
def test_driver_accepts_the_camelcase_name(tmp_path):
    report = _run_driver(
        'export function reverseString(s: string): string {\n'
        '  return [...s].reverse().join("");\n}\n', tmp_path)
    assert report["targets"][0]["status"] == "PASS"


@needs_node
def test_driver_reports_a_wrong_answer_with_detail(tmp_path):
    report = _run_driver(
        'export function reverse_string(s: string): string { return s; }\n',
        tmp_path)
    target = report["targets"][0]
    assert target["status"] == "FAIL"
    assert any('"olleh"' in c["expected"] for c in target["cases"])


@needs_node
def test_untouched_starter_is_not_attempted_not_wrong(tmp_path):
    """The placeholder return is a value, so this cannot be detected by output."""
    lang = languages.get("typescript")
    starter = codegen.stub_for(
        {"name": "reverse_string", "returns": "string", "inplace": False,
         "params": [{"name": "s", "type": "string"}], "doc": ""}, lang)
    report = _run_driver(starter, tmp_path)
    assert report["targets"][0]["status"] == "STUB"


@needs_node
def test_missing_export_says_so(tmp_path):
    report = _run_driver(
        'function reverse_string(s: string): string { return s; }\n', tmp_path)
    assert report["targets"][0]["status"] == "MISSING"


@needs_node
def test_syntax_error_is_a_compile_error(tmp_path):
    report = _run_driver('export function reverse_string(s: string {\n}\n',
                         tmp_path)
    assert report["compileError"]["type"] == "SyntaxError"


@needs_node
def test_printing_does_not_corrupt_the_report(tmp_path):
    report = _run_driver(
        'export function reverse_string(s: string): string {\n'
        '  console.log("chatty");\n  return [...s].reverse().join("");\n}\n',
        tmp_path)
    assert report["targets"][0]["status"] == "PASS"
    assert "chatty" in report["stdout"]


@needs_node
def test_an_infinite_loop_hits_the_time_limit(tmp_path):
    """
    The reason grading runs in a worker thread.

    A tight loop blocks the event loop, so a same-thread watchdog never fires and
    the submission ran until the container backstop instead.
    """
    report = _run_driver(
        'export function reverse_string(s: string): string { while (true) {} }\n',
        tmp_path, cpu_seconds=2)
    assert report["compileError"]["type"] == "TimeLimit"


@needs_node
def test_process_exit_is_named_not_reported_as_a_crash(tmp_path):
    report = _run_driver(
        'export function reverse_string(s: string): string {\n'
        '  process.exit(0);\n}\n', tmp_path)
    assert report["compileError"]["type"] == "Aborted"


@needs_node
@pytest.mark.parametrize("mode,expected", [("run", "RAN")])
def test_run_mode_executes_without_grading(tmp_path, mode, expected):
    report = _run_driver('console.log("hi");\nexport function reverse_string(s: string) '
                         '{ return s; }\n', tmp_path, mode=mode)
    assert report["targets"][0]["status"] == expected
    assert "hi" in report["stdout"]


@needs_node
def test_comparison_modes_match_the_python_normalisers(tmp_path):
    """`sorted` must mean the same thing in both runners, or grading diverges."""
    plan = dict(PLAN)
    plan["targets"] = [{
        "name": "pairs", "compare": "sorted_pairs", "tol": None,
        "inplace": False, "note": "",
        "cases": [{"args": [[1, 2, 3]], "expected": [[0, 2], [1, 1]]}],
    }]
    path = tmp_path / "solution.mts"
    source = ('export function pairs(xs: number[]): number[][] {\n'
              '  return [[1, 1], [0, 2]];\n}\n')          # same set, other order
    path.write_text(source, encoding="utf-8")
    job = json.dumps({"source": source, "sourceFile": str(path), "plan": plan,
                      "mode": "test", "cpuSeconds": 5, "memoryMb": 256})
    lang = languages.get("typescript")
    argv = languages.resolve_command(
        lang, driver=str(languages.RUNNERS / lang.driver),
        python_root="", workdir=str(tmp_path), python=sys.executable)
    proc = subprocess.run(argv, input=job, capture_output=True, text=True,
                          timeout=60)
    report = json.loads(proc.stdout)
    assert report["targets"][0]["status"] == "PASS", report["targets"][0]
