from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< Updated upstream
SECRET_KEY = 'django-insecure-ri)pg8z_1r4@t_=3-0ucm0h-z0)dl^og#ecz3s1#*q)1@kiw2-'

DEBUG = True

ALLOWED_HOSTS = []
=======
SECRET_KEY = 'django-eventify-secret-key-2025-very-secure'
DEBUG      = True
ALLOWED_HOSTS = ['*']
>>>>>>> Stashed changes

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
<<<<<<< Updated upstream
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eventify_db',
        'USER': 'eventify_user',
        'PASSWORD': 'olise',
        'HOST': 'localhost',
        'PORT': '5432',
=======
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : 'eventify_db',
        'USER'    : 'eventify_user',
        'PASSWORD': 'olise',
        'HOST'    : 'localhost',
        'PORT'    : '5432',
>>>>>>> Stashed changes
    }
}

AUTH_USER_MODEL = 'api.User'
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Dakar'
USE_I18N      = True
USE_TZ        = True

STATIC_URL = '/static/'
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

<<<<<<< Updated upstream
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
=======
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
>>>>>>> Stashed changes
