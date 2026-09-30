import pytest

from apps.care_plans.models import CarePlan
from apps.care_plans.selectors import get_care_plan_for_user, list_care_plans_for_patient
from apps.common.enums import Role
from apps.common.tests.factories import PatientFactory, UserFactory, add_to_care_team

pytestmark = pytest.mark.django_db


def test_care_team_member_sees_patients_care_plans():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()
    add_to_care_team(clinician, patient)
    plan = CarePlan.objects.create(patient=patient, title="Diabetes management")

    plans = list_care_plans_for_patient(user=clinician, patient_id=patient.id)

    assert list(plans) == [plan]


def test_non_care_team_member_sees_no_care_plans():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()
    CarePlan.objects.create(patient=patient, title="Diabetes management")

    plans = list_care_plans_for_patient(user=clinician, patient_id=patient.id)

    assert list(plans) == []


def test_care_team_member_can_load_single_care_plan():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()
    add_to_care_team(clinician, patient)
    plan = CarePlan.objects.create(patient=patient, title="Diabetes management")

    assert get_care_plan_for_user(user=clinician, care_plan_id=plan.id) == plan


def test_non_care_team_member_cannot_load_single_care_plan():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()
    plan = CarePlan.objects.create(patient=patient, title="Diabetes management")

    assert get_care_plan_for_user(user=clinician, care_plan_id=plan.id) is None
