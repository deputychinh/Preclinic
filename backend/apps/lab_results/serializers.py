from rest_framework import serializers

from apps.lab_results.models import LabImportJob, LabResult


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = ["id", "patient", "test_name", "value", "unit", "observed_at"]


class LabImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabImportJob
        fields = ["id", "status", "total_rows", "imported_rows", "error_report", "created_at"]
        read_only_fields = fields
