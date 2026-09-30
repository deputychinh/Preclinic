from django.conf import settings
from django.db import models

from apps.common.enums import AuditAction


class AuditEvent(models.Model):
    """One row per PHI access or mutation. Written inside the same transaction as the access
    itself (DS-04) — never via signals, since bulk_update/raw SQL bypass signals silently."""

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="audit_events")
    action = models.CharField(max_length=32, choices=AuditAction.choices)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=64)
    patient_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    reason = models.TextField(blank=True, default="")
    is_break_glass = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["resource_type", "resource_id"]),
            models.Index(fields=["actor", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.action} {self.resource_type}:{self.resource_id} by {self.actor_id}"
