from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0m2s@E*l3U6BY1eBmiZ@0hReQI5Ld$Re5xe$PlAxxNFcM8s29z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['debug']

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'cashout.nfmstudios.com'

WSGI_APPLICATION = 'olly.cashout_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cashout',
        'USER': 'cashout',
        'PASSWORD': 'mIqOCA1IzotBBxxwEAAD0rnjnxny7n6m',
        'HOST': '10.136.73.223',
        'PORT': '',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = 'KUFQHBOF22M2QMJSTYNR'
AWS_SECRET_ACCESS_KEY = '7Bv6HMTi787mHoQL9EyGm3hzY7OAcx7Shzco0REJpFs'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'cashout'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'cashout@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = '7S1ln6HYKQDmCHweKy1XHbjyHCIYk7Vj'
FROM_EMAIL = "Cashout <noreply@cashoutgaming.net.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = ""

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Ld1nXoUAAAAAM4pi7LdpIncBDGdzfZf2cA5OvdQ'
GOOGLE_RECAPTCHA_SITE_KEY = '6Ld1nXoUAAAAAI9LdR0ZZkp-6vORurjP-vUcydsL'

# Site info
SITE_NAME = "Cashout"
SITE_SERVER = "Wheezy"
