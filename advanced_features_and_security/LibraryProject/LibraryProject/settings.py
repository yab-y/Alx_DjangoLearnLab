"""
Django settings for LibraryProject project.

Security-related HTTPS and headers settings included.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'

# IMPORTANT: Set to False in production only; True disables HTTPS enforcement
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# SECURITY SETTINGS FOR HTTPS AND SECURE HEADERS

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True
# Documentation: Ensures all requests use HTTPS, preventing unencrypted traffic.

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Documentation: Instructs browsers to always connect via HTTPS for the specified duration.
# Including subdomains and enabling preload improves security coverage.

# Secure cookies settings to transmit cookies only over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Documentation: Protects session and CSRF cookies from being sent over insecure connections.

# Prevent clickjacking by not allowing the site to be embedded in frames
X_FRAME_OPTIONS = 'DENY'
# Documentation: Blocks framing of your site to protect against clickjacking attacks.

# Prevent MIME sniffing to reduce risk of drive-by downloads
SECURE_CONTENT_TYPE_NOSNIFF = True
# Documentation: Forces browser to respect the declared content-type of resources.

# Enable the browser's built-in XSS protection
SECURE_BROWSER_XSS_FILTER = True
# Documentation: Adds header to enable the browser’s cross-site scripting filter.

# Other standard settings omitted for brevity...
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
