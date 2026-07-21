from django.conf import settings
from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def send_email(subject, message, recipient):

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )