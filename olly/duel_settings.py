from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bcgu@a)k$z!)1qmv@5a)&e$x@+@_tvl-s87)3@n)032*6r6u-2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = True

ALLOWED_HOSTS = ['duel.nfmstudios.com','duelbattleroyale.com', 'Dueltournaments.com', 'Dueltournament.com', 'Duelchallenge.us', '127.0.0.1']

SITE_URL = '127.0.0.1'

WSGI_APPLICATION = 'olly.duel_wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'duel',
        'USER': 'duel',
        'PASSWORD': '9tAqopY6bVXnnoVnz7NCFojtQ3EIC2k5',
        'HOST': '10.136.73.223',
        'PORT': '',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = 'ANARP7WZBRXNDXS6M6ES'
AWS_SECRET_ACCESS_KEY = 'uy/4rMr2bPVqfKWm+3fSKZstNQqCWk3C1eAIW2b0WiM'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'duel'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'duel@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'PBmks2LpvRbWrr5oPPtGpNyJmScJfDjf'
FROM_EMAIL = "Duel Challenge <noreply@dueltournaments.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "omega.competitions@gmail.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lcj1GYUAAAAABo_n8XJrwvutsDRTHm6Iqv04rwK'
GOOGLE_RECAPTCHA_SITE_KEY = '6Lcj1GYUAAAAAKzN1gxoYx-_Q6h0zagkwr9wpc_S'

# Site info
SITE_NAME = "DuelChallenge"
SITE_SERVER = "Wheezy"
