"""
Shared fixtures.

Two things matter here:

* **Every test gets its own database file.** A shared one makes tests order
  dependent, and an order-dependent auth test is worse than no auth test.
* **scrypt is turned down to 2^12 for tests only.** At the production 2^15 the
  suite spends most of its wall clock hashing passwords, which makes people stop
  running it. The parameter is stored inside each hash, so this exercises the
  same code path -- and `test_password_params_are_recorded` asserts production
  really does use 2^15.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """A fresh, isolated app configuration. Returns the settings module."""
    monkeypatch.setenv("FORGE_SKIP_DOTENV", "1")
    monkeypatch.setenv("FORGE_ENV", "dev")
    monkeypatch.setenv("FORGE_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("FORGE_SCRYPT_N", str(2 ** 12))
    monkeypatch.setenv("FORGE_EXECUTOR", "local")
    monkeypatch.setenv("FORGE_LOG_LEVEL", "WARNING")
    monkeypatch.setenv("FORGE_LOG_REQUESTS", "0")
    monkeypatch.setenv("FORGE_RATE_MAX_ATTEMPTS", "4")

    # Reload the whole app package: settings are read at import time on purpose
    # (a server should not change configuration under itself), so a test that
    # wants different settings has to re-import.
    for name in [n for n in list(sys.modules) if n.startswith("app")]:
        del sys.modules[name]
    from app import settings as config
    importlib.reload(config)
    return config


@pytest.fixture()
def database(env):
    from app import db
    db.close_all()
    db.init()
    yield db
    db.close_all()


@pytest.fixture()
def client(env):
    """A TestClient on http://localhost, so Secure-cookie logic behaves."""
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app, base_url="http://localhost") as c:
        yield c


def _unlock_all(client) -> None:
    """
    Grant every module, for tests that are not about progression.

    Kept explicit rather than folded into the `account` fixture: a test that
    submits to problem 03-01 should say out loud that it needed the gate opened,
    otherwise the next person to add a test cannot tell whether the lock applies.
    """
    from app import content
    for module in content.get("dsa").modules:
        client.post(f"/api/courses/dsa/modules/{module.id}/unlock")


@pytest.fixture
def open_account(account):
    """A signed-in account with the whole course unlocked."""
    client, email, password = account
    _unlock_all(client)
    return client, email, password


@pytest.fixture
def account(client):
    """A registered, signed-in account. Returns (client, email, password)."""
    email, password = "learner@example.com", "a sufficiently long password"
    res = client.post("/api/auth/register",
                      json={"email": email, "password": password,
                            "name": "Learner"})
    assert res.status_code == 200, res.text
    return client, email, password
