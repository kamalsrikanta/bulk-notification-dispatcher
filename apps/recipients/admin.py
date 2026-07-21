from django.contrib import admin

from .models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "campaign",
        "name",
        "email",
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
    )

    list_filter = (
        "status",
    )