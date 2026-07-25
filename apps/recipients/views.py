import logging

import pandas as pd

from django.shortcuts import get_object_or_404

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

logger = logging.getLogger(__name__)


class CSVUploadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):

        campaign = get_object_or_404(
            Campaign,
            id=campaign_id,
            owner=request.user,
        )

        serializer = CSVUploadSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data["file"]

        dataframe = pd.read_csv(csv_file)

        logger.info(
            f"CSV upload started for Campaign {campaign.id}"
        )

        existing_emails = set(
            Recipient.objects.filter(
                campaign=campaign
            ).values_list(
                "email",
                flat=True,
            )
        )

        recipients = []

        skipped_duplicates = 0

        for _, row in dataframe.iterrows():

            email = str(row["email"]).strip().lower()

            if email in existing_emails:
                skipped_duplicates += 1
                continue

            recipients.append(
                Recipient(
                    campaign=campaign,
                    name=str(row["name"]).strip(),
                    email=email,
                )
            )

            existing_emails.add(email)

        if recipients:

            Recipient.objects.bulk_create(
                recipients,
                batch_size=1000,
            )

        campaign.total_recipients = Recipient.objects.filter(
            campaign=campaign
        ).count()

        campaign.save(
            update_fields=[
                "total_recipients",
            ]
        )

        logger.info(
            f"Campaign {campaign.id}: "
            f"{len(recipients)} recipients imported, "
            f"{skipped_duplicates} duplicates skipped."
        )

        return Response(
            {
                "message": "CSV uploaded successfully.",
                "campaign_id": campaign.id,
                "uploaded": len(recipients),
                "duplicates_skipped": skipped_duplicates,
                "total_recipients": campaign.total_recipients,
            },
            status=status.HTTP_201_CREATED,
        )


class CampaignRecipientsAPIView(ListAPIView):

    serializer_class = RecipientSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):

        campaign = get_object_or_404(
            Campaign,
            id=self.kwargs["campaign_id"],
            owner=self.request.user,
        )

        return Recipient.objects.filter(
            campaign=campaign
        ).order_by(
            "id"
        )