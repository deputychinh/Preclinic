from typing import cast

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.accounts.models import User
from apps.patients.models import Patient
from apps.referrals.selectors import list_referrals_for_patient, list_referrals_for_user
from apps.referrals.serializers import ReferralSerializer
from apps.referrals.services import create_referral


class ReferralListCreateView(ListAPIView):
    serializer_class = ReferralSerializer

    def get_queryset(self):  # type: ignore[no-untyped-def]
        raw_patient_id = self.request.query_params.get("patient_id")
        user = cast(User, self.request.user)
        if raw_patient_id and raw_patient_id.isdigit():
            return list_referrals_for_patient(user=user, patient_id=int(raw_patient_id))
        return list_referrals_for_user(user=user)

    def post(self, request):  # type: ignore[no-untyped-def]
        serializer = ReferralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = get_object_or_404(Patient, id=serializer.validated_data["patient"].id)
        referral = create_referral(
            patient=patient,
            specialty=serializer.validated_data["specialty"],
            reason=serializer.validated_data["reason"],
            actor=request.user,
        )
        return Response(ReferralSerializer(referral).data, status=201)
