import pytest

from apps.common.dashboard import get_dashboard_summary
from apps.common.enums import Role
from apps.common.tests.factories import EncounterFactory, PatientFactory, UserFactory, add_to_care_team

pytestmark = pytest.mark.django_db


def test_clinical_summary_counts_only_care_team_patients():
    clinician = UserFactory(role=Role.CLINICIAN)
    own_patient = PatientFactory()
    other_patient = PatientFactory()
    add_to_care_team(clinician, own_patient)
    EncounterFactory(patient=own_patient, clinician=clinician)
    EncounterFactory(patient=other_patient)  # not on this clinician's care team

    summary = get_dashboard_summary(user=clinician)

    assert summary["role"] == Role.CLINICIAN
    assert summary["patient_count"] == 1
    assert summary["encounters_this_week"] == 1
    assert summary["encounter_breakdown"] == [{"label": "DRAFT", "count": 1}]


def test_compliance_summary_has_no_patient_count():
    officer = UserFactory(role=Role.COMPLIANCE_OFFICER)

    summary = get_dashboard_summary(user=officer)

    assert summary["role"] == Role.COMPLIANCE_OFFICER
    assert "patient_count" not in summary
    assert "events_today" in summary
