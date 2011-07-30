
TIME_ZONE = "Australia/Melbourne"
TEMPLATE_DEBUG = True
DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SITE_ID = 1
USE_I18N = False
SECRET_KEY = "SRGF45gR45wtg$%G$RGt4tFTG%t6rsfbvsfdvBSR"
INTERNAL_IPS = ("127.0.0.1", "60.241.76.198")

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

DATABASES = {
    "default": {
        "ENGINE": "sqlite3",
        "NAME": "drawnby.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
full_path = lambda *parts: os.path.join(PROJECT_ROOT, *parts)

PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
ADMIN_MEDIA_PREFIX = "/media/"
MEDIA_URL = "/static/"
MEDIA_ROOT = full_path(MEDIA_URL.strip("/"))
ROOT_URLCONF = "urls"
TEMPLATE_DIRS = full_path("templates")

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_extensions",
    "social_auth",
    "easy_thumbnails",
    "south",
    "pagination",
    "compressor",
    "core",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
)

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY     = ""
TWITTER_CONSUMER_SECRET  = ""
FACEBOOK_APP_ID          = ""
FACEBOOK_API_SECRET      = ""
FACEBOOK_EXTENDED_PERMISSIONS = ["email", "offline_access", "publish_stream"]

LOGIN_URL          = '/auth/'
LOGIN_REDIRECT_URL = '/auth/loggedin/'
LOGIN_ERROR_URL    = '/auth/error/'

COMPRESS = True
COMPRESS_OUTPUT_DIR = "cache"

try:
    from local_settings import *
except ImportError:
    pass
