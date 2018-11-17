from . base_settings import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mag2$s![w,bVphL(L@)b#GTzBB9QeG"_h[4<{ww6<af5/?/&m9'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['debug'] == 'True':
        DEBUG = True
else:
        DEBUG = False

# SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'online.nfmstudios.com'

WSGI_APPLICATION = 'olly.online_wsgi:application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'online',
        'USER': 'online',
        'PASSWORD': 'ytS8kpLf72nVK7vVC9LeBJu4bUggwzqb',
        'HOST': '10.136.73.223',
        'PORT': '',
        'SSLMODE': 'require',
    }
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

AWS_ACCESS_KEY_ID = '34CZJFTNT63XU4KYIHGL'
AWS_SECRET_ACCESS_KEY = 'XzHFfqKWV4on2lfvMAlS7wK5Cg+sFDhaJOarMx74a/c'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'onlinetournament'
AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'online@mg.nfmstudios.com'
EMAIL_HOST_PASSWORD = 'W4kw86E9D9LunBcSaZSycgVpvHLPyAgf'
FROM_EMAIL = "Online Tournament <noreply@playot.se>"
EMAIL_PORT = 587
PAYPAL_EMAIL = "pay@playot.se"

# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = '6LeDXnEUAAAAAMzomeFz_-ZOn3vJW3Dm9FIsoYUt'
GOOGLE_RECAPTCHA_SITE_KEY = '6LeDXnEUAAAAAGLrAxK8JSt7IRRliula5alcn9Ou'

# Site info
SITE_NAME = "OnlineTournament"
SITE_SERVER = "Wheezy"
