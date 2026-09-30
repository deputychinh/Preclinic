import pytest

from apps.common.tests.factories import PatientFactory, UserFactory, add_to_care_team
from apps.referrals.models import Referral
from apps.referrals.selectors import list_referrals_for_patient, list_referrals_for_user

pytestmark = pytest.mark.django_db


def test_care_team_member_sees_patients_referrals():
    clinician = UserFactory()
    patient = PatientFactory()
    add_to_care_team(clinician, patient)
    referral = Referral.objects.create(
        patient=patient, referring_clinician=clinician, specialty="Cardiology", reason="Chest pain"
    )

    assert list(list_referrals_for_patient(user=clinician, patient_id=patient.id)) == [referral]
    assert list(list_referrals_for_user(user=clinician)) == [referral]


def test_non_care_team_member_sees_no_referrals():
    clinician = UserFactory()
    other_clinician = UserFactory()
    patient = PatientFactory()
    add_to_care_team(other_clinician, patient)
    Referral.objects.create(
        patient=patient, referring_clinician=other_clinician, specialty="Cardiology", reason="Chest pain"
    )

    assert list(list_referrals_for_patient(user=clinician, patient_id=patient.id)) == []
    assert list(list_referrals_for_user(user=clinician)) == []
