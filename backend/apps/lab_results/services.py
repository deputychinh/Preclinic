from datetime import datetime

from apps.accounts.models import User
from apps.lab_results.models import LabImportJob, LabResult
from apps.patients.models import Patient


def start_import_job(*, file_bytes: bytes, actor: User) -> tuple[LabImportJob, bool]:
    """Returns (job, created). `created=False` means an identical file was already imported —
    the caller should report that back rather than re-queue it (idempotency, DS-06)."""
    key = LabImportJob.compute_idempotency_key(file_bytes)
    job, created = LabImportJob.objects.get_or_create(
        idempotency_key=key, defaults={"uploaded_by": actor}
    )
    if created:
        # Lazy on purpose: tasks.py imports apply_csv_rows from this module at its own top level,
        # so a top-level import here would be circular.
        from apps.lab_results.tasks import run_lab_import  # noqa: PLC0415

        run_lab_import.delay(job.id, file_bytes.decode("utf-8"))
    return job, created


def apply_csv_rows(*, job: LabImportJob, rows: list[dict]) -> None:
    """Called by the Celery task in chunks so a large file never sits fully in memory at once."""
    errors = list(job.error_report)
    imported = job.imported_rows

    for i, row in enumerate(rows):
        try:
            patient = Patient.objects.get(mrn=row["mrn"])
            LabResult.objects.create(
                patient=patient,
                test_name=row["test_name"],
                value=row["value"],
                unit=row.get("unit", ""),
                observed_at=datetime.fromisoformat(row["observed_at"]),
            )
            imported += 1
        except Exception as exc:
            errors.append({"row": i, "error": str(exc)})

    job.imported_rows = imported
    job.error_report = errors
    job.save(update_fields=["imported_rows", "error_report"])
