from django.conf import settings
from pages.models import StaticInfo


def site_info(request):
    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_SERVER': settings.SITE_SERVER,
            'SITE_VERSION': settings.SITE_VERSION,
            'staticinfo': StaticInfo.objects.get(pk=1)}
