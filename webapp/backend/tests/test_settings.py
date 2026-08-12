"""Configuration, and the guards that stop a bad deployment from starting."""

from __future__ import annotations

import importlib
import sys

import pytest


def _reload(monkeypatch, **env):
    monkeypatch.setenv("FORGE_SKIP_DOTENV", "1")
    for key, value in env.items():
        monkeypatch.setenv(f"FORGE_{key}", value)
    for name in [n for n in list(sys.modules) if n.startswith("app")]:
        del sys.modules[name]
    from app import settings as config
    return importlib.reload(config)


def test_defaults_are_development_shaped(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"))
    assert config.settings.env == "dev"
    assert config.settings.debug is True
    assert config.settings.cookie_secure is None        # decided per request
    assert config.settings.allowed_origin_regex is not None


def test_production_refuses_to_guess_allowed_origins(monkeypatch, tmp_path):
    with pytest.raises(Exception) as exc:
        _reload(monkeypatch, ENV="prod", DB_PATH=str(tmp_path / "d.db"))
    assert "ALLOWED_ORIGINS" in str(exc.value)


def test_production_accepts_explicit_origins(monkeypatch, tmp_path):
    config = _reload(monkeypatch, ENV="prod", DB_PATH=str(tmp_path / "d.db"),
                     ALLOWED_ORIGINS="https://forge.example,https://www.forge.example")
    assert config.settings.is_prod
    assert config.settings.debug is False               # never on in prod
    assert len(config.settings.allowed_origins) == 2


def test_samesite_none_without_secure_is_rejected(monkeypatch, tmp_path):
    with pytest.raises(Exception):
        _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"),
                COOKIE_SAMESITE="none", COOKIE_SECURE="false")


def test_bad_values_fail_loudly(monkeypatch, tmp_path):
    for key, value in (("SESSION_DAYS", "not-a-number"),
                       ("ENV", "staging"),
                       ("EXECUTOR", "vm"),
                       ("DEBUG", "maybe")):
        with pytest.raises(Exception):
            _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"), **{key: value})


def test_cookie_secure_is_off_only_for_plain_http_localhost(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"))
    s = config.settings
    assert s.cookie_secure_for("http", "localhost") is False
    assert s.cookie_secure_for("http", "127.0.0.1") is False
    assert s.cookie_secure_for("https", "localhost") is True
    assert s.cookie_secure_for("http", "forge.example") is True   # not localhost


def test_explicit_cookie_secure_wins(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"),
                     COOKIE_SECURE="true")
    assert config.settings.cookie_secure_for("http", "localhost") is True


def test_prod_will_not_start_on_an_unsandboxed_executor(monkeypatch, tmp_path):
    """The guard that matters most: no accidental rollout without isolation."""
    config = _reload(monkeypatch, ENV="prod", DB_PATH=str(tmp_path / "d.db"),
                     ALLOWED_ORIGINS="https://forge.example")
    with pytest.raises(Exception) as exc:
        config.check_safety("local")
    assert "refusing to start" in str(exc.value)

    # ...unless the operator says so, in writing.
    config = _reload(monkeypatch, ENV="prod", DB_PATH=str(tmp_path / "d.db"),
                     ALLOWED_ORIGINS="https://forge.example",
                     ALLOW_UNSAFE_EXECUTOR="1")
    config.check_safety("local")            # no raise

    # Sandboxed executors are always fine.
    for safe in ("docker", "seatbelt"):
        config.check_safety(safe)


def test_dev_tolerates_the_unsafe_executor(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"))
    config.check_safety("local")            # no raise


def test_explicit_executor_that_is_unavailable_is_an_error(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"),
                     EXECUTOR="docker")
    with pytest.raises(Exception) as exc:
        config.resolve_executor({"docker": False,
                                 "docker_reason": "daemon unreachable"})
    assert "daemon unreachable" in str(exc.value)


def test_auto_prefers_the_strongest_available(monkeypatch, tmp_path):
    config = _reload(monkeypatch, DB_PATH=str(tmp_path / "d.db"))
    assert config.resolve_executor(
        {"docker": True, "seatbelt": True}) == "docker"
    assert config.resolve_executor(
        {"docker": False, "seatbelt": True}) == "seatbelt"
    assert config.resolve_executor(
        {"docker": False, "seatbelt": False}) == "local"
