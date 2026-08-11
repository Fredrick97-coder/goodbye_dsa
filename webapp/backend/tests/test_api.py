"""
The HTTP surface: access tiers, account isolation, and the error contract.

These are the tests that would catch a refactor accidentally making a
user-scoped endpoint public, or dropping the user filter from a query.
"""

from __future__ import annotations

import pytest

PUBLIC_GETS = ["/api/health", "/api/ready", "/api/meta", "/api/problems",
               "/api/problems/03-01", "/api/problems/random"]
PROTECTED_GETS = ["/api/progress", "/api/activity", "/api/submissions",
                  "/api/submissions/1", "/api/bookmarks", "/api/notes/03-01"]


# ---------------------------------------------------------- access tiers

@pytest.mark.parametrize("path", PUBLIC_GETS)
def test_public_endpoints_need_no_account(client, path):
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("path", PROTECTED_GETS)
def test_account_endpoints_reject_anonymous(client, path):
    res = client.get(path)
    assert res.status_code == 401
    assert res.json()["detail"] == "sign in to do that"


def test_anonymous_can_run_but_not_submit(client):
    body = {"problemId": "03-01", "language": "python",
            "source": "print('hello')", "mode": "run"}
    assert client.post("/api/submit", json=body).status_code == 200

    body["mode"] = "test"
    res = client.post("/api/submit", json=body)
    assert res.status_code == 401
    assert "sign in" in res.json()["detail"]


def test_signed_in_can_submit_and_it_is_recorded(account):
    client, _, _ = account
    res = client.post("/api/submit", json={
        "problemId": "03-01", "language": "python",
        "source": "def reverse_string(s):\n    return s[::-1]\n",
        "mode": "test"})
    assert res.status_code == 200
    body = res.json()
    assert body["summary"]["verdict"] == "accepted"
    assert isinstance(body["submissionId"], int)
    assert client.get("/api/progress").json()["totals"]["solved"] == 1


def test_running_is_never_recorded(account):
    client, _, _ = account
    client.post("/api/submit", json={"problemId": "03-01", "language": "python",
                                     "source": "print(1)", "mode": "run"})
    assert client.get("/api/submissions").json() == []


def test_submitting_untouched_starter_code_is_not_recorded(account):
    """`stub` means "not attempted", and history should not fill up with it."""
    client, _, _ = account
    res = client.post("/api/submit", json={
        "problemId": "03-01", "language": "python",
        "source": "def reverse_string(s):\n    pass\n", "mode": "test"})
    assert res.json()["summary"]["verdict"] == "stub"
    assert res.json()["submissionId"] is None
    assert client.get("/api/submissions").json() == []


# ------------------------------------------------------------- isolation

def test_accounts_cannot_see_each_other(client):
    first = client.post("/api/auth/register",
                        json={"email": "one@example.com", "password": "password one"})
    assert first.status_code == 200
    client.post("/api/submit", json={
        "problemId": "03-01", "language": "python",
        "source": "def reverse_string(s):\n    return s[::-1]\n", "mode": "test"})
    client.post("/api/bookmarks/05-01")
    client.put("/api/notes/03-01", json={"body": "mine"})
    mine = client.get("/api/submissions").json()[0]["id"]
    client.post("/api/auth/logout")

    client.post("/api/auth/register",
                json={"email": "two@example.com", "password": "password two"})
    assert client.get("/api/progress").json()["totals"]["solved"] == 0
    assert client.get("/api/submissions").json() == []
    assert client.get("/api/bookmarks").json() == []
    assert client.get("/api/notes/03-01").json()["body"] == ""
    # The other account's submission is not merely hidden -- it is not found.
    assert client.get(f"/api/submissions/{mine}").status_code == 404
    assert client.get("/api/problems/03-01").json()["status"] == "todo"


def test_problem_list_is_neutral_when_anonymous(client):
    for problem in client.get("/api/problems").json():
        assert problem["status"] == "todo"
        assert problem["bookmarked"] is False
        assert problem["hasNote"] is False
        assert problem["attempts"] == 0


# ------------------------------------------------------------ auth routes

def test_register_login_logout_cycle(client):
    email, password = "cycle@example.com", "a long enough password"
    assert client.post("/api/auth/register",
                       json={"email": email, "password": password}).status_code == 200
    assert client.get("/api/auth/me").json()["user"]["email"] == email
    client.post("/api/auth/logout")
    assert client.get("/api/auth/me").json()["user"] is None
    assert client.post("/api/auth/login",
                       json={"email": email, "password": password}).status_code == 200
    assert client.get("/api/auth/me").json()["user"]["email"] == email


def test_duplicate_registration_is_refused_case_insensitively(client):
    client.post("/api/auth/register",
                json={"email": "dup@example.com", "password": "password here"})
    res = client.post("/api/auth/register",
                      json={"email": "DUP@example.com", "password": "password here"})
    assert res.status_code == 409


