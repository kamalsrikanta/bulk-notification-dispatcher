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
def retry_failed_emails(campaign_id):

    logger.info(f"Retry task started for campaign {campaign_id}")

    campaign = Campaign.objects.get(id=campaign_id)

    failed_recipients = Recipient.objects.filter(
        campaign=campaign,
        status=Recipient.Status.FAILED,
    )

    sent = campaign.sent_count
    failed = campaign.failed_count

    company_name = (
        campaign.owner.company_name
        if campaign.owner.company_name
        else "Bulk Notification Dispatcher"
    )

    for recipient in failed_recipients:

        try:

            logger.info(f"Retrying {recipient.email}")

            html_content = render_to_string(
                "emails/campaign_email.html",
                {
                    "campaign": campaign,
                    "recipient": recipient,
                    "company_name": company_name,
                },
            )

            text_content = (
                f"Hello {recipient.name}\n\n"
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

            logger.info(f"Retry successful for {recipient.email}")

            sent += 1
            failed -= 1

        except Exception as e:

            logger.error(
                f"Retry failed for {recipient.email}: {str(e)}"
            )

            recipient.error_message = str(e)
            recipient.save()

    campaign.sent_count = sent
    campaign.failed_count = failed

    if failed == 0:
        campaign.status = Campaign.Status.COMPLETED

    campaign.save()

    logger.info(
        f"Retry task completed for campaign {campaign_id}. Remaining failed={failed}"
    )

    return f"Retried {failed_recipients.count()} recipients"