from django.db import models

from apps.common.models import TimestampedModel
from apps.patients.models import Patient


class CarePlan(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="care_plans")
    title = models.CharField(max_length=200)
    goal = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.title} ({self.patient.mrn})"


class CarePlanTask(TimestampedModel):
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=300)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.description
