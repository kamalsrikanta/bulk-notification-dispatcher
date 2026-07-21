from rest_framework import serializers

from .models import Recipient


class CSVUploadSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(self, value):

        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )

        return value


class RecipientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipient
        fields = [
            "id",
            "name",
            "email",
            "status",
            "sent_at",
            "error_message",
        ]