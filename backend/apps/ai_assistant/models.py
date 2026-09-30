from django.conf import settings
from django.db import models

from apps.common.enums import AIDraftStatus
from apps.common.models import TimestampedModel
from apps.encounters.models import Encounter


class AIDraft(TimestampedModel):
    """DS-05/NFR-04: lives entirely outside the clinical record. No code path exists that turns
    an AIDraft directly into an EncounterNoteVersion — only `approve_draft()` (services.py), which
    a clinician must call explicitly, and which goes through the normal sign flow."""

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name="ai_drafts")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    status = models.CharField(max_length=32, choices=AIDraftStatus.choices, default=AIDraftStatus.PENDING)
    content = models.TextField(blank=True, default="")
    model_name = models.CharField(max_length=100, blank=True, default="")
    tool_calls = models.JSONField(default=list, blank=True)
    error = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"AIDraft #{self.id} for encounter {self.encounter_id} ({self.status})"
