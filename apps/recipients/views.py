import pandas as pd

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.campaigns.models import Campaign

from .models import Recipient
from .serializers import (
    CSVUploadSerializer,
    RecipientSerializer,
)


class CSVUploadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        campaign = Campaign.objects.get(
            id=campaign_id,
            owner=request.user,
        )

        csv_file = serializer.validated_data["file"]

        dataframe = pd.read_csv(csv_file)

        recipients = []

        for _, row in dataframe.iterrows():

            recipients.append(
                Recipient(
                    campaign=campaign,
                    name=row["name"],
                    email=row["email"],
                )
            )

        Recipient.objects.bulk_create(recipients)

        campaign.total_recipients = Recipient.objects.filter(
            campaign=campaign
        ).count()

        campaign.save()

        return Response(
            {
                "message": "CSV uploaded successfully.",
                "total_recipients": campaign.total_recipients,
            },
            status=status.HTTP_201_CREATED,
        )


class CampaignRecipientsAPIView(ListAPIView):

    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        campaign_id = self.kwargs["campaign_id"]

        return Recipient.objects.filter(
            campaign__id=campaign_id,
            campaign__owner=self.request.user,
        )