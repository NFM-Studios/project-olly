from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bcgu@a)k$z!)1qmv@5a)&e$x@+@_tvl-s87)3@n)032*6r6u-2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = True

ALLOWED_HOSTS = ['*']

SITE_URL = '127.0.0.1'

WSGI_APPLICATION = 'olly.duel_wsgi.application'

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

AWS_ACCESS_KEY_ID = 'SFEXIZLBH3QT2TTAMVUG'
AWS_SECRET_ACCESS_KEY = 'LBPpYOTa22L8e62+yOrh/krtMMplsKlOoZbTFklZLvc'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'olly-dev-space'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nfm.studios@gmail.com'
EMAIL_HOST_PASSWORD = 'mikemaddem'
FROM_EMAIL = "NFM Testing <noreply@nfmstudios.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "steven.young.1-merchant@gmail.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6LdEsEMUAAAAABfKHZo9Ox0j55s2EnANq-wQlUOm'
GOOGLE_RECAPTCHA_SITE_KEY = '6LcSkGkUAAAAAPUR-nM9Fh_L4b3cYm75_Hwp6mRd'

# Site info
SITE_NAME = "Dev-Environment"
SITE_SERVER = "Dev-Environment"
