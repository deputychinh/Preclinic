from django.db import transaction

from apps.accounts.models import User
from apps.audit.services import record_access
from apps.common.enums import AuditAction, ConsentType
from apps.common.exceptions import ConsentRequiredError
from apps.patients.models import Consent, Patient
from apps.referrals.models import Referral


@transaction.atomic
def create_referral(*, patient: Patient, specialty: str, reason: str, actor: User) -> Referral:
    has_consent = Consent.objects.filter(
        patient=patient, consent_type=ConsentType.DATA_SHARING, revoked_at__isnull=True
    ).exists()
    if not has_consent:
        raise ConsentRequiredError(
            "Patient has no active data-sharing consent", details={"patient_id": patient.id}
        )

    referral = Referral.objects.create(
        patient=patient, referring_clinician=actor, specialty=specialty, reason=reason
    )
    record_access(
        actor=actor,
        action=AuditAction.CREATE,
        resource_type="Referral",
        resource_id=str(referral.id),
        patient_id=str(patient.id),
    )
    return referral
