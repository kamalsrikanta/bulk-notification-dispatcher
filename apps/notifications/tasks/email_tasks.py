import logging

from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from apps.campaigns.models import Campaign
from apps.recipients.models import Recipient


logger = logging.getLogger(__name__)


@shared_task
def send_campaign_emails(campaign_id):

    logger.info(f"Campaign {campaign_id} started")

    campaign = Campaign.objects.get(id=campaign_id)

    campaign.status = Campaign.Status.PROCESSING
    campaign.save()

    recipients = Recipient.objects.filter(campaign=campaign)

    sent = 0
    failed = 0

    company_name = (
        campaign.owner.company_name
        if campaign.owner.company_name
        else "Bulk Notification Dispatcher"
    )

    for recipient in recipients:

        try:

            logger.info(f"Sending email to {recipient.email}")

            html_content = render_to_string(
                "emails/campaign_email.html",
                {
                    "campaign": campaign,
                    "recipient": recipient,
                    "company_name": company_name,
                },
            )

            text_content = (
                f"Hello {recipient.name},\n\n"
                f"{campaign.description}\n\n"
                f"Regards,\n{company_name}"
            )

            email = EmailMultiAlternatives(
                subject=campaign.name,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient.email],
            )

            email.attach_alternative(
                html_content,
                "text/html",
            )

            email.send()

            recipient.status = Recipient.Status.SENT
            recipient.sent_at = timezone.now()
            recipient.error_message = ""
            recipient.save()

            logger.info(f"Email sent to {recipient.email}")

            sent += 1

        except Exception as e:

            logger.error(
                f"Failed sending email to {recipient.email}: {str(e)}"
            )

            recipient.status = Recipient.Status.FAILED
            recipient.error_message = str(e)
            recipient.save()

            failed += 1

    campaign.sent_count = sent
    campaign.failed_count = failed
    campaign.status = Campaign.Status.COMPLETED
    campaign.save()

    logger.info(
        f"Campaign {campaign_id} completed. Sent={sent}, Failed={failed}"
    )

    return f"Sent: {sent}, Failed: {failed}"