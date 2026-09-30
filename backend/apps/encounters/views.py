from typing import cast

from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.common.exceptions import AppError
from apps.encounters.selectors import get_encounter_for_user
from apps.encounters.serializers import (
    EncounterNoteVersionSerializer,
    EncounterSerializer,
    SignNoteSerializer,
)
from apps.encounters.services import sign_note


class EncounterNotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class EncounterDetailView(RetrieveAPIView):
    serializer_class = EncounterSerializer

    def get_object(self):  # type: ignore[no-untyped-def]
        user = cast(User, self.request.user)
        encounter = get_encounter_for_user(user=user, encounter_id=self.kwargs["pk"])
        if encounter is None:
            raise EncounterNotFoundError("Encounter not found")
        return encounter


class EncounterListCreateView(CreateAPIView):
    serializer_class = EncounterSerializer

    def perform_create(self, serializer):  # type: ignore[no-untyped-def]
        serializer.save(clinician=self.request.user)


class SignNoteView(APIView):
    def post(self, request, pk):  # type: ignore[no-untyped-def]
        encounter = get_encounter_for_user(user=request.user, encounter_id=pk)
        if encounter is None:
            raise EncounterNotFoundError("Encounter not found")
        payload = SignNoteSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        note = get_object_or_404(encounter.note_versions, id=payload.validated_data["note_id"])
        signed = sign_note(encounter=encounter, note=note, clinician=request.user)
        return Response(EncounterNoteVersionSerializer(signed).data)
