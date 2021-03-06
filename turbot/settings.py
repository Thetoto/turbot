"""
Django settings for turbot project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path
import environ
from slack import WebClient
from dateutil import parser

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent.absolute()

environ.Env().read_env(str(BASE_DIR / ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["slack.thetoto.fr", "slack-dev.thetoto.fr", "newaltair.herokuapp.com"]


# Application definition

BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = []

LOCAL_APPS = [
    "polls.apps.PollsConfig",
    "workspaces.apps.WorkspacesConfig",
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "turbot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "turbot.wsgi.application"


# Database (Override with DATABASE_URL)
DATABASES = {"default": env.db(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Sentry
SENTRY_DSN = env("SENTRY_DSN", default=None)

if SENTRY_DSN != None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(SENTRY_DSN, integrations=[DjangoIntegration()])

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"
STATICFILES_DIR = os.path.join(BASE_DIR, "static")

SLACK_API_TOKEN = env("SLACK_API_TOKEN")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "slackbot": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="DEBUG"),
        }
    },
}

ERROR_ICON_URL = env("ERROR_ICON_URL", default=None)

SLACK_CLIENT = WebClient(SLACK_API_TOKEN)

NIGHT_START = parser.parse(env("NIGHT_START", default="23:00")).time()
NIGHT_END = parser.parse(env("NIGHT_END", default="09:00")).time()

PHOTO_FSTRING = env("PHOTO_FSTRING", default="https://picsum.photos/200?{}")
PHOTO_FSTRING_SQUARE = env(
    "PHOTO_FSTRING_SQUARE", default="https://picsum.photos/200?{}"
)

TURBOT_USER_ID = env("TURBOT_USER_ID", default="Turbot")

ALGOLIA_APP_ID = env("ALGOLIA_APP_ID", default=None)
ALGOLIA_API_KEY = env("ALGOLIA_API_KEY", default=None)
ALGOLIA_INDEX = env("ALGOLIA_INDEX", default=None)
