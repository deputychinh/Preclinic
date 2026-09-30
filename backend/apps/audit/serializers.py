from rest_framework import serializers

from apps.audit.models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.get_full_name", read_only=True)
    actor_email = serializers.EmailField(source="actor.email", read_only=True)

    class Meta:
        model = AuditEvent
        fields = [
            "id", "actor_name", "actor_email", "action", "resource_type", "resource_id",
            "patient_id", "reason", "is_break_glass", "metadata", "created_at",
        ]
        read_only_fields = fields
