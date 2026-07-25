# Bulk Notification Dispatcher Architecture

```text
                   User
                    │
                    ▼
             Django REST API
                    │
     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼
Authentication   Campaign API   Recipient API
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
              PostgreSQL Database
                    │
                    ▼
            Celery Task Queue
                    │
              Redis Broker
                    │
                    ▼
             Celery Workers
                    │
                    ▼
              SMTP Email Server
                    │
                    ▼
               Email Recipients
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   Open Tracking           Click Tracking
        │                       │
        └───────────┬───────────┘
                    ▼
              Dashboard Analytics
```