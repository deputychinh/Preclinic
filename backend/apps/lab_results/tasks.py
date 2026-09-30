import csv
import io

from celery import shared_task

from apps.common.enums import ImportJobStatus
from apps.lab_results.models import LabImportJob
from apps.lab_results.services import apply_csv_rows

CHUNK_SIZE = 500


@shared_task
def run_lab_import(job_id: int, csv_text: str) -> None:
    job = LabImportJob.objects.get(id=job_id)
    job.status = ImportJobStatus.RUNNING
    job.save(update_fields=["status"])

    reader = list(csv.DictReader(io.StringIO(csv_text)))
    job.total_rows = len(reader)
    job.save(update_fields=["total_rows"])

    for start in range(0, len(reader), CHUNK_SIZE):
        apply_csv_rows(job=job, rows=reader[start : start + CHUNK_SIZE])

    job.status = ImportJobStatus.FAILED_PARTIAL if job.error_report else ImportJobStatus.SUCCEEDED
    job.save(update_fields=["status"])
