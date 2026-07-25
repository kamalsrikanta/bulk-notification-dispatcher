from django.conf import settings
from django.db import models


class Campaign(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SCHEDULED = "SCHEDULED", "Scheduled"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns",
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )
    website_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Destination URL when recipients click the email button.",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    total_recipients = models.PositiveIntegerField(
        default=0,
    )

    sent_count = models.PositiveIntegerField(
        default=0,
    )

    failed_count = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # NEW: Date & time when the campaign should be sent
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # NEW: Indicates whether this campaign should be sent automatically
    is_scheduled = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name