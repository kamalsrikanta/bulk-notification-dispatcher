import pandas as pd

from rest_framework import serializers

from .models import Recipient


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    REQUIRED_COLUMNS = {
        "name",
        "email",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    def validate_file(self, value):

        # -------------------------
        # File extension
        # -------------------------
        if not value.name.lower().endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )

        # -------------------------
        # File size
        # -------------------------
        if value.size > self.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                "CSV file exceeds the maximum size of 5 MB."
            )

        # -------------------------
        # Read CSV
        # -------------------------
        try:
            dataframe = pd.read_csv(value)

        except Exception:
            raise serializers.ValidationError(
                "Unable to read CSV file."
            )

        if dataframe.empty:
            raise serializers.ValidationError(
                "CSV file is empty."
            )

        # -------------------------
        # Required Columns
        # -------------------------
        missing_columns = (
            self.REQUIRED_COLUMNS -
            set(dataframe.columns)
        )

        if missing_columns:
            raise serializers.ValidationError(
                f"Missing required columns: "
                f"{', '.join(sorted(missing_columns))}"
            )

        # -------------------------
        # Remove blank rows
        # -------------------------
        dataframe = dataframe.dropna(
            how="all"
        )

        if dataframe.empty:
            raise serializers.ValidationError(
                "CSV contains no valid rows."
            )

        # -------------------------
        # Validate Name
        # -------------------------
        if dataframe["name"].isnull().any():
            raise serializers.ValidationError(
                "Some recipients have an empty name."
            )

        # -------------------------
        # Validate Email
        # -------------------------
        if dataframe["email"].isnull().any():
            raise serializers.ValidationError(
                "Some recipients have an empty email."
            )

        # -------------------------
        # Duplicate Emails
        # -------------------------
        duplicate_emails = dataframe[
            dataframe["email"].duplicated()
        ]

        if not duplicate_emails.empty:

            duplicates = (
                duplicate_emails["email"]
                .astype(str)
                .tolist()
            )

            raise serializers.ValidationError(
                f"Duplicate email(s) found: "
                f"{', '.join(duplicates)}"
            )

        # Reset stream for pandas reuse
        value.seek(0)

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
            "is_opened",
            "opened_at",
            "is_clicked",
            "clicked_at",
            "click_count",
        ]

        read_only_fields = fields