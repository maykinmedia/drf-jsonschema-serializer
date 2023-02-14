from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent

USE_TZ = True

SECRET_KEY = "so-secret-i-cant-believe-you-are-looking-at-this"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "testapp",
]

MIDDLEWARE: List[str] = []

TEMPLATES: List[dict] = []

DEBUG_PROPAGATE_EXCEPTIONS = True
