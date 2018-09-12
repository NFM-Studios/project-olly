from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'H8+;[TG8G$8nxGT([mT:wJY%KF]J:ur#C^-?*+/zvF^Z4)/PA>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'binge.nfmstudios.com'

WSGI_APPLICATION = 'olly.binge_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'binge',
        'USER': 'binge',
        'PASSWORD': '9tAqopY6bVXnnoVnz7NCFojtQ3EIC2k5',
        'HOST': '10.136.73.223',
        'PORT': '',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = 'CSAMQ5GFQMTLT3FBSFWD'
AWS_SECRET_ACCESS_KEY = 'Rkls5L2UG9/T9MfDGok0H912JHRjFSo1EnBJR6jdkRE'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'binge'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'binge@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'U7THcY3Pam5vBaQWkNeasY6NYUCXgKTd'
FROM_EMAIL = "Bingeplay <noreply@bingeplay.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "omega.competitions@gmail.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lcj1GYUAAAAABo_n8XJrwvutsDRTHm6Iqv04rwK'
GOOGLE_RECAPTCHA_SITE_KEY = '6Lcj1GYUAAAAAKzN1gxoYx-_Q6h0zagkwr9wpc_S'

# Site info
SITE_NAME = "BingePlay"
SITE_SERVER = "Wheezy"
