from django.conf import settings

OLLY_VERSION = getattr(settings, 'PAGES_OLLY_VERSION', (
    '18.04.1'
))

SERVER_CHOICE = getattr(settings, 'PAGES_SERVER_CHOICE', (
    'Wheezy'
))