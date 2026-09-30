from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.audit.services import record_access
from apps.common.enums import AuditAction, EncounterStatus, NoteSource
from apps.common.exceptions import AppError
from apps.encounters.models import Encounter, EncounterNoteVersion


class EncounterNotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class InvalidSignError(AppError):
    status_code = 409
    code = "CONFLICT"


@transaction.atomic
def create_note_draft(
    *, encounter: Encounter, content: str, source: NoteSource, actor: User
) -> EncounterNoteVersion:
    latest_version = (
        encounter.note_versions.order_by("-version").values_list("version", flat=True).first()
    )
    next_version = (latest_version or 0) + 1
    note = EncounterNoteVersion.objects.create(
        encounter=encounter, version=next_version, source=source, content=content
    )
    record_access(
        actor=actor,
        action=AuditAction.CREATE,
        resource_type="EncounterNoteVersion",
        resource_id=str(note.id),
        patient_id=str(encounter.patient_id),
        metadata={"source": source, "version": next_version},
    )
    return note


@transaction.atomic
def sign_note(*, encounter: Encounter, note: EncounterNoteVersion, clinician: User) -> EncounterNoteVersion:
    """B2 final step: only a human sign turns a draft (clinician or AI-sourced) into the legal
    record. §7.5's diff-before-sign UI rule is enforced client-side; server-side the only guarantee
    is that this is the sole path that sets `signed_by`/`signed_at` and flips encounter status."""
    if note.encounter_id != encounter.id:
        raise InvalidSignError("Note does not belong to this encounter")
    if note.signed_at is not None:
        raise InvalidSignError("Note is already signed")

    note.signed_by = clinician
    note.signed_at = timezone.now()
    note.save(update_fields=["signed_by", "signed_at"])
    encounter.status = EncounterStatus.SIGNED
    encounter.save(update_fields=["status"])

    record_access(
        actor=clinician,
        action=AuditAction.UPDATE,
        resource_type="EncounterNoteVersion",
        resource_id=str(note.id),
        patient_id=str(encounter.patient_id),
        metadata={"signed": True, "source": note.source},
    )
    return note
