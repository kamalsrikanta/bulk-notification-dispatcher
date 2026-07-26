# Bulk Notification Dispatcher – Asynchronous Email Campaign Management System

A production-inspired backend system built with Django REST Framework for managing, scheduling, and tracking bulk email campaigns using asynchronous task processing with Celery and Redis.


## Overview

Sending thousands of emails synchronously blocks the application and creates poor user experience.

This project demonstrates how modern backend systems solve this problem using asynchronous task queues.

Users can create campaigns, upload recipients through CSV files, schedule email delivery, monitor campaign progress, retry failed deliveries, and analyse campaign performance through REST APIs.

The application follows a modular Django architecture and integrates Celery, Redis, PostgreSQL, Docker, and JWT authentication to simulate a production-ready notification service.

---
## Key Highlights

- Asynchronous task processing using Celery
- Redis-based message broker
- Dockerized multi-service architecture
- JWT secured REST APIs
- CSV-based bulk recipient upload
- Email scheduling and retry mechanism
- Campaign analytics and tracking
- OpenAPI (Swagger) documentation

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


**Login**

<img width="900" height="728" alt="Login" src="https://github.com/user-attachments/assets/ba327ebc-633d-4604-a716-9dda1d752774" />



**Swagger UI**
<img width="900" height="855" alt="Swagger" src="https://github.com/user-attachments/assets/a4233499-a58d-4fe3-977b-125d0a989837" />


**health**

<img width="900" height="922" alt="health" src="https://github.com/user-attachments/assets/54de85af-4b22-4222-95aa-a39d5e159169" />


```
```

```
**## Live Demo
**
🌐 **Application**

https://bulk-notification-dispatcher.onrender.com/

📖 **Swagger**

https://bulk-notification-dispatcher.onrender.com/api/docs/

❤️ **Health Check**

https://bulk-notification-dispatcher.onrender.com/health/

⚙️ **Admin**

https://bulk-notification-dispatcher.onrender.com/admin/

## Note

The hosted demo currently runs the Django web service.

Celery Worker and Celery Beat are disabled in the deployed environment because Render requires separate paid worker services.

The complete asynchronous workflow runs correctly in the Docker-based local environment.

# ✨ Future Improvements


✔ Per-recipient task distribution

✔ Flower monitoring

✔ GitHub Actions

✔ Rate limiting

✔ Amazon SES

✔ Email templates

✔ Multi-tenant architecture

✔ WebSocket live progress

✔ RabbitMQ supportt

---

# 👨‍💻 Author

**Srikanta Kamal**

Python Full Stack Developer
