# stolen from django-rest-framework conftest.py
# needed to convince django to do models.
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DEBUG_PROPAGATE_EXCEPTIONS = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SITE_ID = 1
SECRET_KEY = 'not very secret in tests'
USE_I18N = True
USE_L10N = True
STATIC_URL = '/static/'
ROOT_URLCONF = 'drf_jsonschema.tests.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
MIDDLEWARE = MIDDLEWARE
MIDDLEWARE_CLASSES = MIDDLEWARE
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_jsonschema.tests',
)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
