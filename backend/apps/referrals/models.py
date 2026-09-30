from django.conf import settings
from django.db import models

from apps.common.enums import ReferralStatus
from apps.common.models import TimestampedModel
from apps.patients.models import Patient


class Referral(TimestampedModel):
    """DS-08/B3: creation is gated on an active DATA_SHARING consent, checked in services.py."""

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="referrals")
    referring_clinician = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="referrals_made"
    )
    specialty = models.CharField(max_length=150)
    reason = models.TextField()
    status = models.CharField(max_length=32, choices=ReferralStatus.choices, default=ReferralStatus.REQUESTED)

    def __str__(self) -> str:
        return f"Referral to {self.specialty} for {self.patient.mrn}"
