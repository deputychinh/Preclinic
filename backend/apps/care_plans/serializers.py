from rest_framework import serializers

from apps.care_plans.models import CarePlan, CarePlanTask


class CarePlanTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePlanTask
        fields = ["id", "description", "due_date", "completed_at"]


class CarePlanSerializer(serializers.ModelSerializer):
    tasks = CarePlanTaskSerializer(many=True, read_only=True)

    class Meta:
        model = CarePlan
        fields = ["id", "patient", "title", "goal", "tasks"]
