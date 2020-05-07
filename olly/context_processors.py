from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from pages import models as pagesmodels

try:
    SocialInfo = pagesmodels.SocialInfo.objects.get(pk=1)
except ObjectDoesNotExist:
    SocialInfo = None


def site_info(request):
    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_SERVER': settings.SITE_SERVER,
            'SITE_VERSION': settings.SITE_VERSION,
            'SocialInfo': SocialInfo,
            'ESPORTS_MODE': settings.ESPORTS_MODE}
