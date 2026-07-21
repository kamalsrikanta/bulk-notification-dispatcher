from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Campaign
from .serializers import CampaignSerializer
from apps.notifications.tasks import send_campaign_emails
from .report_serializers import CampaignReportSerializer
from apps.notifications.tasks import retry_failed_emails

class CampaignListCreateAPIView(ListCreateAPIView):
    """
    GET  -> List all campaigns of the logged-in user
    POST -> Create a new campaign
    """

    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only campaigns owned by the logged-in user.
        """
        return Campaign.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Create a new campaign and assign it to the logged-in user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(owner=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CampaignDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve a campaign
    PUT    -> Update an entire campaign
    PATCH  -> Partially update a campaign
    DELETE -> Delete a campaign
    """

    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only access their own campaigns.
        """
        return Campaign.objects.filter(
            owner=self.request.user
        )
class SendCampaignAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        campaign = Campaign.objects.get(
            id=campaign_id,
            owner=request.user,
        )

        send_campaign_emails.delay(campaign.id)

        return Response(
            {
                "message": "Campaign started successfully."
            },
            status=status.HTTP_200_OK,
        )
class CampaignReportAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, campaign_id):

        campaign = Campaign.objects.get(
            id=campaign_id,
            owner=request.user,
        )

        total = campaign.total_recipients
        sent = campaign.sent_count
        failed = campaign.failed_count

        if total > 0:
            success_rate = f"{(sent / total) * 100:.2f}%"
        else:
            success_rate = "0.00%"

        data = {
            "campaign": campaign.name,
            "status": campaign.status,
            "total_recipients": total,
            "sent": sent,
            "failed": failed,
            "success_rate": success_rate,
        }

        serializer = CampaignReportSerializer(data)

        return Response(serializer.data)
class RetryFailedEmailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        campaign = Campaign.objects.get(
            id=campaign_id,
            owner=request.user,
        )

        retry_failed_emails.delay(campaign.id)

        return Response(
            {
                "message": "Retry started successfully."
            },
            status=status.HTTP_200_OK,
        )