from .base import *  # base.py must define BASE_DIR
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["your-heroku-app.herokuapp.com", "127.0.0.1"]

# Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

# Database
DATABASES['default'] = dj_database_url.config(
    default='sqlite:///db.sqlite3',  # fallback for local testing
    conn_max_age=600)
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
