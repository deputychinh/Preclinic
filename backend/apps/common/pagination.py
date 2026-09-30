"""Keyset (cursor) pagination for large tables (DS-07, NFR-05). Never OFFSET n at scale."""

from rest_framework.pagination import CursorPagination


class KeysetPagination(CursorPagination):
    # DRF's CursorPagination accepts str or tuple[str, ...] for `ordering` at runtime; its stub only
    # types it as str, so subclasses using a tuple need the wider annotation here.
    ordering: str | tuple[str, ...] = "-created_at"  # overridden per-view where a more specific key is needed
    page_size = 25
    max_page_size = 100
    cursor_query_param = "cursor"


class PatientKeysetPagination(KeysetPagination):
    """Cursor on (last_name, id): stable, index-backed, alphabetical roster order."""

    ordering = ("last_name", "id")


class AuditKeysetPagination(KeysetPagination):
    ordering = "-created_at"
