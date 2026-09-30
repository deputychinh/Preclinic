from rest_framework import serializers

from apps.patients.models import Allergy, Consent, Medication, Patient


class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "mrn", "full_name", "date_of_birth"]
        read_only_fields = fields


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ["id", "substance", "reaction", "severity"]


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "name", "dosage", "frequency", "active"]


class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = ["id", "consent_type", "granted_at", "revoked_at"]


class PatientDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    allergies = AllergySerializer(many=True, read_only=True)
    medications = MedicationSerializer(many=True, read_only=True)
    consents = ConsentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id", "mrn", "full_name", "first_name", "last_name", "date_of_birth",
            "allergies", "medications", "consents",
        ]
        read_only_fields = fields
