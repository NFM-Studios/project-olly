import os

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iKQusaQGM&WgdjNnzsCohupNhP3HKVTA&jkF#cmH8q^&whm%vD'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['debug'] == 'True':
    DEBUG = True
else:
    DEBUG = False

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'eot.nfmstudios.com'

WSGI_APPLICATION = 'olly.eot_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eot',
        'USER': 'eot',
        'PASSWORD': 'jU7Cky2%9hVXz4uKJeQc8%x4HD$Jd@ig',
        'HOST': '10.136.73.223',
        'PORT': '',
        'SSLMODE': 'require',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

# AWS_ACCESS_KEY_ID = 'ANARP7WZBRXNDXS6M6ES'
# AWS_SECRET_ACCESS_KEY = 'uy/4rMr2bPVqfKWm+3fSKZstNQqCWk3C1eAIW2b0WiM'
# AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
# AWS_STORAGE_BUCKET_NAME = 'duel'
# AWS_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

MEDIA_URL = '/media/'

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'eot@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'GHZ2uHeo2NgEvjgpIXnWN3biCC8XvgHT'
FROM_EMAIL = "eSports open tour <noreply@esportsopentour.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "steven.young.1-merchant@gmail.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lf37VYUAAAAAEgZAWo7p1DFVCtu-x567TrG3DT_'
GOOGLE_RECAPTCHA_SITE_KEY = '6Lf37VYUAAAAALOiWdAFVP0Wufd9rvY9E0r5hRnW'

# Site info
SITE_NAME = "EOT"
SITE_SERVER = "Wheezy"
