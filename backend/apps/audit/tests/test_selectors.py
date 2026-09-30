import pytest
from django.db import transaction

from apps.audit.selectors import NotComplianceOfficerError, search_audit_events
from apps.audit.services import record_access
from apps.common.enums import AuditAction, Role
from apps.common.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_non_compliance_officer_denied():
    clinician = UserFactory(role=Role.CLINICIAN)

    with pytest.raises(NotComplianceOfficerError):
        search_audit_events(user=clinician, filters={})


def test_compliance_officer_can_search_and_filter():
    officer = UserFactory(role=Role.COMPLIANCE_OFFICER)
    actor = UserFactory(role=Role.CLINICIAN)
    with transaction.atomic():
        record_access(
            actor=actor, action=AuditAction.READ, resource_type="Patient", resource_id="1", patient_id="1"
        )
        record_access(
            actor=actor,
            action=AuditAction.BREAK_GLASS,
            resource_type="Patient",
            resource_id="2",
            is_break_glass=True,
        )

    all_events = search_audit_events(user=officer, filters={})
    assert all_events.count() == 2

    break_glass_only = search_audit_events(user=officer, filters={"break_glass_only": True})
    assert break_glass_only.count() == 1

    by_patient = search_audit_events(user=officer, filters={"patient_id": "1"})
    assert by_patient.count() == 1
