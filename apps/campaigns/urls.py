from django.urls import path

from .views import (
    CampaignListCreateAPIView,
    CampaignDetailAPIView,
    SendCampaignAPIView,
    CampaignReportAPIView,
    RetryFailedEmailsAPIView,
)

urlpatterns = [
    path(
        "",
        CampaignListCreateAPIView.as_view(),
        name="campaign-list-create",
    ),

    path(
        "<int:pk>/",
        CampaignDetailAPIView.as_view(),
        name="campaign-detail",
    ),

    path(
        "<int:campaign_id>/send/",
        SendCampaignAPIView.as_view(),
        name="send-campaign",
    ),
    path(
    "<int:campaign_id>/report/",
    CampaignReportAPIView.as_view(),
    name="campaign-report",
    ),
    path(
    "<int:campaign_id>/retry/",
    RetryFailedEmailsAPIView.as_view(),
    name="retry-failed-emails",
    ),
]