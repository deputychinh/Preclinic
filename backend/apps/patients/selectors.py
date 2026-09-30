from django.db.models import Q, QuerySet

from apps.accounts.models import User
from apps.patients.models import Patient


def list_patients_for_user(*, user: User, search: str = "") -> QuerySet[Patient]:
    """B1: care-team-scoped roster/search. Trigram index (see migrations) backs `search` at scale (NFR-05)."""
    qs = Patient.objects.for_user(user).alive()
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(mrn__icontains=search)
        )
    return qs


def get_patient_for_user(*, user: User, patient_id: int) -> Patient | None:
    return Patient.objects.for_user(user).alive().filter(id=patient_id).first()
