from django.conf import settings
from pages import models as pagesmodels


def site_info(request):
    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_SERVER': settings.SITE_SERVER,
            'SITE_VERSION': settings.SITE_VERSION,
            'SocialInfo': pagesmodels.SocialInfo}
