import logging
import time
import uuid

from apps.common.request_context import set_request_id

logger = logging.getLogger("apps.request")


class RequestIdMiddleware:
    """Assigns a request id, echoes it as a header, and logs method/path/status/duration."""

    def __init__(self, get_response):  # type: ignore[no-untyped-def]
        self.get_response = get_response

    def __call__(self, request):  # type: ignore[no-untyped-def]
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        set_request_id(request_id)
        started = time.perf_counter()
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - started) * 1000, 1),
                "request_id": request_id,
            },
        )
        return response
