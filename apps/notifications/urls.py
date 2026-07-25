from django.urls import path

from .views import (
    track_email_open,
    track_email_click,
)

urlpatterns = [

    path(
        "track/open/<int:recipient_id>/",
        track_email_open,
        name="track-email-open",
    ),

    path(
        "track/click/<int:recipient_id>/",
        track_email_click,
        name="track-email-click",
    ),

]