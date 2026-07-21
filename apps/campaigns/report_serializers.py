from rest_framework import serializers


class CampaignReportSerializer(serializers.Serializer):

    campaign = serializers.CharField()

    status = serializers.CharField()

    total_recipients = serializers.IntegerField()

    sent = serializers.IntegerField()

    failed = serializers.IntegerField()

    success_rate = serializers.CharField()