from typing import cast

from rest_framework.generics import ListAPIView

from apps.accounts.models import User
from apps.audit.selectors import search_audit_events
from apps.audit.serializers import AuditEventSerializer
from apps.common.pagination import AuditKeysetPagination
from apps.common.permissions import IsComplianceOfficer


class AuditEventListView(ListAPIView):
    """NFR-06: searchable, exportable audit log for compliance officers (B6)."""

    serializer_class = AuditEventSerializer
    permission_classes = [IsComplianceOfficer]
    pagination_class = AuditKeysetPagination

    def get_queryset(self):  # type: ignore[no-untyped-def]
        filters = {
            "patient_id": self.request.query_params.get("patient_id"),
            "actor_id": self.request.query_params.get("actor_id"),
            "action": self.request.query_params.get("action"),
            "break_glass_only": self.request.query_params.get("break_glass_only") == "true",
        }
        user = cast(User, self.request.user)
        return search_audit_events(user=user, filters=filters)
