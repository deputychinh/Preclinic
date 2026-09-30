import pytest

from apps.common.enums import Role
from apps.common.tests.factories import EncounterFactory, UserFactory, add_to_care_team
from apps.encounters.selectors import get_encounter_for_user

pytestmark = pytest.mark.django_db


def test_care_team_member_can_load_encounter():
    encounter = EncounterFactory()
    add_to_care_team(encounter.clinician, encounter.patient)

    result = get_encounter_for_user(user=encounter.clinician, encounter_id=encounter.id)

    assert result == encounter


def test_non_care_team_member_cannot_load_encounter():
    encounter = EncounterFactory()
    outsider = UserFactory(role=Role.CLINICIAN)

    result = get_encounter_for_user(user=outsider, encounter_id=encounter.id)

    assert result is None


def test_nonexistent_encounter_returns_none():
    clinician = UserFactory(role=Role.CLINICIAN)

    assert get_encounter_for_user(user=clinician, encounter_id=999999) is None