def test_login_failures_are_indistinguishable(client):
    client.post("/api/auth/register",
                json={"email": "real@example.com", "password": "the real password"})
    client.post("/api/auth/logout")
    unknown = client.post("/api/auth/login",
                          json={"email": "ghost@example.com", "password": "whatever"})
    wrong = client.post("/api/auth/login",
                        json={"email": "real@example.com", "password": "whatever"})
    assert unknown.status_code == wrong.status_code == 401
    assert unknown.json()["detail"] == wrong.json()["detail"]


def test_password_change_invalidates_other_sessions(client, env):
    """The whole point of changing a password after losing a device."""
    from fastapi.testclient import TestClient
    from app.main import app

    email, password = "multi@example.com", "first password here"
    client.post("/api/auth/register", json={"email": email, "password": password})

    other = TestClient(app, base_url="http://localhost")
    other.post("/api/auth/login", json={"email": email, "password": password})
    assert other.get("/api/auth/me").json()["user"] is not None

    res = client.post("/api/auth/password",
                      json={"currentPassword": password,
                            "newPassword": "second password here"})
    assert res.status_code == 200
    assert client.get("/api/auth/me").json()["user"] is not None   # this device
    assert other.get("/api/auth/me").json()["user"] is None        # the other one


def test_wrong_current_password_is_refused(account):
    client, _, password = account
    assert client.post("/api/auth/password",
                       json={"currentPassword": "not it",
                             "newPassword": "a new long password"}
                       ).status_code == 401


def test_forged_session_cookie_is_rejected(client, env):
    client.cookies.set(env.settings.cookie_name, "not-a-real-token")
    assert client.get("/api/progress").status_code == 401


def test_rate_limit_returns_429_with_retry_after(client, env):
    client.post("/api/auth/register",
                json={"email": "limited@example.com", "password": "the password"})
    client.post("/api/auth/logout")
    codes = []
    for _ in range(env.settings.rate_max_attempts + 2):
        res = client.post("/api/auth/login",
                          json={"email": "limited@example.com", "password": "wrong"})
        codes.append(res.status_code)
        if res.status_code == 429:
            assert "Retry-After" in res.headers
            break
    assert 429 in codes


# -------------------------------------------------------- error contract

def test_errors_always_have_a_detail_string_and_request_id(client):
    for res in (client.get("/api/problems/99-99"),
                client.get("/api/progress"),
                client.post("/api/auth/register", json={"email": "x", "password": "y"}),
                client.post("/api/auth/register", json={})):
        body = res.json()
        assert isinstance(body.get("detail"), str), body
        assert body.get("requestId"), body
        assert res.headers.get("X-Request-ID")


def test_request_id_is_echoed_when_supplied(client):
    res = client.get("/api/meta", headers={"X-Request-ID": "trace-me-123"})
    assert res.headers["X-Request-ID"] == "trace-me-123"


def test_request_id_from_a_client_is_sanitised(client):
    """It lands in log lines, so it cannot carry newlines or control bytes."""
    res = client.get("/api/meta",
                     headers={"X-Request-ID": "bad\r\nInjected: header"})
    echoed = res.headers["X-Request-ID"]
    assert "\n" not in echoed and "\r" not in echoed and " " not in echoed


def test_security_headers_are_present(client):
    headers = client.get("/api/meta").headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["Referrer-Policy"] == "no-referrer"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Cache-Control"] == "no-store"


def test_oversized_body_is_rejected_before_handling(client, env):
    res = client.post("/api/submit", json={
        "problemId": "03-01", "language": "python", "mode": "run",
        "source": "x" * (env.settings.max_body_bytes + 100)})
    assert res.status_code == 413


def test_cross_origin_mutation_is_refused(account):
    client, _, _ = account
    assert client.post("/api/bookmarks/03-01",
                       headers={"Origin": "https://evil.example"}
                       ).status_code == 403
    assert client.post("/api/bookmarks/03-01",
                       headers={"Origin": "http://localhost:5173"}
                       ).status_code == 200


def test_unknown_language_is_refused_clearly(account):
    client, _, _ = account
    res = client.post("/api/submit", json={
        "problemId": "03-01", "language": "java", "source": "x", "mode": "test"})
    assert res.status_code == 400
    assert "only Python" in res.json()["detail"]


def test_health_reports_the_executor_and_schema(client):
    body = client.get("/api/health").json()
    assert body["status"] == "ok"
    assert body["db"]["schemaVersion"] == body["db"]["expectedVersion"]
    assert body["config"]["executor"] in ("local", "seatbelt", "docker")


def test_access_log_lines_carry_the_request_id(client, caplog):
    """
    Regression: the context variable was reset before the access log was
    written, so every line said "-" and the ids were useless for tracing.
    """
    import logging
    with caplog.at_level(logging.INFO, logger="forge"):
        from app.settings import settings
        object.__setattr__(settings, "log_requests", True)
        try:
            res = client.get("/api/meta", headers={"X-Request-ID": "abc123"})
        finally:
            object.__setattr__(settings, "log_requests", False)

    assert res.headers["X-Request-ID"] == "abc123"
    records = [r for r in caplog.records if "/api/meta" in r.getMessage()]
    assert records, "the request was not logged at all"
    assert getattr(records[0], "request_id", "-") == "abc123"
