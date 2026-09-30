from django.db.models import QuerySet

from apps.accounts.models import User
from apps.patients.models import Patient
from apps.patients.selectors import get_patient_for_user
from apps.referrals.models import Referral


def list_referrals_for_patient(*, user: User, patient_id: int) -> QuerySet[Referral]:
    if get_patient_for_user(user=user, patient_id=patient_id) is None:
        return Referral.objects.none()
    return Referral.objects.filter(patient_id=patient_id)


def list_referrals_for_user(*, user: User) -> QuerySet[Referral]:
    """Referral queue across every patient on the user's care teams (F7) — same `for_user()` scoping
    as the patient roster (§6.7), applied through the FK instead of the patient endpoint directly."""
    return Referral.objects.filter(patient__in=Patient.objects.for_user(user))
