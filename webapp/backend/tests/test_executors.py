"""
The sandbox: does it grade correctly, and does it actually contain?

Containment tests are skipped rather than failed when a backend is unavailable on
the host, but they are never skipped silently -- pytest reports the reason, so
"all green" cannot hide "the sandbox was never exercised".
"""

from __future__ import annotations

import pytest

GOOD = "def reverse_string(s):\n    return s[::-1]\n"
WRONG = "def reverse_string(s):\n    return s\n"
STUB = "def reverse_string(s):\n    pass\n"
SYNTAX = "def reverse_string(s)\n    return s\n"
CPU_LOOP = "def reverse_string(s):\n    while True:\n        pass\n"

WRITE_HOST = ("def reverse_string(s):\n"
              "    open('/repo/PWNED', 'w').write('x')\n"
              "    return s[::-1]\n")
READ_HOME = ("import os\n"
             "def reverse_string(s):\n"
             "    return open(os.path.expanduser('~/.zshrc')).read()[:5]\n")
NETWORK = ("import socket\n"
           "def reverse_string(s):\n"
           "    socket.create_connection(('1.1.1.1', 53), timeout=3)\n"
           "    return s[::-1]\n")
SPAWN = ("import subprocess\n"
         "def reverse_string(s):\n"
         "    return subprocess.run(['/bin/ls', '/'],\n"
         "                          capture_output=True).stdout.decode()[:4]\n")

SANDBOXED = ["seatbelt", "docker"]


def _run(name, source, topic=3, num=1):
    from app import executors
    from app.executors.base import Job, to_report
    return to_report(executors.get(name).run(Job(source, topic, num)), name)


def _skip_unless_available(name):
    from app import executors
    have = executors.availability()
    if not have.get(name):
        pytest.skip(f"{name} unavailable: {have.get(name + '_reason')}")


# ------------------------------------------------------------- unit level

def test_docker_argv_carries_every_isolation_flag(env):
    from app.executors.docker_exec import build_argv
    argv = build_argv("forge-run-test")
    joined = " ".join(argv)
    for flag in ("--network none", "--read-only", "--cap-drop ALL",
                 "--security-opt no-new-privileges", "--user 65534:65534",
                 "--pids-limit", "--memory", "--memory-swap"):
        assert flag in joined, f"missing {flag}"
    # The curriculum must be mounted read-only, or the sandbox is decorative.
    assert any(a.endswith(":/repo:ro") for a in argv)
    assert "--rm" in argv


def test_docker_memory_and_swap_are_equal(env):
    """Unequal values would let a container swap past its memory cap."""
    from app.executors.docker_exec import build_argv
    argv = build_argv("x")
    memory = argv[argv.index("--memory") + 1]
    swap = argv[argv.index("--memory-swap") + 1]
    assert memory == swap


def test_verdicts_are_derived_consistently(env):
    from app.executors.base import summarise
    assert summarise({"targets": [{"status": "PASS", "passed": 3, "total": 3}]}
                     )["verdict"] == "accepted"
    assert summarise({"targets": [{"status": "STUB", "passed": 0, "total": 3}]}
                     )["verdict"] == "stub"
    assert summarise({"targets": [{"status": "PASS", "passed": 1, "total": 1},
                                  {"status": "FAIL", "passed": 0, "total": 1}]}
                     )["verdict"] == "failed"
    assert summarise({"compileError": {"type": "SyntaxError"}, "targets": []}
                     )["verdict"] == "error"
    assert summarise({"untested": True, "targets": []})["verdict"] == "untested"


def test_source_size_is_capped_before_any_process_starts(env):
    from app.execute import run_submission
    report = run_submission("x" * (env.settings.exec_max_source_bytes + 1), 3, 1)
    assert report["compileError"]["type"] == "SubmissionTooLarge"


# ---------------------------------------------------- grading, per backend

@pytest.mark.parametrize("backend", ["local", "seatbelt", "docker"])
@pytest.mark.parametrize("source,expected", [
    (GOOD, "accepted"), (WRONG, "failed"), (STUB, "stub"), (SYNTAX, "error"),
])
def test_every_backend_grades_identically(env, backend, source, expected):
    """
    A backend that disagreed about a verdict would be a silent grading bug, so
    this is parametrised across all of them rather than testing only the default.
    """
    _skip_unless_available(backend)
    assert _run(backend, source)["summary"]["verdict"] == expected


@pytest.mark.parametrize("backend", ["local", "seatbelt", "docker"])
def test_infinite_loop_is_stopped_and_named(env, backend):
    _skip_unless_available(backend)
    report = _run(backend, CPU_LOOP)
    assert report["summary"]["verdict"] == "error"
    # Never "CrashedSilently": the learner has to be told it was a time limit.
    assert report["compileError"]["type"] in ("TimeLimit", "Timeout")


# --------------------------------------------------------- containment

@pytest.mark.parametrize("backend", SANDBOXED)
def test_sandbox_blocks_writing_to_the_curriculum(env, backend, tmp_path):
    _skip_unless_available(backend)
    report = _run(backend, WRITE_HOST)
    assert report["summary"]["verdict"] in ("error", "failed")
    from app.settings import settings
    assert not (settings.python_root / "PWNED").exists(), "escaped to the host"


@pytest.mark.parametrize("backend", SANDBOXED)
def test_sandbox_blocks_the_network(env, backend):
    _skip_unless_available(backend)
    assert _run(backend, NETWORK)["summary"]["verdict"] in ("error", "failed")


@pytest.mark.parametrize("backend", SANDBOXED)
def test_sandbox_blocks_reading_the_home_directory(env, backend):
    _skip_unless_available(backend)
    assert _run(backend, READ_HOME)["summary"]["verdict"] in ("error", "failed")


@pytest.mark.parametrize("backend", SANDBOXED)
def test_sandbox_blocks_spawning_other_programs(env, backend):
    _skip_unless_available(backend)
    assert _run(backend, SPAWN)["summary"]["verdict"] in ("error", "failed")


def test_local_backend_is_honestly_labelled_unsafe(env):
    """
    It is not a sandbox and must not claim to be -- `check_safety` keys off this.
    """
    from app import executors
    assert executors.is_safe("local") is False
    assert executors.is_safe("docker") is True
    assert executors.is_safe("seatbelt") is True
