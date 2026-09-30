from rest_framework import serializers

from apps.ai_assistant.models import AIDraft


class AIDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDraft
        fields = ["id", "encounter", "status", "content", "model_name", "tool_calls", "error"]
        read_only_fields = fields
