from rest_framework import serializers

from apps.referrals.models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ["id", "patient", "specialty", "reason", "status", "referring_clinician"]
        read_only_fields = ["id", "status", "referring_clinician"]
