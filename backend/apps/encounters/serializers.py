from rest_framework import serializers

from apps.encounters.models import DiagnosisCode, Encounter, EncounterNoteVersion


class DiagnosisCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        fields = ["id", "code", "description"]


class EncounterNoteVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncounterNoteVersion
        fields = ["id", "version", "source", "content", "signed_by", "signed_at", "supersedes"]
        read_only_fields = fields


class EncounterSerializer(serializers.ModelSerializer):
    diagnosis_codes = DiagnosisCodeSerializer(many=True, read_only=True)
    note_versions = EncounterNoteVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Encounter
        fields = [
            "id", "patient", "clinician", "status", "reason", "occurred_at",
            "diagnosis_codes", "note_versions",
        ]
        read_only_fields = ["id", "clinician", "status", "diagnosis_codes", "note_versions"]


class SignNoteSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()
