import hashlib

from django.conf import settings
from django.db import models

from apps.common.enums import ImportJobStatus
from apps.common.models import TimestampedModel
from apps.patients.models import Patient


class LabResult(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="lab_results")
    test_name = models.CharField(max_length=200)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True, default="")
    observed_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["patient", "-observed_at"])]

    def __str__(self) -> str:
        return f"{self.test_name}={self.value}{self.unit} ({self.patient.mrn})"


class LabImportJob(TimestampedModel):
    """B4: async, chunked, idempotent bulk CSV import (NFR-05/DS-06). `idempotency_key` is the
    SHA-256 of the uploaded file — re-uploading the identical file is a no-op, not a duplicate import."""

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    idempotency_key = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=32, choices=ImportJobStatus.choices, default=ImportJobStatus.PENDING)
    total_rows = models.PositiveIntegerField(default=0)
    imported_rows = models.PositiveIntegerField(default=0)
    error_report = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return f"Import job #{self.id} ({self.status})"

    @staticmethod
    def compute_idempotency_key(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()
