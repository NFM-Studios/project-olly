"""
Django settings for olly project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bcgu@a)k$z!)1qmv@5a)&e$x@+@_tvl-s87)3@n)032*6r6u-2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#SECURITY WARNING: don't run with this set to true in prod
PAYPAL_TEST = True

ALLOWED_HOSTS = ['127.0.0.1', 'ban-mikemaddem.c9users.io', 'olly-techlover1.c9users.io']

SESSION_COOKIE_AGE = 604800

SITE_URL = '127.0.0.1'

# Application definition

INSTALLED_APPS = [

    #all stock stuff
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # modified user model, etc.
    'profiles',

    # just regular pages
    'pages',

    # mikes awesome support tickets
    'support',

    # news app
    'news',

    #store app
    'store',

    # staff admin panel
    'staff',

    # teams
    'teams',
    
    # tag manager package
    'taggit',

    # ip package
    'ipware',

    #paypal IPN
    'paypal.standard.ipn',

    # the country field
    'django_countries',

    # matches for all uses
    'matches',

    # single elimination tournaments
    'singletournaments',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'olly.middleware.CheckBanListMiddleware'

]


ROOT_URLCONF = 'olly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'olly.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'olly/media')

# Where to redirect users after login
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Email stuff
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nfm.studios@gmail.com'
EMAIL_HOST_PASSWORD = 'mikemaddem'
EMAIL_PORT = 587
PAYPAL_EMAIL = "steven.young.1-merchant@gmail.com"


GOOGLE_RECAPTCHA_SECRET_KEY = '6LdEsEMUAAAAABfKHZo9Ox0j55s2EnANq-wQlUOm'
