from django.db.models import QuerySet

from apps.accounts.models import User
from apps.encounters.models import Encounter
from apps.patients.selectors import get_patient_for_user


def get_encounter_for_user(*, user: User, encounter_id: int) -> Encounter | None:
    encounter = Encounter.objects.select_related("patient").filter(id=encounter_id).first()
    if encounter is None:
        return None
    if get_patient_for_user(user=user, patient_id=encounter.patient_id) is None:
        return None
    return encounter


def list_note_versions(*, encounter: Encounter) -> QuerySet:
    return encounter.note_versions.all()
