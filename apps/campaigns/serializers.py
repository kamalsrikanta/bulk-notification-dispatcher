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