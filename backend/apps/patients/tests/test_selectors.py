import pytest

from apps.common.enums import Role
from apps.common.tests.factories import PatientFactory, UserFactory, add_to_care_team
from apps.patients.selectors import list_patients_for_user

pytestmark = pytest.mark.django_db


def test_clinician_sees_only_own_care_team_patients():
    clinician = UserFactory(role=Role.CLINICIAN)
    own_patient = PatientFactory()
    other_patient = PatientFactory()
    add_to_care_team(clinician, own_patient)

    visible = list(list_patients_for_user(user=clinician))

    assert visible == [own_patient]
    assert other_patient not in visible


def test_compliance_officer_sees_no_patients():
    officer = UserFactory(role=Role.COMPLIANCE_OFFICER)
    patient = PatientFactory()
    add_to_care_team(officer, patient)  # even if somehow added, DS-02 must still deny

    assert list(list_patients_for_user(user=officer)) == []


def test_search_filters_by_name_and_mrn():
    clinician = UserFactory(role=Role.CLINICIAN)
    match = PatientFactory(first_name="Alice", last_name="Smith")
    other = PatientFactory(first_name="Bob", last_name="Jones")
    add_to_care_team(clinician, match)
    add_to_care_team(clinician, other)

    results = list(list_patients_for_user(user=clinician, search="Alice"))

    assert results == [match]
