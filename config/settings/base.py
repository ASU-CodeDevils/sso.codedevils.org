"""
Base settings to build other settings files upon.
"""
import environ
from django.utils.translation import ugettext_lazy as _
from pathlib2 import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# cdsso/
APPS_DIR = ROOT_DIR / "cdsso"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en-us")

LANGUAGES = [
    ("es", _("Spanish")),
    ("en-us", _("English")),
    ("fr", _("French")),
    ("ar", _("Arabic")),
    ("nl", _("Dutch")),
    ("ge", _("German")),
    ("ja", _("Japanese")),
    ("hi", _("Hindi")),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL", default="mysql:///codedevils_weblogin")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.keycloak",
    "cas_server",
    "django_celery_beat",
    "drf_yasg",
    "graphene_django",
    "rest_framework",
    "rest_framework.authtoken",
    "rosetta",
]

LOCAL_APPS = [
    "cdsso.users.apps.UsersConfig",
    "cdsso.contrib.countries.apps.CountriesConfig",
    "cdsso.contrib.register.apps.RegisterConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "cdsso.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = env("CDSSO_LOGIN_REDIRECT_URL", default="register:status")
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "cas_server:login"
# https://docs.djangoproject.com/en/3.0/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = LOGIN_URL

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cdsso.contrib.register.middleware.UserRegistrationConfirmationMiddleware",
    "config.middleware.LanguageIdenitifcationMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "public/static/")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR / "public/media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "cdsso.utils.context_processors.settings_context",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_PORT = 25
EMAIL_TIMEOUT = 5
EMAIL_USE_TLS = True
EMAIL_HOST = env("EMAIL_HOST", default="smtp.dreamhost.com")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="donotreply@codedevils.org")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Kevin Shelley""", "krshelle@asu.edu"),
    ("""David Welbourne""", "dswelbor@asu.edu"),
    ("""Jacob Labrec""", "jlabrec@asu.edu")
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "cdsso.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "cdsso.users.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html#account-forms
ACCOUNT_FORMS = {"signup": "cdsso.contrib.register.forms.StudentRegistrationForm"}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# django-cas-server
# https://pypi.org/project/django-cas-server/#id6
# -------------------------------------------------------------------------------
# CAS_FEDERATE = True  # https://pypi.org/project/django-cas-server/#federation-mode
CAS_LOGO_URL = False
CAS_FAVICON_URL = False
CAS_SHOW_POWERED = False
CAS_SHOW_SERVICE_MESSAGES = False
CAS_LOGIN_TEMPLATE = "cas/login.html"
CAS_WARN_TEMPLATE = "cas/warn.html"
CAS_LOGOUT_TEMPLATE = "cas/logout.html"
CAS_LOGGED_TEMPLATE = "cas/logged.html"

# drf-yasg
# https://drf-yasg.readthedocs.io/en/stable/readme.html#usage
# -------------------------------------------------------------------------------
DRF_YASG_TITLE = "CodeDevils SSO API"
DRF_YASG_LOGO = STATIC_URL + "img/logo-light.png"
DRF_YASG_DEFAULT_VERSION = "v1"
DRF_YASG_DESCRIPTION = "CodeDevils identity and user management sytem"
DRF_YASG_TERMS_OF_SERVICE = "https://www.asu.edu/aad/manuals/acd/acd125.html"
DRF_YASG_CONTACT_EMAIL = "webmaster@codedevils.org"
DRF_YASG_LICENSE = "BSD License"
# https://drf-yasg.readthedocs.io/en/stable/security.html#describing-authentication-schemes
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

# graphene
# https://docs.graphene-python.org/projects/django/en/latest/
# -------------------------------------------------------------------------------
GRAPHENE = {"SCHEMA": "config.graphene.schema.schema"}

# CD SSO-specific settings
# -------------------------------------------------------------------------------

# CD website
CODEDEVILS_WEBSITE = {
    "BASE_URL": env("CODEDEVILS_WEBSITE_BASE_URL", default="https://codedevils.org"),
    "API_KEY": env("CODEDEVILS_WEBSITE_API_KEY"),
    "GRAPHQL_API": env("CODEDEVILS_WEBSITE_GRAPHQL_API", default="/api/graphql/"),
    "REST_API": env("CODEDEVILS_WEBSITE_REST_API", default="/api/"),
    "UPDATE_FIELDS": env.list(
        "CODEDEVILS_WEBSITE_UPDATE_FIELDS", default=["email", "name", "anonymous", "slack_id", "image_24", "image_512"]
    ),
    "SKIP_FIELDS": env.list("CODEDEVILS_WEBSITE_SKIP_FIELDS", default="last_login"),
}

# Flameboi Slack
FLAMEBOI = {
    "API_URL": env("FLAMEBOI_API_URL", default="https://flameboi.codedevils.org/"),
    "USERNAME": env("FLAMEBOI_API_USERNAME"),
    "PASSWORD": env("FLAMEBOI_API_PASSWORD"),
    "REGISTER_SLACK_USERS_WITH_FLAMEBOI": env.bool(
        "FLAMEBOI_REGISTER_SLACK_USERS_WITH_FLAMEBOI", default=True
    ),
}
REGISTRATION_PAGINATION = env.int("CDSSO_REGISTRATION_PAGINATION", default=100)
NOTIFY_MANAGERS_SDS_REGISTRATION = env.bool(
    "CDSSO_NOTIFY_MANAGERS_SDS_REGISTRATION", default=True
)
SEND_COMPLETED_REGISTRATION_NOTIFICATION = env.bool(
    "CDSSO_SEND_COMPLETED_REGISTRATION_NOTIFICATION", default=True
)
RUN_REGISTRATION_POST_SAVE_SIGNAL = env.bool(
    "CDSSO_RUN_REGISTRATION_POST_SAVE_SIGNAL", default=True
)
