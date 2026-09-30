from django.db.models import QuerySet

from apps.accounts.models import User
from apps.care_plans.models import CarePlan
from apps.patients.selectors import get_patient_for_user


def list_care_plans_for_patient(*, user: User, patient_id: int) -> QuerySet[CarePlan]:
    if get_patient_for_user(user=user, patient_id=patient_id) is None:
        return CarePlan.objects.none()
    return CarePlan.objects.filter(patient_id=patient_id).prefetch_related("tasks")


def get_care_plan_for_user(*, user: User, care_plan_id: int) -> CarePlan | None:
    """§7.2's `/care-plans/:id` detail view: care-team-scoped through the plan's own patient FK."""
    plan = (
        CarePlan.objects.select_related("patient")
        .prefetch_related("tasks")
        .filter(id=care_plan_id)
        .first()
    )
    if plan is None:
        return None
    if get_patient_for_user(user=user, patient_id=plan.patient_id) is None:
        return None
    return plan
