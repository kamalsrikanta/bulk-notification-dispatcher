# Bulk Notification Dispatcher

A production-inspired backend system built with Django REST Framework for managing, scheduling, and tracking bulk email campaigns using asynchronous task processing with Celery and Redis.


## Overview

Sending thousands of emails synchronously blocks the application and creates poor user experience.

This project demonstrates how modern backend systems solve this problem using asynchronous task queues.

Users can create campaigns, upload recipients through CSV files, schedule email delivery, monitor campaign progress, retry failed deliveries, and analyse campaign performance through REST APIs.

The application follows a modular Django architecture and integrates Celery, Redis, PostgreSQL, Docker, and JWT authentication to simulate a production-ready notification service.

---

## Features

- JWT Authentication
- Campaign Management
- CSV Recipient Upload
- Asynchronous Email Processing
- Email Scheduling
- Retry Failed Emails
- Campaign Analytics Dashboard
- Email Open Tracking
- Email Click Tracking
- Swagger API Documentation
- Docker Support
- PostgreSQL Database
- Celery + Redis Task Queue
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

| Category | Technology |
|----------|------------|
| Backend | Django, DRF |
| Database | PostgreSQL |
| Queue | Celery |
| Broker | Redis |
| Authentication | JWT |
| Documentation | Swagger |
| Containerization | Docker |

---

# 📂 Project Structure

```
apps/
 ├── accounts/
 ├── campaigns/
 ├── notifications/
 ├── recipients/
 └── core/

config/
Dockerfile
docker-compose.yml
manage.py
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

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| POST   | /login             | Login           |
| POST   | /campaigns         | Create campaign |
| POST   | /recipients/upload | Upload CSV      |
| POST   | /campaigns/send    | Send campaign   |
| GET    | /dashboard         | Analytics       |

---

# 📖 Screenshots


Swagger UI
<img width="1276" height="855" alt="Swagger" src="https://github.com/user-attachments/assets/05eae4a8-2798-408b-8a57-03d80b778442" />


```
http://localhost:8000/api/docs/
```

OpenAPI Schema

```
http://localhost:8000/api/schema/
```
## Live Demo

Application

https://bulk-notification-dispatcher.onrender.com/

Swagger

https://bulk-notification-dispatcher.onrender.com/api/docs/

Health Check

https://bulk-notification-dispatcher.onrender.com/health/

Admin 

https://bulk-notification-dispatcher.onrender.com/admin/login/?next=/admin/

---

## Note

The hosted demo currently runs the Django web service.

Celery Worker and Celery Beat are disabled in the deployed environment because Render requires separate paid worker services.

The complete asynchronous workflow runs correctly in the Docker-based local environment.

# ✨ Future Improvements

- Per-recipient Celery task distribution for improved scalability
- Flower dashboard for Celery monitoring
- GitHub Actions CI/CD
- Rate limiting
- Email template engine
- SMS and WhatsApp notifications
- Amazon SES integration
- Multi-tenant support

---

# 👨‍💻 Author

**Srikanta Kamal**

Python Full Stack Developer
