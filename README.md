# 📧 Bulk Notification Dispatcher

A production-ready Django REST Framework backend for managing, scheduling, and tracking bulk email campaigns using Celery, Redis, PostgreSQL, and Docker.

---

## 🚀 Features

- User Authentication (JWT)
- Campaign Management
- CSV Recipient Upload
- Bulk Email Sending
- Email Scheduling
- Asynchronous Task Processing (Celery)
- Redis Message Broker
- Email Open Tracking
- Email Click Tracking
- Retry Failed Emails
- Campaign Analytics Dashboard
- Campaign Reports
- Dockerized Deployment
- REST API
- Swagger API Documentation
- Unit Testing

---

# 🏗 System Architecture

```
                Client
                   │
                   ▼
         Django REST Framework
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 PostgreSQL      Redis      Celery Beat
      │            │
      │            ▼
      │      Celery Worker
      │            │
      └────────────┼──────────► SMTP Server
                   │
                   ▼
               Email Users
```

---

# 🛠 Tech Stack

## Backend

- Python 3.12
- Django
- Django REST Framework

## Database

- PostgreSQL

## Task Queue

- Celery
- Redis

## Authentication

- JWT Authentication

## Documentation

- Swagger
- DRF Spectacular

## Deployment

- Docker
- Docker Compose

---

# 📂 Project Structure

```
bulk_notification_dispatcher/

apps/
│
├── accounts/
├── campaigns/
├── recipients/
├── notifications/
├── core/
│
config/
│
Dockerfile
docker-compose.yml
requirements.txt
manage.py
README.md
```

---

# ⚡ Installation

Clone repository

```bash
git clone <repository-url>
```

Move inside project

```bash
cd bulk_notification_dispatcher
```

Create environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🐳 Docker

Start project

```bash
docker compose up --build
```

Run migrations

```bash
docker compose exec web python manage.py migrate
```

Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```
SECRET_KEY=your-secret-key

DEBUG=True

POSTGRES_DB=bulk_notification

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_HOST=db

POSTGRES_PORT=5432

EMAIL_HOST=smtp.gmail.com

EMAIL_PORT=587

EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_app_password

DEFAULT_FROM_EMAIL=your_email@gmail.com

CELERY_BROKER_URL=redis://redis:6379/0

CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

# 📬 API Endpoints

## Authentication

- Register
- Login
- Profile
- Refresh Token

## Campaigns

- Create Campaign
- Update Campaign
- Delete Campaign
- Send Campaign
- Retry Failed Emails
- Campaign Reports
- Dashboard

## Recipients

- CSV Upload
- Campaign Recipients
- Email Tracking

---

# 📊 Dashboard Metrics

- Total Campaigns
- Processing Campaigns
- Completed Campaigns
- Failed Campaigns
- Emails Sent
- Emails Failed
- Email Open Rate
- Click Rate
- Success Rate

---

# 🧪 Testing

Run authentication tests

```bash
docker compose exec web python manage.py test apps.accounts.tests.AuthenticationTests
```

Run campaign tests

```bash
docker compose exec web python manage.py test apps.campaigns.tests.CampaignAPITests
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/api/docs/
```

OpenAPI Schema

```
http://localhost:8000/api/schema/
```

---

# ✨ Future Improvements

- SMS Notifications
- Push Notifications
- WhatsApp Integration
- Email Templates
- A/B Testing
- Rate Limiting
- Multi-Tenant Support

---

# 👨‍💻 Author

**Srikanta Kamal**

Python Full Stack Developer
