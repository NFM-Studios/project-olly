from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'GUxk&cxi2gvh8h&kqpz&X4RcX!ZiIzioS2BIg@Eawp3b&*rfxm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['debug']

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'roc.nfmstudios.com'

WSGI_APPLICATION = 'olly.roc_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roc',
        'USER': 'roc',
        'PASSWORD': 'ZRtHZ7mqz&V$#qqJS&7vm*7fc2Z6B98g',
        'HOST': '10.136.73.223',
        'PORT': '',
        'SSLMODE': 'require',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = 'RBKENOP7DWP4OK3NUZGO'
AWS_SECRET_ACCESS_KEY = 'oxB8YeZm0ywPm+RvqIUHLgAF658Fzkk4aVFXUuXKdAI'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'roc'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'roc@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'vrtCAUq4bLNhtGAJ2DhFTeigAAN5AGgd'
EMAIL_PORT = 587
FROM_EMAIL = "ROC eSports League <noreply@rocesportsleague.com>"
PAYPAL_EMAIL = "steven.young.1-merchant@gmail.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6LcbdWwUAAAAAO9elu8TeJ3WDeDZsOPpoXwW5xXD'
GOOGLE_RECAPTCHA_SITE_KEY = '6LcbdWwUAAAAAG7fJWJNsbqRqfSJSxqKklsnZAim'

# Site info
SITE_NAME = "RightOfChange"
SITE_SERVER = "Wheezy"
