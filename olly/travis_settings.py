import os

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CI_BUILD'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = True

ALLOWED_HOSTS = ['*']

SITE_URL = '127.0.0.1'

WSGI_APPLICATION = 'olly.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test-db.sqlite3'),
        }
    }

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

# Site info
SITE_NAME = "Dev-Environment"
SITE_SERVER = "Dev-Environment"
