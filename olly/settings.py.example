import os

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = True

ALLOWED_HOSTS = ['*']

SITE_URL = '127.0.0.1'

WSGI_APPLICATION = 'olly.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_S3_ENDPOINT_URL = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
FROM_EMAIL = 'Testing <noreply@example.com>'
EMAIL_PORT = 587
PAYPAL_EMAIL = ''

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = ''
GOOGLE_RECAPTCHA_SITE_KEY = ''

# Site info
SITE_NAME = "Dev-Environment"
SITE_SERVER = "Dev-Environment"
