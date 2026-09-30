from django.db import transaction

from apps.accounts.models import User
from apps.audit.services import record_access
from apps.common.enums import AuditAction, Role
from apps.common.exceptions import AppError
from apps.patients.models import Patient
from apps.patients.selectors import get_patient_for_user


class PatientAccessDeniedError(AppError):
    """404, not 403 (DS-12/B5): never reveal to an unauthorized user whether a patient exists."""

    status_code = 404
    code = "NOT_FOUND"


@transaction.atomic
def get_patient_chart(*, user: User, patient_id: int, break_glass_reason: str = "") -> Patient:
    patient = get_patient_for_user(user=user, patient_id=patient_id)
    is_break_glass = False

    if patient is None:
        if user.role == Role.COMPLIANCE_OFFICER or not break_glass_reason:
            raise PatientAccessDeniedError("Patient not found")
        # B5: break-glass grants access outside the care team, but only with a reason, and it is
        # audited as such below.
        patient = Patient.objects.alive().filter(id=patient_id).first()
        if patient is None:
            raise PatientAccessDeniedError("Patient not found")
        is_break_glass = True

    record_access(
        actor=user,
        action=AuditAction.READ,
        resource_type="Patient",
        resource_id=str(patient.id),
        patient_id=str(patient.id),
        reason=break_glass_reason,
        is_break_glass=is_break_glass,
    )
    return patient
