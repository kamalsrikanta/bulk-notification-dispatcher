from .base import *
DEBUG = False

ALLOWED_HOSTS = [
    "bulk-notification-dispatcher.onrender.com",
    ".onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://bulk-notification-dispatcher.onrender.com",
]