from django.utils import timezone
from rest_framework import serializers

from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "description",
            "status",
            "total_recipients",
            "sent_count",
            "failed_count",
            "created_at",
            "updated_at",
            "scheduled_at",
            "is_scheduled",
            "website_url",
        ]

        read_only_fields = [
            "id",
            "status",
            "total_recipients",
            "sent_count",
            "failed_count",
            "created_at",
            "updated_at",
        ]

    def validate_scheduled_at(self, value):
        """
        Ensure scheduled time is in the future.
        """
        if value and value <= timezone.now():
            raise serializers.ValidationError(
                "Scheduled time must be in the future."
            )
        return value

    def create(self, validated_data):
        """
        Automatically mark the campaign as scheduled
        if scheduled_at is provided.
        """

        scheduled_at = validated_data.get("scheduled_at")

        if scheduled_at:
            validated_data["is_scheduled"] = True
            validated_data["status"] = Campaign.Status.SCHEDULED
        else:
            validated_data["is_scheduled"] = False
            validated_data["status"] = Campaign.Status.DRAFT

        return super().create(validated_data)