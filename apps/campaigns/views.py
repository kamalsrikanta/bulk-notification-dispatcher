import logging

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.tasks import (
    retry_failed_emails,
    send_campaign_emails,
)
from apps.recipients.models import Recipient

from .dashboard_serializer import DashboardSerializer
from .models import Campaign
from .report_serializers import CampaignReportSerializer
from .serializers import CampaignSerializer

logger = logging.getLogger(__name__)


class CampaignListCreateAPIView(ListCreateAPIView):

    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "is_scheduled",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "name",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return Campaign.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        campaign = serializer.save(owner=request.user)

        logger.info(f"Campaign {campaign.id} created.")

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CampaignDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(
            owner=self.request.user
        )


class SendCampaignAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        campaign = get_object_or_404(
            Campaign,
            id=campaign_id,
            owner=request.user,
        )

        if campaign.total_recipients == 0:
            return Response(
                {
                    "error": "Campaign has no recipients."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"Campaign {campaign.id} send requested.")

        if (
            campaign.scheduled_at
            and campaign.scheduled_at > timezone.now()
        ):

            send_campaign_emails.apply_async(
                args=[campaign.id],
                eta=campaign.scheduled_at,
            )

            logger.info(f"Campaign {campaign.id} scheduled.")

            return Response(
                {
                    "message": "Campaign scheduled successfully.",
                    "campaign_id": campaign.id,
                    "scheduled_at": campaign.scheduled_at,
                }
            )

        send_campaign_emails.delay(campaign.id)

        logger.info(f"Campaign {campaign.id} queued.")

        return Response(
            {
                "message": "Campaign started successfully.",
                "campaign_id": campaign.id,
            }
        )


class CampaignReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, campaign_id):

        campaign = get_object_or_404(
            Campaign,
            id=campaign_id,
            owner=request.user,
        )

        total = campaign.total_recipients
        sent = campaign.sent_count
        failed = campaign.failed_count

        success_rate = (
            f"{(sent / total) * 100:.2f}%"
            if total
            else "0.00%"
        )

        logger.info(
            f"Report generated for Campaign {campaign.id}"
        )

        serializer = CampaignReportSerializer(
            {
                "campaign": campaign.name,
                "status": campaign.status,
                "total_recipients": total,
                "sent": sent,
                "failed": failed,
                "success_rate": success_rate,
            }
        )

        return Response(serializer.data)


class RetryFailedEmailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        campaign = get_object_or_404(
            Campaign,
            id=campaign_id,
            owner=request.user,
        )

        if campaign.failed_count == 0:
            return Response(
                {
                    "message": "No failed emails to retry."
                }
            )

        retry_failed_emails.delay(campaign.id)

        logger.info(
            f"Retry queued for Campaign {campaign.id}"
        )

        return Response(
            {
                "message": "Retry started successfully.",
                "campaign_id": campaign.id,
            }
        )


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        campaigns = Campaign.objects.filter(
            owner=request.user
        )

        total_campaigns = campaigns.count()

        draft_campaigns = campaigns.filter(
            status=Campaign.Status.DRAFT
        ).count()

        processing_campaigns = campaigns.filter(
            status=Campaign.Status.PROCESSING
        ).count()

        completed_campaigns = campaigns.filter(
            status=Campaign.Status.COMPLETED
        ).count()

        failed_campaigns = campaigns.filter(
            status=Campaign.Status.FAILED
        ).count()

        totals = campaigns.aggregate(
            total_recipients=Sum("total_recipients"),
            emails_sent=Sum("sent_count"),
            emails_failed=Sum("failed_count"),
        )

        total_recipients = totals["total_recipients"] or 0
        emails_sent = totals["emails_sent"] or 0
        emails_failed = totals["emails_failed"] or 0

        emails_opened = Recipient.objects.filter(
            campaign__owner=request.user,
            is_opened=True,
        ).count()

        emails_clicked = Recipient.objects.filter(
            campaign__owner=request.user,
            is_clicked=True,
        ).count()

        success_rate = (
            (emails_sent / total_recipients) * 100
            if total_recipients
            else 0
        )

        open_rate = (
            (emails_opened / emails_sent) * 100
            if emails_sent
            else 0
        )

        click_rate = (
            (emails_clicked / emails_opened) * 100
            if emails_opened
            else 0
        )

        logger.info("Dashboard loaded.")

        serializer = DashboardSerializer(
            {
                "total_campaigns": total_campaigns,
                "draft_campaigns": draft_campaigns,
                "processing_campaigns": processing_campaigns,
                "completed_campaigns": completed_campaigns,
                "failed_campaigns": failed_campaigns,
                "total_recipients": total_recipients,
                "emails_sent": emails_sent,
                "emails_failed": emails_failed,
                "emails_opened": emails_opened,
                "emails_clicked": emails_clicked,
                "success_rate": f"{success_rate:.2f}%",
                "open_rate": f"{open_rate:.2f}%",
                "click_rate": f"{click_rate:.2f}%",
            }
        )

        return Response(serializer.data)