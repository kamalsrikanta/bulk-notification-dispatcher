from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_campaigns = serializers.IntegerField()

    draft_campaigns = serializers.IntegerField()

    processing_campaigns = serializers.IntegerField()

    completed_campaigns = serializers.IntegerField()

    failed_campaigns = serializers.IntegerField()

    total_recipients = serializers.IntegerField()

    emails_sent = serializers.IntegerField()

    emails_failed = serializers.IntegerField()

    emails_opened = serializers.IntegerField()

    emails_clicked = serializers.IntegerField()

    success_rate = serializers.CharField()

    open_rate = serializers.CharField()

    click_rate = serializers.CharField()