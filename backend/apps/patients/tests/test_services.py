import pytest

from apps.audit.models import AuditEvent
from apps.common.enums import Role
from apps.common.tests.factories import PatientFactory, UserFactory, add_to_care_team
from apps.patients.services import PatientAccessDeniedError, get_patient_chart

pytestmark = pytest.mark.django_db


def test_care_team_member_can_read_chart_and_is_audited():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()
    add_to_care_team(clinician, patient)

    result = get_patient_chart(user=clinician, patient_id=patient.id)

    assert result == patient
    event = AuditEvent.objects.get(resource_type="Patient", resource_id=str(patient.id))
    assert event.is_break_glass is False


def test_non_care_team_member_denied_without_reason():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()

    with pytest.raises(PatientAccessDeniedError):
        get_patient_chart(user=clinician, patient_id=patient.id)


def test_break_glass_grants_access_with_reason_and_is_audited():
    clinician = UserFactory(role=Role.CLINICIAN)
    patient = PatientFactory()

    result = get_patient_chart(user=clinician, patient_id=patient.id, break_glass_reason="ED emergency")

    assert result == patient
    event = AuditEvent.objects.get(resource_type="Patient", resource_id=str(patient.id))
    assert event.is_break_glass is True
    assert event.reason == "ED emergency"


def test_compliance_officer_denied_even_with_break_glass_reason():
    officer = UserFactory(role=Role.COMPLIANCE_OFFICER)
    patient = PatientFactory()

    with pytest.raises(PatientAccessDeniedError):
        get_patient_chart(user=officer, patient_id=patient.id, break_glass_reason="curious")


def test_nonexistent_patient_returns_same_404_as_denied_access():
    clinician = UserFactory(role=Role.CLINICIAN)

    with pytest.raises(PatientAccessDeniedError):
        get_patient_chart(user=clinician, patient_id=999999)
