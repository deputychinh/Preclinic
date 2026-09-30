"""Standard error envelope: {"error": {"code", "message", "details", "request_id"}}."""

from typing import Any

from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.request_context import get_request_id


class AppError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "CONFLICT"


class ConsentRequiredError(ConflictError):
    code = "CONSENT_REQUIRED"


_CODE_BY_STATUS = {
    400: "VALIDATION_ERROR",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "NOT_FOUND",
    409: "CONFLICT",
    429: "RATE_LIMITED",
}


def _error_response(status_code: int, code: str, message: str, details: Any = None) -> Response:
    return Response(
        {"error": {"code": code, "message": message, "details": details, "request_id": get_request_id()}},
        status=status_code,
    )


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    if isinstance(exc, AppError):
        return _error_response(exc.status_code, exc.code, exc.message, exc.details)

    if isinstance(exc, Http404):
        return _error_response(404, "NOT_FOUND", "Not found")

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, drf_exceptions.ValidationError):
        return _error_response(400, "VALIDATION_ERROR", "Request validation failed", response.data)

    code = _CODE_BY_STATUS.get(response.status_code, "ERROR")
    detail = response.data.get("detail") if isinstance(response.data, dict) else response.data
    return _error_response(response.status_code, code, str(detail), None)
