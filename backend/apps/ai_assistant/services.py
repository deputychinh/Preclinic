from django.db import transaction

from apps.accounts.models import User
from apps.ai_assistant.models import AIDraft
from apps.ai_assistant.tasks import generate_ai_draft
from apps.audit.services import record_access
from apps.common.enums import AuditAction, NoteSource
from apps.common.exceptions import AppError
from apps.encounters.models import Encounter
from apps.encounters.services import create_note_draft


class DraftNotReadyError(AppError):
    status_code = 409
    code = "CONFLICT"


def request_ai_draft(*, encounter: Encounter, actor: User) -> AIDraft:
    draft = AIDraft.objects.create(encounter=encounter, requested_by=actor)
    generate_ai_draft.delay(draft.id)
    return draft


@transaction.atomic
def approve_draft(*, draft: AIDraft, clinician: User):
    """DS-05: the ONLY function that can turn an AIDraft into part of the legal record. It does so
    by creating a normal EncounterNoteVersion (source=AI_DRAFT) — still unsigned, still subject to
    the same sign_note() gate every human-authored note goes through."""
    if draft.status != "READY":
        raise DraftNotReadyError("Draft is not ready for approval")

    note = create_note_draft(
        encounter=draft.encounter, content=draft.content, source=NoteSource.AI_DRAFT, actor=clinician
    )
    draft.status = "APPROVED"
    draft.save(update_fields=["status"])

    record_access(
        actor=clinician,
        action=AuditAction.CREATE,
        resource_type="AIDraft",
        resource_id=str(draft.id),
        patient_id=str(draft.encounter.patient_id),
        metadata={"approved_to_note_version": note.id},
    )
    return note
