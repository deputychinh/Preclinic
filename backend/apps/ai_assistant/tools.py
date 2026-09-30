"""Read-only tools only (DS-05/NFR-04): no tool in this module can write anything. The LLM can
look at the chart; it cannot change it."""

from dataclasses import dataclass
from typing import Any

from apps.patients.models import Allergy, Medication, Patient


@dataclass
class GetPatientHistoryTool:
    patient: Patient
    name: str = "get_patient_history"
    description: str = "Get the patient's demographics and recent encounter reasons."
    input_schema: dict[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.input_schema = {"type": "object", "properties": {}}

    def __call__(self, **_: Any) -> Any:
        encounters = self.patient.encounters.order_by("-occurred_at")[:5]
        return {
            "name": self.patient.get_full_name(),
            "date_of_birth": str(self.patient.date_of_birth),
            "recent_encounters": [
                {"reason": e.reason, "occurred_at": str(e.occurred_at)} for e in encounters
            ],
        }


@dataclass
class GetMedicationsTool:
    patient: Patient
    name: str = "get_medications"
    description: str = "List the patient's active medications."
    input_schema: dict[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.input_schema = {"type": "object", "properties": {}}

    def __call__(self, **_: Any) -> Any:
        return list(
            Medication.objects.filter(patient=self.patient, active=True).values("name", "dosage", "frequency")
        )


@dataclass
class GetAllergiesTool:
    patient: Patient
    name: str = "get_allergies"
    description: str = "List the patient's known allergies."
    input_schema: dict[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.input_schema = {"type": "object", "properties": {}}

    def __call__(self, **_: Any) -> Any:
        return list(Allergy.objects.filter(patient=self.patient).values("substance", "reaction", "severity"))


def build_read_only_tools(patient: Patient) -> list:
    return [GetPatientHistoryTool(patient), GetMedicationsTool(patient), GetAllergiesTool(patient)]
