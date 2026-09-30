from typing import cast

from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.accounts.models import User
from apps.common.pagination import PatientKeysetPagination
from apps.patients.models import Patient
from apps.patients.selectors import list_patients_for_user
from apps.patients.serializers import PatientDetailSerializer, PatientListSerializer
from apps.patients.services import PatientAccessDeniedError, get_patient_chart


class PatientListView(ListAPIView):
    serializer_class = PatientListSerializer
    pagination_class = PatientKeysetPagination

    def get_queryset(self):  # type: ignore[no-untyped-def]
        user = cast(User, self.request.user)
        return list_patients_for_user(user=user, search=self.request.query_params.get("q", ""))


class PatientDetailView(RetrieveAPIView):
    """Routed by MRN (§7.2's human-facing `/patients/:mrn`), not the numeric pk — `get_patient_chart`
    itself still takes an id, since every other app's selector (care_plans, referrals, encounters)
    looks patients up by FK id, not MRN."""

    serializer_class = PatientDetailSerializer

    def get_object(self):  # type: ignore[no-untyped-def]
        reason = self.request.query_params.get("break_glass_reason", "")
        patient_id = Patient.objects.filter(mrn=self.kwargs["mrn"]).values_list("id", flat=True).first()
        if patient_id is None:
            raise PatientAccessDeniedError("Patient not found")
        user = cast(User, self.request.user)
        return get_patient_chart(user=user, patient_id=patient_id, break_glass_reason=reason)
