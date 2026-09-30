from django.db.models import QuerySet

from apps.accounts.models import User
from apps.audit.models import AuditEvent
from apps.common.enums import Role
from apps.common.exceptions import AppError


class NotComplianceOfficerError(AppError):
    status_code = 403
    code = "FORBIDDEN"


def search_audit_events(*, user: User, filters: dict) -> QuerySet[AuditEvent]:
    if user.role != Role.COMPLIANCE_OFFICER:
        raise NotComplianceOfficerError("Only compliance officers may search the audit log")

    qs = AuditEvent.objects.select_related("actor").all()
    if patient_id := filters.get("patient_id"):
        qs = qs.filter(patient_id=patient_id)
    if actor_id := filters.get("actor_id"):
        qs = qs.filter(actor_id=actor_id)
    if action := filters.get("action"):
        qs = qs.filter(action=action)
    if filters.get("break_glass_only"):
        qs = qs.filter(is_break_glass=True)
    return qs
