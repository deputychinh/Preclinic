import pytest

from apps.ai_assistant.models import AIDraft
from apps.ai_assistant.services import DraftNotReadyError, approve_draft
from apps.common.enums import AIDraftStatus
from apps.common.tests.factories import EncounterFactory

pytestmark = pytest.mark.django_db


def test_pending_draft_cannot_be_approved():
    encounter = EncounterFactory()
    draft = AIDraft.objects.create(
        encounter=encounter, requested_by=encounter.clinician, status=AIDraftStatus.PENDING
    )

    with pytest.raises(DraftNotReadyError):
        approve_draft(draft=draft, clinician=encounter.clinician)


def test_ready_draft_approval_creates_unsigned_note_version_sourced_as_ai():
    encounter = EncounterFactory()
    draft = AIDraft.objects.create(
        encounter=encounter,
        requested_by=encounter.clinician,
        status=AIDraftStatus.READY,
        content="Drafted SOAP note",
    )

    note = approve_draft(draft=draft, clinician=encounter.clinician)
    draft.refresh_from_db()

    assert note.source == "AI_DRAFT"
    assert note.signed_at is None  # DS-05: approval is not the same as signing
    assert draft.status == "APPROVED"


def test_failed_draft_cannot_be_approved():
    encounter = EncounterFactory()
    draft = AIDraft.objects.create(
        encounter=encounter, requested_by=encounter.clinician, status=AIDraftStatus.FAILED
    )

    with pytest.raises(DraftNotReadyError):
        approve_draft(draft=draft, clinician=encounter.clinician)
