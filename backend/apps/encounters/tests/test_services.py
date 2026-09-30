import pytest

from apps.common.enums import NoteSource
from apps.common.tests.factories import EncounterFactory
from apps.encounters.services import InvalidSignError, create_note_draft, sign_note

pytestmark = pytest.mark.django_db


def test_sign_note_marks_signed_and_updates_encounter_status():
    encounter = EncounterFactory()
    clinician = encounter.clinician
    note = create_note_draft(
        encounter=encounter, content="SOAP note text", source=NoteSource.CLINICIAN, actor=clinician
    )

    signed = sign_note(encounter=encounter, note=note, clinician=clinician)

    encounter.refresh_from_db()
    assert signed.signed_at is not None
    assert signed.signed_by == clinician
    assert encounter.status == "SIGNED"


def test_cannot_sign_an_already_signed_note():
    encounter = EncounterFactory()
    clinician = encounter.clinician
    note = create_note_draft(
        encounter=encounter, content="text", source=NoteSource.CLINICIAN, actor=clinician
    )
    sign_note(encounter=encounter, note=note, clinician=clinician)

    with pytest.raises(InvalidSignError):
        sign_note(encounter=encounter, note=note, clinician=clinician)


def test_signing_never_mutates_note_content_append_only():
    encounter = EncounterFactory()
    clinician = encounter.clinician
    note = create_note_draft(
        encounter=encounter, content="original text", source=NoteSource.CLINICIAN, actor=clinician
    )

    sign_note(encounter=encounter, note=note, clinician=clinician)
    note.refresh_from_db()

    assert note.content == "original text"


def test_note_from_another_encounter_cannot_be_signed():
    encounter_a = EncounterFactory()
    encounter_b = EncounterFactory()
    note = create_note_draft(
        encounter=encounter_a, content="text", source=NoteSource.CLINICIAN, actor=encounter_a.clinician
    )

    with pytest.raises(InvalidSignError):
        sign_note(encounter=encounter_b, note=note, clinician=encounter_b.clinician)
