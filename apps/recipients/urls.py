from django.urls import path

from .views import (
    CSVUploadAPIView,
    CampaignRecipientsAPIView,
)

urlpatterns = [

    path(
        "campaigns/<int:campaign_id>/upload/",
        CSVUploadAPIView.as_view(),
        name="csv-upload",
    ),

    path(
        "campaigns/<int:campaign_id>/recipients/",
        CampaignRecipientsAPIView.as_view(),
        name="campaign-recipients",
    ),
]