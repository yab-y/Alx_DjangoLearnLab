from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "your-secret-key"
INSTALLED_APPS = [
    # your apps
]
MIDDLEWARE = [
    # your middleware
]
ROOT_URLCONF = "social_media_api.urls"
TEMPLATES = [
    # your template settings
]
WSGI_APPLICATION = "social_media_api.wsgi.application"

# Default database (can be overridden in production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
