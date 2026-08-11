"""
Logging, request ids, the exception boundary, and response headers.

The goal is that a production incident is diagnosable from the logs alone. Three
things make that true, and none of them existed before:

* **A request id on every log line and every response.** When someone reports
  "submitting failed at about 3pm", the id in their network tab finds the exact
  request, including the traceback, without grepping by timestamp.
* **An exception boundary.** An unhandled error returns a generic 500 with that
  id and logs the traceback server-side. Previously a bug would have returned
  Starlette's default 500 with nothing logged -- and with `debug` on, a
  traceback to the browser.
* **Structured output when it matters.** JSON in production so a log shipper can
  index it; human-readable lines in development so a terminal stays readable.

Response headers are here too, because they are part of the same "what does the
outside world see" concern.
"""

from __future__ import annotations

import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar
from typing import Any, Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .settings import settings

#: The current request's id, readable from anywhere without threading it
#: through every function signature.
request_id: ContextVar[str] = ContextVar("request_id", default="-")

REQUEST_ID_HEADER = "X-Request-ID"

log = logging.getLogger("forge")


# ------------------------------------------------------------------ logging

class _RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


class JsonFormatter(logging.Formatter):
    """One JSON object per line: what a log shipper wants."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "requestId": getattr(record, "request_id", "-"),
        }
        for key, value in getattr(record, "extra_fields", {}).items():
            payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


class TextFormatter(logging.Formatter):
    """Readable in a terminal, with the request id kept short."""

    def format(self, record: logging.LogRecord) -> str:
        rid = getattr(record, "request_id", "-")
        short = rid[:8] if rid != "-" else "--------"
        base = (f"{self.formatTime(record, '%H:%M:%S')} {record.levelname:<7} "
                f"{short} {record.name:<12} {record.getMessage()}")
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def configure_logging() -> None:
    """Install our handler as the only one, including for uvicorn's loggers."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter() if settings.log_json
                         else TextFormatter())
    handler.addFilter(_RequestIdFilter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(settings.log_level)

    # uvicorn installs its own handlers; without this every line appears twice,
    # once in our format and once in theirs.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        target = logging.getLogger(name)
        target.handlers = []
        target.propagate = True
    # The access log is redundant: RequestLogMiddleware below records the same
    # requests with a request id and a duration attached.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def log_with(logger: logging.Logger, level: int, message: str, **fields: Any) -> None:
    """Log with structured extras that the JSON formatter will include."""
    logger.log(level, message, extra={"extra_fields": fields})


# --------------------------------------------------------------- middleware

class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Assign a request id, echo it back, and log the outcome with a duration.

    An inbound `X-Request-ID` is honoured so a reverse proxy's id is preserved
    end to end -- but it is sanitised, because it lands in log lines and an
    unbounded caller-controlled string in a log is how log injection works.
    """

    async def dispatch(self, request: Request,
                       call_next: Callable[[Request], Awaitable[Response]]
                       ) -> Response:
        inbound = request.headers.get(REQUEST_ID_HEADER, "")
        clean = "".join(c for c in inbound if c.isalnum() or c in "-_")[:64]
        rid = clean or uuid.uuid4().hex[:16]
        token = request_id.set(rid)
        started = time.perf_counter()
        # The reset has to wrap the logging too. Resetting in a `finally` around
        # `call_next` alone put every access-log line back to the default "-",
        # which quietly made the whole request-id mechanism useless.
        try:
            try:
                response = await call_next(request)
            except Exception:
                # main.py's handler turns this into a 500; log here so the
                # duration and path are attached even if it never gets there.
                log_with(log, logging.ERROR, "request failed",
                         method=request.method, path=request.url.path,
                         durationMs=round((time.perf_counter() - started) * 1000, 1))
                raise

            duration = (time.perf_counter() - started) * 1000
            response.headers[REQUEST_ID_HEADER] = rid
            if settings.log_requests and not _is_noise(request, response):
                level = (logging.WARNING if response.status_code >= 500
                         else logging.INFO)
                log_with(log, level, f"{request.method} {request.url.path} "
                                     f"{response.status_code} "
                                     f"{duration:.0f}ms",
                         method=request.method, path=request.url.path,
                         status=response.status_code,
                         durationMs=round(duration, 1))
            return response
        finally:
            request_id.reset(token)


def _is_noise(request: Request, response: Response) -> bool:
    """Health checks succeed thousands of times a day and say nothing."""
    return (request.url.path == "/api/health"
            and response.status_code < 400)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Headers that cost nothing and close off whole categories of problem.

    No CSP here: this API serves JSON, and the frontend is served by Vite in
    development or by a static host in production -- a CSP declared on the API
    would apply to nothing and give false assurance. It belongs on whatever
    serves index.html.
    """

    async def dispatch(self, request: Request,
                       call_next: Callable[[Request], Awaitable[Response]]
                       ) -> Response:
        response = await call_next(request)
        headers = response.headers
        # Stop a browser from guessing a JSON response is HTML and running it.
        headers.setdefault("X-Content-Type-Options", "nosniff")
        headers.setdefault("Referrer-Policy", "no-referrer")
        headers.setdefault("X-Frame-Options", "DENY")
        headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        headers.setdefault("Permissions-Policy",
                           "geolocation=(), microphone=(), camera=()")
        # Never let a proxy or browser cache a per-account response.
        if request.url.path.startswith("/api/"):
            headers.setdefault("Cache-Control", "no-store")
        if settings.is_prod and request.url.scheme == "https":
            headers.setdefault("Strict-Transport-Security",
                               "max-age=31536000; includeSubDomains")
        return response


class BodyLimitMiddleware(BaseHTTPMiddleware):
    """
    Reject oversized bodies before they are read into memory.

    `Content-Length` is checked first because it is free. A chunked request has
    no length, so the read itself is capped as well -- otherwise the check is
    trivially bypassed by omitting the header.
    """

    async def dispatch(self, request: Request,
                       call_next: Callable[[Request], Awaitable[Response]]
                       ) -> Response:
        limit = settings.max_body_bytes
        declared = request.headers.get("content-length")
        if declared:
            try:
                if int(declared) > limit:
                    return _too_large(limit)
            except ValueError:
                return JSONResponse({"detail": "invalid Content-Length"},
                                    status_code=400)
        elif request.method in ("POST", "PUT", "PATCH"):
            body = await request.body()
            if len(body) > limit:
                return _too_large(limit)
        return await call_next(request)


def _too_large(limit: int) -> JSONResponse:
    return JSONResponse(
        {"detail": f"request body exceeds {limit} bytes"},
        status_code=413,
        headers={REQUEST_ID_HEADER: request_id.get()},
    )


# ---------------------------------------------------------- error boundary

def install_exception_handlers(app) -> None:
    """
    Never leak an internal error to a client, always leave one in the log.

    The response carries the request id so a user can quote it and it can be
    found immediately -- which is the whole reason the id exists.
    """
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        # 4xx is the client's business and is not logged at error level; 5xx is
        # ours and is.
        if exc.status_code >= 500:
            log_with(log, logging.ERROR, f"http {exc.status_code}: {exc.detail}",
                     path=request.url.path)
        return JSONResponse(
            {"detail": exc.detail, "requestId": request_id.get()},
            status_code=exc.status_code,
            headers={**(exc.headers or {}), REQUEST_ID_HEADER: request_id.get()},
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError):
        # Pydantic's default 422 body is a nested structure the UI would have to
        # parse. Flatten it to the same {"detail": str} shape as every other
        # error so one code path in the frontend handles all of them.
        first = exc.errors()[0] if exc.errors() else {}
        field = ".".join(str(p) for p in first.get("loc", [])[1:]) or "request"
        message = first.get("msg", "invalid request")
        return JSONResponse(
            {"detail": f"{field}: {message}", "requestId": request_id.get()},
            status_code=422,
            headers={REQUEST_ID_HEADER: request_id.get()},
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        log.exception("unhandled exception on %s %s",
                      request.method, request.url.path)
        detail = "internal server error"
        if settings.debug:
            # Only in development, and only because chasing a 500 without it is
            # miserable. Production never sees this.
            detail = f"{type(exc).__name__}: {exc}"
        return JSONResponse(
            {"detail": detail, "requestId": request_id.get()},
            status_code=500,
            headers={REQUEST_ID_HEADER: request_id.get()},
        )
