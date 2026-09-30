import pytest

from apps.common.tests.factories import PatientFactory, UserFactory
from apps.lab_results.models import LabImportJob, LabResult
from apps.lab_results.services import apply_csv_rows, start_import_job

pytestmark = pytest.mark.django_db


def test_apply_csv_rows_imports_valid_rows_and_reports_bad_ones():
    patient = PatientFactory(mrn="MRN0001")
    job = LabImportJob.objects.create(uploaded_by=UserFactory(), idempotency_key="k1")
    rows = [
        {
            "mrn": "MRN0001",
            "test_name": "A1C",
            "value": "5.4",
            "unit": "%",
            "observed_at": "2026-01-01T00:00:00+00:00",
        },
        {
            "mrn": "NOSUCH",
            "test_name": "A1C",
            "value": "5.4",
            "unit": "%",
            "observed_at": "2026-01-01T00:00:00+00:00",
        },
    ]

    apply_csv_rows(job=job, rows=rows)
    job.refresh_from_db()

    assert job.imported_rows == 1
    assert len(job.error_report) == 1
    assert job.error_report[0]["row"] == 1
    assert LabResult.objects.filter(patient=patient).count() == 1


def test_start_import_job_is_idempotent_on_identical_file(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    actor = UserFactory()
    file_bytes = b"mrn,test_name,value,unit,observed_at\n"

    job1, created1 = start_import_job(file_bytes=file_bytes, actor=actor)
    job2, created2 = start_import_job(file_bytes=file_bytes, actor=actor)

    assert created1 is True
    assert created2 is False
    assert job1.id == job2.id
    assert LabImportJob.objects.count() == 1
