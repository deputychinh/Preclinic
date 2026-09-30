from django.db import models
from django.db.models import Q

from apps.accounts.models import CareTeam, User
from apps.common.enums import ConsentType, Role
from apps.common.models import SoftDeleteModel, SoftDeleteQuerySet, TimestampedModel


class PatientQuerySet(SoftDeleteQuerySet):
    def for_user(self, user: User) -> "PatientQuerySet":
        """DS-02/NFR-02: care-team scoping enforced at the query level. Compliance officers see
        patient metadata nowhere by default — their access is audit-log-only, never chart data,
        unless a break-glass grant is active (handled in services.py, not here)."""
        if user.role == Role.COMPLIANCE_OFFICER:
            return self.none()
        return self.filter(care_team__memberships__user=user).distinct()


class Patient(TimestampedModel, SoftDeleteModel):
    mrn = models.CharField("medical record number", max_length=32, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    care_team = models.ForeignKey(CareTeam, on_delete=models.PROTECT, related_name="patients")

    # django-stubs types SoftDeleteModel.objects as ManagerFromSoftDeleteQuerySet[SoftDeleteModel];
    # overriding it with a Patient-specific manager is intentional (PatientQuerySet.for_user is the
    # RBAC-scoping entry point, §6.7) but reads as an invariant-type mismatch to the plugin.
    objects = PatientQuerySet.as_manager()  # type: ignore[misc,assignment]

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["mrn"]),
        ]

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} ({self.mrn})"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Allergy(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="allergies")
    substance = models.CharField(max_length=200)
    reaction = models.CharField(max_length=200, blank=True, default="")
    severity = models.CharField(max_length=50, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.substance} ({self.patient.mrn})"


class Medication(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, blank=True, default="")
    frequency = models.CharField(max_length=100, blank=True, default="")
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.patient.mrn})"


class Consent(TimestampedModel):
    """DS-08: referrals require an active DATA_SHARING consent row (checked in referrals/services.py)."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="consents")
    consent_type = models.CharField(max_length=32, choices=ConsentType.choices)
    granted_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "consent_type"],
                condition=Q(revoked_at__isnull=True),
                name="uq_one_active_consent_per_type",
            ),
        ]

    def is_active(self) -> bool:
        return self.revoked_at is None

    def __str__(self) -> str:
        return f"{self.consent_type} for {self.patient.mrn}"
