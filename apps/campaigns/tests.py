from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.campaigns.models import Campaign
from apps.recipients.models import Recipient


class CampaignAPITests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="kamal",
            email="kamal@test.com",
            password="Test@12345",
        )

        login = self.client.post(
            reverse("login"),
            {
                "email": "kamal@test.com",
                "password": "Test@12345",
            },
            format="json",
        )

        self.token = login.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.campaign = Campaign.objects.create(
            owner=self.user,
            name="Summer Campaign",
            description="Testing Campaign",
        )

        # Create one recipient so campaign can be sent
        Recipient.objects.create(
            campaign=self.campaign,
            name="John Doe",
            email="john@example.com",
        )

        # Keep campaign statistics consistent
        self.campaign.total_recipients = 1
        self.campaign.save()

    def test_create_campaign(self):

        response = self.client.post(
            reverse("campaign-list-create"),
            {
                "name": "New Campaign",
                "description": "Campaign Description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_list_campaigns(self):

        response = self.client.get(
            reverse("campaign-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_campaign(self):

        response = self.client.get(
            reverse(
                "campaign-detail",
                args=[self.campaign.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_campaign(self):

        response = self.client.patch(
            reverse(
                "campaign-detail",
                args=[self.campaign.id],
            ),
            {
                "description": "Updated Description"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_campaign(self):

        response = self.client.delete(
            reverse(
                "campaign-detail",
                args=[self.campaign.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_dashboard(self):

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_campaign_report(self):

        response = self.client.get(
            reverse(
                "campaign-report",
                args=[self.campaign.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_send_campaign(self):

        response = self.client.post(
            reverse(
                "send-campaign",
                args=[self.campaign.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retry_failed(self):

        # Simulate a failed email
        self.campaign.failed_count = 1
        self.campaign.save()

        response = self.client.post(
            reverse(
                "retry-failed-emails",
                args=[self.campaign.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )