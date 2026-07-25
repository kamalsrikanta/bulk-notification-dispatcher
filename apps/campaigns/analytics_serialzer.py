from rest_framework import serializers


class CampaignAnalyticsSerializer(serializers.Serializer):

    campaign = serializers.CharField()

    total_recipients = serializers.IntegerField()

    sent = serializers.IntegerField()

    failed = serializers.IntegerField()

    opened = serializers.IntegerField()

    clicked = serializers.IntegerField()

    delivery_rate = serializers.CharField()

    open_rate = serializers.CharField()

    click_rate = serializers.CharField()