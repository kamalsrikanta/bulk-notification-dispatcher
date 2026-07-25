from django.db import connection
from django.utils.timezone import now
from django.conf import settings

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import redis


class HealthCheckAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        overall_status = "healthy"

        # -----------------------------
        # Database
        # -----------------------------
        try:
            connection.ensure_connection()

            database = {
                "status": "connected",
                "engine": connection.vendor,
            }

        except Exception as e:

            overall_status = "unhealthy"

            database = {
                "status": "disconnected",
                "error": str(e),
            }

        # -----------------------------
        # Redis
        # -----------------------------
        try:

            client = redis.Redis(
                host="redis",
                port=6379,
                db=0,
            )

            client.ping()

            redis_status = {
                "status": "connected",
            }

        except Exception as e:

            overall_status = "unhealthy"

            redis_status = {
                "status": "disconnected",
                "error": str(e),
            }

        # -----------------------------
        # Celery
        # -----------------------------
        try:

            from config.celery import app

            inspector = app.control.inspect()

            active_workers = inspector.ping()

            if active_workers:

                celery = {
                    "status": "connected",
                    "workers": list(active_workers.keys()),
                }

            else:

                overall_status = "unhealthy"

                celery = {
                    "status": "disconnected",
                    "workers": [],
                }

        except Exception as e:

            overall_status = "unhealthy"

            celery = {
                "status": "disconnected",
                "error": str(e),
            }

        # -----------------------------
        # Response
        # -----------------------------
        return Response(
            {
                "application": "Bulk Notification Dispatcher",
                "environment": "development" if settings.DEBUG else "production",
                "status": overall_status,
                "database": database,
                "redis": redis_status,
                "celery": celery,
                "timestamp": now(),
            }
        )