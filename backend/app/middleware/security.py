"""Configurable OWASP-aligned HTTP security and observability middleware."""

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import get_settings

logger = logging.getLogger("talenova.http")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Create request state, correlation ids, timings, and structured logs."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Record the request lifecycle without exposing sensitive values."""

        correlation_id = request.headers.get("X-Correlation-ID", str(uuid4()))
        request.state.correlation_id = correlation_id
        request.state.request_started_at = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed = (perf_counter() - request.state.request_started_at) * 1000
            logger.exception(
                "request_failed correlation_id=%s method=%s path=%s duration_ms=%.2f",
                correlation_id,
                request.method,
                request.url.path,
                elapsed,
            )
            raise
        elapsed = (perf_counter() - request.state.request_started_at) * 1000
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["Server-Timing"] = f"app;dur={elapsed:.2f}"
        logger.info(
            "request_completed correlation_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            correlation_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Apply configured browser hardening headers to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Attach safe headers after application response creation."""

        settings = get_settings()
        response = await call_next(request)
        if "server" in response.headers:
            del response.headers["server"]
        response.headers["Content-Security-Policy"] = settings.content_security_policy
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), microphone=(), payment=()"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-site"
        if settings.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                f"max-age={settings.hsts_max_age}; includeSubDomains"
            )
        return response
