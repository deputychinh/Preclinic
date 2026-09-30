from django.conf import settings
from django.db import models

from apps.common.enums import EncounterStatus, NoteSource
from apps.common.models import TimestampedModel
from apps.patients.models import Patient


class Encounter(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="encounters")
    clinician = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="encounters"
    )
    status = models.CharField(max_length=32, choices=EncounterStatus.choices, default=EncounterStatus.DRAFT)
    reason = models.CharField(max_length=300)
    occurred_at = models.DateTimeField()

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self) -> str:
        return f"Encounter #{self.id} ({self.patient.mrn})"


class EncounterNoteVersion(TimestampedModel):
    """DS-03: append-only. A signed note is never mutated — amending creates a new version with
    `supersedes` pointing at the prior one. `views.py`/`services.py` never expose an update path."""

    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT, related_name="note_versions")
    version = models.PositiveIntegerField()
    source = models.CharField(max_length=32, choices=NoteSource.choices)
    content = models.TextField()
    signed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    signed_at = models.DateTimeField(null=True, blank=True)
    supersedes = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="+")

    class Meta:
        ordering = ["-version"]
        constraints = [
            models.UniqueConstraint(fields=["encounter", "version"], name="uq_encounter_note_version"),
        ]

    def __str__(self) -> str:
        return f"Encounter {self.encounter_id} v{self.version}"


class DiagnosisCode(TimestampedModel):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name="diagnosis_codes")
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.code} on encounter {self.encounter_id}"
