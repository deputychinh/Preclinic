from .base import *

DEBUG = False
SECRET_KEY = "test-secret-key"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "carepath_test",
        "USER": "carepath",
        "PASSWORD": "carepath",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # fast tests only
INSTALLED_APPS = [*INSTALLED_APPS]
