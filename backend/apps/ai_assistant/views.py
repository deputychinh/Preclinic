from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai_assistant.models import AIDraft
from apps.ai_assistant.serializers import AIDraftSerializer
from apps.ai_assistant.services import approve_draft, request_ai_draft
from apps.common.exceptions import AppError
from apps.encounters.selectors import get_encounter_for_user
from apps.encounters.serializers import EncounterNoteVersionSerializer


class EncounterNotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class AIDraftRequestView(APIView):
    def post(self, request, encounter_id):  # type: ignore[no-untyped-def]
        encounter = get_encounter_for_user(user=request.user, encounter_id=encounter_id)
        if encounter is None:
            raise EncounterNotFoundError("Encounter not found")
        draft = request_ai_draft(encounter=encounter, actor=request.user)
        return Response(AIDraftSerializer(draft).data, status=202)


class AIDraftDetailView(RetrieveAPIView):
    serializer_class = AIDraftSerializer
    queryset = AIDraft.objects.all()


class AIDraftApproveView(APIView):
    def post(self, request, pk):  # type: ignore[no-untyped-def]
        draft = get_object_or_404(AIDraft, id=pk)
        note = approve_draft(draft=draft, clinician=request.user)
        return Response(EncounterNoteVersionSerializer(note).data, status=201)
