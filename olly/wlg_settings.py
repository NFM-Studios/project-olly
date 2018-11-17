from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8k%8LQ2KBtbjVQfzDC7mN6mQUKJws9$reLCvGQxRK7Exr5pAik'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['debug'] == 'True':
        DEBUG = True
else:
        DEBUG = False

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['wlg.nfmstudios.com', 'worldleagueofgaming.com', 'wlg.lan']

SITE_URL = 'wlg.nfmstudios.com'

WSGI_APPLICATION = 'olly.wlg_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wlg',
        'USER': 'wlg',
        'PASSWORD': '*9kWWhU5N@AgkcSUm4@A%!^YUk9fQR%o',
        'HOST': '10.136.73.223',
        'PORT': '',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AAWS_ACCESS_KEY_ID = 'W74O67XJ3SJUTMCJNSBE'
AWS_SECRET_ACCESS_KEY = 'mjNILBlckmn9cJT+11S+DofDIcZtDUxNPLoQQBtwdJk'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'wlg'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'wlg@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'qBWbPcsf38VLGAW7CbHtPxgm7SrIcKBn'
FROM_EMAIL = "World League of Gaming <noreply@worldleagueofgaming.com>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "loubravo@worldleaguegaming.com"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lf9OFYUAAAAAF-24jSe5cxH8JPr_DCBMWhQJQuC'
GOOGLE_RECAPTCHA_SITE_KEY = '6Lf9OFYUAAAAAJ-CIbE26ciHRwYIaPoVOkiB3pHj'

# Site info
SITE_NAME = "WorldLeagueOfGaming"
SITE_SERVER = "Wheezy"
