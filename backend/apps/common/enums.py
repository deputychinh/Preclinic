"""Every closed set in the domain. Stored as strings in Postgres, mirrored in frontend/src/enums."""

from django.db import models


class Role(models.TextChoices):
    CLINICIAN = "CLINICIAN", "Clinician"
    CARE_COORDINATOR = "CARE_COORDINATOR", "Care coordinator"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER", "Compliance officer"


class EncounterStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PENDING_SIGNATURE = "PENDING_SIGNATURE", "Pending signature"
    SIGNED = "SIGNED", "Signed"
    AMENDED = "AMENDED", "Amended"


class NoteSource(models.TextChoices):
    CLINICIAN = "CLINICIAN", "Clinician"
    AI_DRAFT = "AI_DRAFT", "AI draft"


class ReferralStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    ACCEPTED = "ACCEPTED", "Accepted"
    DECLINED = "DECLINED", "Declined"
    COMPLETED = "COMPLETED", "Completed"


class ConsentType(models.TextChoices):
    TREATMENT = "TREATMENT", "Treatment"
    DATA_SHARING = "DATA_SHARING", "Data sharing"
    RESEARCH = "RESEARCH", "Research"


class ImportJobStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    RUNNING = "RUNNING", "Running"
    SUCCEEDED = "SUCCEEDED", "Succeeded"
    FAILED_PARTIAL = "FAILED_PARTIAL", "Failed (partial)"


class AuditAction(models.TextChoices):
    READ = "READ", "Read"
    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    EXPORT = "EXPORT", "Export"
    BREAK_GLASS = "BREAK_GLASS", "Break-glass access"


class AIDraftStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    READY = "READY", "Ready for review"
    APPROVED = "APPROVED", "Approved"
    FAILED = "FAILED", "Failed"
