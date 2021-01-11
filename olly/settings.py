import os

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['secret_key']

if os.environ['debug'] == 'True' or 'TRAVIS' in os.environ:
    DEBUG = True
    PAYPAL_TEST = True
else:
    DEBUG = False
    PAYPAL_TEST = False

ALLOWED_HOSTS = os.environ['allowed_hosts']

SITE_URL = os.environ['site_url']

WSGI_APPLICATION = 'olly.wsgi.application'

try:
    if os.environ['user_verification'] == 'True':
        USER_VERIFICATION = True
    else:
        USER_VERIFICATION = False
except KeyError:
    USER_VERIFICATION = False

try:
    if os.environ['esports_mode'] == 'False':
        ESPORTS_MODE = False
    else:
        ESPORTS_MODE = True
except KeyError:
    ESPORTS_MODE = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ['db_type'] == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['db_name'],
            'USER': os.environ['db_username'],
            'PASSWORD': os.environ['db_password'],
            'HOST': os.environ['db_host'],
            'PORT': os.environ['db_port'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_DEFAULT_ACL = 'public-read'
AWS_ACCESS_KEY_ID = os.environ['storage_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['storage_secret_key']
AWS_S3_ENDPOINT_URL = os.environ['storage_endpoint_url']
AWS_STORAGE_BUCKET_NAME = os.environ['storage_bucket_name']
AWS_LOCATION = ''
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = os.environ['email_use_tls']
EMAIL_HOST = os.environ['email_host']
EMAIL_HOST_USER = os.environ['email_host_user']
EMAIL_HOST_PASSWORD = os.environ['email_host_password']
FROM_EMAIL = os.environ['from_email'].split('"')[1]
EMAIL_PORT = os.environ['email_port']

try:
    PAYPAL_EMAIL = os.environ['paypal_email'].split('"')[1]
except (KeyError, IndexError):
    PAYPAL_EMAIL = 'none@example.com'


# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ['google_recaptcha_secret_key']
GOOGLE_RECAPTCHA_SITE_KEY = os.environ['google_recaptcha_site_key']

# Site info
SITE_NAME = os.environ['site_name']
SITE_SERVER = os.environ['site_server']
