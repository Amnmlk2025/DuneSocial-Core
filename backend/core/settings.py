SECRET_KEY = "dev-only"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'dt_growth',
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
]

ROOT_URLCONF = "core.urls"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

# speed up tests: disable migrations for dt_growth
MIGRATION_MODULES = {'dt_growth': None}
