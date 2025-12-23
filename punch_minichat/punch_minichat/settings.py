"""
Django settings for punch_minichat project.
"""

from pathlib import Path
from datetime import timedelta

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# SECURITY (LOCAL)
# --------------------------------------------------
SECRET_KEY = "django-insecure-*k=8#5hlo$$z2n*yi9msg+o2qfl*fq*^kvc(pvkq&*&vhjyp5l"

DEBUG = True

ALLOWED_HOSTS = []

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "channels",
    "whitenoise.runserver_nostatic",

    # Local apps
    "accounts",
    "chat",
    "groupchat",
    "forget_password",
    "frontend",
]

# --------------------------------------------------
# MIDDLEWARE (WITH WHITENOISE)
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# URL / WSGI / ASGI
# --------------------------------------------------
ROOT_URLCONF = "punch_minichat.urls"

WSGI_APPLICATION = "punch_minichat.wsgi.application"
ASGI_APPLICATION = "punch_minichat.asgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "frontend" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------
# DATABASE (LOCAL SQLITE)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------
# AUTH
# --------------------------------------------------
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES (LOCAL)
# --------------------------------------------------
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "static",
]


STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------
# CHANNELS (LOCAL, NO REDIS)
# --------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# --------------------------------------------------
# DRF / JWT
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------
# EMAIL (LOCAL)
# --------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@punchchat.com"

# --------------------------------------------------
# DEFAULT PK
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
