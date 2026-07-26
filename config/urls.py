from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "application": "Bulk Notification Dispatcher",
        "version": "1.0",
        "status": "Running",
        "health": "/health/",
        "docs": "/api/schema/swagger/"
    })

urlpatterns = [
    path("", home),

    path("admin/", admin.site.urls),

    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/campaigns/", include("apps.campaigns.urls")),
    path("api/", include("apps.recipients.urls")),
    path("api/", include("apps.notifications.urls")),

    path("", include("apps.core.urls")),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]