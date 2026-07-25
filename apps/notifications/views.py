from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone

from apps.recipients.models import Recipient


def track_email_open(request, recipient_id):
    """
    Track email opens using a 1x1 tracking pixel.
    """

    try:
        recipient = Recipient.objects.get(id=recipient_id)

        if not recipient.is_opened:
            recipient.is_opened = True
            recipient.opened_at = timezone.now()
            recipient.save(
                update_fields=[
                    "is_opened",
                    "opened_at",
                ]
            )

    except Recipient.DoesNotExist:
        pass

    pixel = (
        b"GIF89a"
        b"\x01\x00\x01\x00"
        b"\x80\x00\x00"
        b"\x00\x00\x00"
        b"\xff\xff\xff"
        b"!\xf9\x04\x01\x00\x00\x00\x00"
        b",\x00\x00\x00\x00\x01\x00\x01\x00\x00"
        b"\x02\x02D\x01\x00;"
    )

    return HttpResponse(
        pixel,
        content_type="image/gif",
    )


def track_email_click(request, recipient_id):
    """
    Track email clicks and redirect to the actual URL.
    """

    redirect_url = request.GET.get(
        "url",
        "https://google.com",
    )

    try:

        recipient = Recipient.objects.get(
            id=recipient_id
        )

        recipient.is_clicked = True

        recipient.clicked_at = timezone.now()

        recipient.click_count += 1

        recipient.save(
            update_fields=[
                "is_clicked",
                "clicked_at",
                "click_count",
            ]
        )

    except Recipient.DoesNotExist:
        pass

    return redirect(redirect_url)