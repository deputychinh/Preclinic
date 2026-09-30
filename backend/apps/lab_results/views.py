from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsClinicianOrCoordinator
from apps.lab_results.models import LabImportJob
from apps.lab_results.serializers import LabImportJobSerializer
from apps.lab_results.services import start_import_job


class LabImportUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsClinicianOrCoordinator]

    def post(self, request):  # type: ignore[no-untyped-def]
        file_bytes = request.FILES["file"].read()
        job, created = start_import_job(file_bytes=file_bytes, actor=request.user)
        return Response(
            {**LabImportJobSerializer(job).data, "already_imported": not created},
            status=202 if created else 200,
        )


class LabImportJobDetailView(RetrieveAPIView):
    serializer_class = LabImportJobSerializer
    queryset = LabImportJob.objects.all()
