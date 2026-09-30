import factory
from django.utils import timezone

from apps.accounts.models import CareTeam, CareTeamMembership, User
from apps.common.enums import ConsentType, Role
from apps.encounters.models import Encounter
from apps.patients.models import Consent, Patient


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@demo.com")
    first_name = "Test"
    last_name = "User"
    role = Role.CLINICIAN

    @factory.post_generation
    def password(self, create, extracted, **kwargs):  # type: ignore[no-untyped-def]
        self.set_password(extracted or "Demo@1234")
        if create:
            self.save()


class CareTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CareTeam

    name = factory.Sequence(lambda n: f"Care Team {n}")


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    mrn = factory.Sequence(lambda n: f"MRN{n:06d}")
    first_name = "Jane"
    last_name = "Doe"
    date_of_birth = "1990-01-01"
    care_team = factory.SubFactory(CareTeamFactory)


class EncounterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Encounter

    patient = factory.SubFactory(PatientFactory)
    clinician = factory.SubFactory(UserFactory)
    reason = "Annual checkup"
    occurred_at = factory.LazyFunction(timezone.now)


def add_to_care_team(user: User, patient: Patient) -> None:
    CareTeamMembership.objects.get_or_create(care_team=patient.care_team, user=user)


def grant_consent(patient: Patient, consent_type: str = ConsentType.DATA_SHARING) -> Consent:
    return Consent.objects.create(patient=patient, consent_type=consent_type, granted_at=timezone.now())
