import os

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'LoNIhExSASJr48ynsgCQfncKIHN7ZbZPmVD5By47zXGNBC%Nb&'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['debug'] == 'True':
        DEBUG = True
else:
        DEBUG = False

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'ga.nfmstudios.com'

WSGI_APPLICATION = 'olly.ga_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ga',
        'USER': 'ga',
        'PASSWORD': '87o5SFCRmRQikVPKcgV68HisYKyWAgWf',
        'HOST': '10.136.73.223',
        'PORT': '',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = 'SC2FWHC3CPU7K65GIZM5'
AWS_SECRET_ACCESS_KEY = 'wZEEbqbTHkArvqMPA9pMDGwnFQDJsH3z0Ww5ebgV9aM'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'ga'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'ga@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'T3tRxMLRD9BWh3pD56gcm2eBAPdEAhhT'
FROM_EMAIL = "Gamers Asylum <noreply@gaesportscenter.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = ""

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Ld6NokUAAAAAGmOedlMmeW9Gd_XOztzwYiZ-6kP'
GOOGLE_RECAPTCHA_SITE_KEY = '6Ld6NokUAAAAALX9DEvds6TDLFoE8hAghuR1_8Ya'

# Site info
SITE_NAME = "GamersAsylum"
SITE_SERVER = "Wheezy"
