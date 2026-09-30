"""DS-04: audit-as-transaction-participant. `record_access` must be called inside the same
`transaction.atomic()` block as the PHI read/write it documents, so a rolled-back access never
leaves an orphaned audit row and a committed access is never left unaudited."""

from typing import Any

from django.db import transaction

from apps.accounts.models import User
from apps.audit.models import AuditEvent
from apps.common.enums import AuditAction


def record_access(
    *,
    actor: User,
    action: AuditAction,
    resource_type: str,
    resource_id: str,
    patient_id: str | None = None,
    reason: str = "",
    is_break_glass: bool = False,
    metadata: dict[str, Any] | None = None,
) -> AuditEvent:
    assert transaction.get_connection().in_atomic_block, (
        "record_access must run inside the same transaction as the PHI access it documents"
    )
    return AuditEvent.objects.create(
        actor=actor,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id),
        patient_id=str(patient_id) if patient_id is not None else "",
        reason=reason,
        is_break_glass=is_break_glass,
        metadata=metadata or {},
    )
