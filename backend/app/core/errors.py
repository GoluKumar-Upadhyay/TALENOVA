"""Shared API error response types and exception handlers."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


class DomainError(Exception):
    """An expected business-rule failure safe to expose to API clients."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def error_body(code: str, message: str, details: Any = None) -> dict[str, Any]:
    """Create the common machine-readable error envelope."""

    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }


def register_exception_handlers(application: FastAPI) -> None:
    """Register consistent public exception responses on an application."""

    @application.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request,
        error: DomainError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content=error_body("domain_error", error.message),
        )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        error: RequestValidationError,
    ) -> JSONResponse:
        import json as _json

        def _safe(obj):
            """Recursively make Pydantic error details JSON-serializable."""
            if isinstance(obj, dict):
                return {k: _safe(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [_safe(v) for v in obj]
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            return str(obj)  # catches ValueError, Exception, etc.

        safe_errors = _safe(error.errors())
        return JSONResponse(
            status_code=422,
            content=error_body("validation_error", "Request validation failed", safe_errors),
        )

    @application.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request,
        error: IntegrityError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content=error_body("integrity_error", "The requested change conflicts with existing data"),
        )
