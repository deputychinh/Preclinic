from typing import cast

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from apps.accounts.models import User
from apps.care_plans.models import CarePlan
from apps.care_plans.selectors import get_care_plan_for_user, list_care_plans_for_patient
from apps.care_plans.serializers import CarePlanSerializer
from apps.common.exceptions import AppError


class CarePlanNotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class CarePlanListCreateView(ListAPIView, CreateAPIView):
    serializer_class = CarePlanSerializer

    def get_queryset(self):  # type: ignore[no-untyped-def]
        raw_patient_id = self.request.query_params.get("patient_id")
        if raw_patient_id is None or not raw_patient_id.isdigit():
            return CarePlan.objects.none()
        user = cast(User, self.request.user)
        return list_care_plans_for_patient(user=user, patient_id=int(raw_patient_id))


class CarePlanDetailView(RetrieveAPIView):
    serializer_class = CarePlanSerializer

    def get_object(self):  # type: ignore[no-untyped-def]
        user = cast(User, self.request.user)
        plan = get_care_plan_for_user(user=user, care_plan_id=self.kwargs["pk"])
        if plan is None:
            raise CarePlanNotFoundError("Care plan not found")
        return plan
