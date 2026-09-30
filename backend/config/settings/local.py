import os

from .base import *

DEBUG = True
SECRET_KEY = "local-dev-secret-key-not-for-production"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "carepath"),
        "USER": os.environ.get("POSTGRES_USER", "carepath"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "carepath"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # npm run dev
    "http://localhost:4173",  # vite preview
    "http://localhost:5180",  # docker-compose (nginx serving the built SPA)
]

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

INSTALLED_APPS = [*INSTALLED_APPS, "corsheaders"]
