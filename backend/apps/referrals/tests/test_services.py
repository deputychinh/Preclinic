import pytest

from apps.common.exceptions import ConsentRequiredError
from apps.common.tests.factories import PatientFactory, UserFactory, grant_consent
from apps.referrals.services import create_referral

pytestmark = pytest.mark.django_db


def test_referral_blocked_without_active_consent():
    patient = PatientFactory()
    clinician = UserFactory()

    with pytest.raises(ConsentRequiredError):
        create_referral(patient=patient, specialty="Cardiology", reason="Chest pain", actor=clinician)


def test_referral_allowed_with_active_consent():
    patient = PatientFactory()
    clinician = UserFactory()
    grant_consent(patient)

    referral = create_referral(patient=patient, specialty="Cardiology", reason="Chest pain", actor=clinician)

    assert referral.id is not None
    assert referral.status == "REQUESTED"


def test_referral_blocked_after_consent_revoked():
    patient = PatientFactory()
    clinician = UserFactory()
    consent = grant_consent(patient)
    consent.revoked_at = consent.granted_at
    consent.save(update_fields=["revoked_at"])

    with pytest.raises(ConsentRequiredError):
        create_referral(patient=patient, specialty="Cardiology", reason="Chest pain", actor=clinician)
