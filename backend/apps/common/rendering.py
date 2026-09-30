"""One response envelope for every endpoint: {"data": ...} or {"data": [...], "meta": {...}}."""

from typing import Any

from rest_framework.renderers import JSONRenderer


class ApiEnvelopeRenderer(JSONRenderer):
    def render(
        self, data: Any, accepted_media_type: str | None = None, renderer_context: Any = None
    ) -> bytes:
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")

        if isinstance(data, dict) and {"results", "next", "previous"} <= data.keys():
            # DRF's paginated shape -> our envelope shape.
            envelope: Any = {
                "data": data["results"],
                "meta": {"next": data.get("next"), "previous": data.get("previous")},
            }
        elif response is not None and response.exception:
            envelope = data  # already shaped by api_exception_handler
        else:
            envelope = {"data": data}
        return super().render(envelope, accepted_media_type, renderer_context)
