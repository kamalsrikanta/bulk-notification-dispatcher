from celery import shared_task
from django.utils import timezone

from apps.campaigns.models import Campaign
from apps.notifications.tasks.email_tasks import send_campaign_emails


@shared_task
def process_scheduled_campaigns():
    """
    Find all campaigns that are due and queue them for sending.
    """

    campaigns = Campaign.objects.filter(
        is_scheduled=True,
        status=Campaign.Status.SCHEDULED,
        scheduled_at__lte=timezone.now(),
    )

    for campaign in campaigns:
        send_campaign_emails.delay(campaign.id)