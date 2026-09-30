"""Richer demo data for local dev/review: a care team, five patients with varied charts, several
encounters at different stages (draft/pending-signature/signed), a ready-to-approve AI draft, care
plans, referrals, lab results, and a handful of real audit events so every tab has something to
show. Mirrors the real-estate project's `make seed` (python-vuejs/backend/scripts/seed.py)."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import CareTeam, CareTeamMembership, User
from apps.ai_assistant.models import AIDraft
from apps.audit.services import record_access
from apps.care_plans.models import CarePlan, CarePlanTask
from apps.common.enums import (
    AIDraftStatus,
    AuditAction,
    ConsentType,
    EncounterStatus,
    NoteSource,
    Role,
)
from apps.encounters.models import Encounter, EncounterNoteVersion
from apps.lab_results.models import LabResult
from apps.patients.models import Allergy, Consent, Medication, Patient
from apps.referrals.models import Referral

DEMO_PASSWORD = "Demo@1234"


class Command(BaseCommand):
    help = "Seed demo accounts, a care team, several patients with full charts, and sample activity."

    @transaction.atomic
    def handle(self, *args: object, **options: object) -> None:
        clinician = self._get_or_create_user("clinician@demo.com", "Demo", "Clinician", Role.CLINICIAN)
        coordinator = self._get_or_create_user(
            "coordinator@demo.com", "Demo", "Coordinator", Role.CARE_COORDINATOR
        )
        compliance = self._get_or_create_user(
            "compliance@demo.com", "Demo", "Compliance", Role.COMPLIANCE_OFFICER
        )

        team, _ = CareTeam.objects.get_or_create(name="Demo Care Team")
        CareTeamMembership.objects.get_or_create(care_team=team, user=clinician)
        CareTeamMembership.objects.get_or_create(care_team=team, user=coordinator)

        now = timezone.now()

        patient1 = self._get_or_create_patient("MRN000001", "Jane", "Doe", "1990-01-01", team)
        Medication.objects.get_or_create(
            patient=patient1, name="Metformin", defaults={"dosage": "500mg", "frequency": "twice daily"}
        )
        Medication.objects.get_or_create(
            patient=patient1, name="Lisinopril", defaults={"dosage": "10mg", "frequency": "once daily"}
        )
        Allergy.objects.get_or_create(
            patient=patient1, substance="Penicillin", defaults={"reaction": "Hives", "severity": "Moderate"}
        )
        Consent.objects.get_or_create(
            patient=patient1, consent_type=ConsentType.DATA_SHARING, defaults={"granted_at": now}
        )
        Consent.objects.get_or_create(
            patient=patient1, consent_type=ConsentType.TREATMENT, defaults={"granted_at": now}
        )
        plan, _ = CarePlan.objects.get_or_create(
            patient=patient1,
            title="Type 2 diabetes management",
            defaults={"goal": "HbA1c under 7.0% within 6 months"},
        )
        CarePlanTask.objects.get_or_create(
            care_plan=plan,
            description="Quarterly HbA1c blood test",
            defaults={"due_date": now.date() + timedelta(days=30)},
        )
        CarePlanTask.objects.get_or_create(
            care_plan=plan, description="Nutrition counseling referral", defaults={"completed_at": now}
        )
        LabResult.objects.get_or_create(
            patient=patient1,
            test_name="HbA1c",
            value="6.8",
            defaults={"unit": "%", "observed_at": now - timedelta(days=14)},
        )
        LabResult.objects.get_or_create(
            patient=patient1,
            test_name="Fasting glucose",
            value="112",
            defaults={"unit": "mg/dL", "observed_at": now - timedelta(days=14)},
        )
        Referral.objects.get_or_create(
            patient=patient1,
            referring_clinician=clinician,
            specialty="Endocrinology",
            defaults={"reason": "Ongoing diabetes management", "status": "ACCEPTED"},
        )

        # Encounter 1: signed, with an approved AI-sourced note (shows the full DS-05 flow's result).
        encounter1, created = Encounter.objects.get_or_create(
            patient=patient1,
            clinician=clinician,
            reason="Annual checkup",
            defaults={"occurred_at": now - timedelta(days=10), "status": EncounterStatus.SIGNED},
        )
        if created:
            EncounterNoteVersion.objects.create(
                encounter=encounter1,
                version=1,
                source=NoteSource.CLINICIAN,
                content="Patient reports feeling well. No new complaints. Continue current medications.",
                signed_by=clinician,
                signed_at=now - timedelta(days=10),
            )
            AIDraft.objects.create(
                encounter=encounter1,
                requested_by=clinician,
                status=AIDraftStatus.APPROVED,
                content="SOAP note (approved): stable on current regimen, no new complaints.",
                model_name="claude-opus-5-5",
            )

        # Encounter 2: a READY AI draft waiting for review — lets the sign-diff flow be tested
        # immediately without needing a live Claude API call.
        encounter2, created = Encounter.objects.get_or_create(
            patient=patient1,
            clinician=clinician,
            reason="Follow-up: medication adjustment",
            defaults={"occurred_at": now - timedelta(days=1), "status": EncounterStatus.DRAFT},
        )
        if created:
            AIDraft.objects.create(
                encounter=encounter2,
                requested_by=clinician,
                status=AIDraftStatus.READY,
                content=(
                    "S: Patient reports occasional dizziness in the morning.\n"
                    "O: BP 118/76, HR 72. No new medications.\n"
                    "A: Possible mild orthostatic effect from Lisinopril.\n"
                    "P: Monitor BP at home, follow up in 2 weeks if symptoms persist."
                ),
                model_name="claude-opus-5-5",
                tool_calls=[
                    {"tool": "get_patient_history", "input": {}},
                    {"tool": "get_medications", "input": {}},
                ],
            )

        patient2 = self._get_or_create_patient("MRN000002", "Robert", "Smith", "1975-06-15", team)
        Allergy.objects.get_or_create(
            patient=patient2,
            substance="Latex",
            defaults={"reaction": "Contact dermatitis", "severity": "Mild"},
        )
        Consent.objects.get_or_create(
            patient=patient2, consent_type=ConsentType.TREATMENT, defaults={"granted_at": now}
        )
        Encounter.objects.get_or_create(
            patient=patient2,
            clinician=clinician,
            reason="New patient intake",
            defaults={"occurred_at": now - timedelta(days=3), "status": EncounterStatus.PENDING_SIGNATURE},
        )
        # No DATA_SHARING consent for patient2 — demonstrates the 409 consent gate (B3) if a
        # referral is attempted for them in the UI.

        patient3 = self._get_or_create_patient("MRN000003", "Maria", "Garcia", "2001-11-02", team)
        Medication.objects.get_or_create(
            patient=patient3, name="Sertraline", defaults={"dosage": "50mg", "frequency": "once daily"}
        )
        Consent.objects.get_or_create(
            patient=patient3, consent_type=ConsentType.DATA_SHARING, defaults={"granted_at": now}
        )
        Referral.objects.get_or_create(
            patient=patient3,
            referring_clinician=clinician,
            specialty="Psychiatry",
            defaults={"reason": "Medication review", "status": "REQUESTED"},
        )

        patient4 = self._get_or_create_patient("MRN000004", "Wei", "Chen", "1958-02-20", team)
        Consent.objects.get_or_create(
            patient=patient4, consent_type=ConsentType.DATA_SHARING, defaults={"granted_at": now}
        )
        Consent.objects.get_or_create(
            patient=patient4,
            consent_type=ConsentType.RESEARCH,
            defaults={"granted_at": now - timedelta(days=200), "revoked_at": now - timedelta(days=30)},
        )
        Referral.objects.get_or_create(
            patient=patient4,
            referring_clinician=clinician,
            specialty="Cardiology",
            defaults={"reason": "Elevated blood pressure, rule out hypertension", "status": "DECLINED"},
        )

        # Deliberately minimal chart for patient5: shows the roster/empty-state UI for a brand-new
        # patient with no encounters, meds or referrals yet.
        self._get_or_create_patient("MRN000005", "Amara", "Okafor", "1995-09-08", team)

        # A handful of real audit events so the Compliance Officer's Audit Log tab has data —
        # written the same way the app itself writes them (DS-04), not faked directly.
        for patient in (patient1, patient2, patient3):
            record_access(
                actor=clinician,
                action=AuditAction.READ,
                resource_type="Patient",
                resource_id=str(patient.id),
                patient_id=str(patient.id),
            )
        record_access(
            actor=clinician,
            action=AuditAction.READ,
            resource_type="Patient",
            resource_id=str(patient4.id),
            patient_id=str(patient4.id),
            reason="Covering for Dr. Nguyen, patient presented to urgent care",
            is_break_glass=True,
        )
        record_access(
            actor=compliance,
            action=AuditAction.EXPORT,
            resource_type="AuditEvent",
            resource_id="bulk",
            reason="Monthly compliance review export",
        )

        self.stdout.write(
            self.style.SUCCESS("Seeded demo data: 5 patients, 3 encounters, 4 referrals, audit events.")
        )
        self.stdout.write(
            f"  clinician@demo.com / coordinator@demo.com / compliance@demo.com : {DEMO_PASSWORD}"
        )

    @staticmethod
    def _get_or_create_patient(
        mrn: str, first_name: str, last_name: str, dob: str, team: CareTeam
    ) -> Patient:
        patient, _ = Patient.objects.get_or_create(
            mrn=mrn,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob,
                "care_team": team,
            },
        )
        return patient

    @staticmethod
    def _get_or_create_user(email: str, first_name: str, last_name: str, role: Role) -> User:
        user, created = User.objects.get_or_create(
            email=email, defaults={"first_name": first_name, "last_name": last_name, "role": role}
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        return user
