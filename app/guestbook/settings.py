import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env(name, default=""):
    return os.environ.get(name, default)


def env_flag(name):
    return env(name, "0").strip().lower() in {"1", "true", "yes", "on"}


DEBUG = env_flag("GUESTBOOK_DEBUG")

SECRET_KEY = env("GUESTBOOK_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "Set GUESTBOOK_SECRET_KEY, or GUESTBOOK_DEBUG=1 for local development."
        )
    SECRET_KEY = "local-development-only"

ALLOWED_HOSTS = [
    host
    for host in env("GUESTBOOK_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host
]

PROJECT_APPS = [
    "accounts",
    "testimonies",
    "moderation",
    "reports",
    "publication",
    "exports",
]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *PROJECT_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "guestbook.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "guestbook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("GUESTBOOK_DB_NAME", "guestbook"),
        "USER": env("GUESTBOOK_DB_USER", "guestbook_admin"),
        "PASSWORD": env("GUESTBOOK_DB_PASSWORD"),
        "HOST": env("GUESTBOOK_DB_HOST", "127.0.0.1"),
        "PORT": env("GUESTBOOK_DB_PORT", "5432"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

SESSION_COOKIE_AGE = 30 * 24 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

EMAIL_BACKEND = env(
    "GUESTBOOK_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = env("GUESTBOOK_FROM_EMAIL", "contact@theaiguestbook.org")

PUBLIC_BASE_URL = env("GUESTBOOK_PUBLIC_BASE_URL", "https://theaiguestbook.org")

# Until moderation has its own role model, the custodian is the moderator:
# accounts signing in with one of these addresses see the moderation queue.
MODERATOR_EMAILS = {
    address.strip().lower()
    for address in env("GUESTBOOK_MODERATOR_EMAILS").split(",")
    if address.strip()
}
