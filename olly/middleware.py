from django.shortcuts import render
from ipware import get_client_ip

from profiles.models import BannedUser

BANNED_PAGE = '/profile/banned/'
EXEMPT_PREFIXES = ('/admin/', '/healthz/', '/readyz/')


def ban_middleware(get_response):
    def middleware(request):
        path = request.path_info
        if path == BANNED_PAGE or path.startswith(EXEMPT_PREFIXES):
            return get_response(request)

        ip = get_client_ip(request)[0]

        if ip is not None and BannedUser.objects.filter(ip=ip).exists():
            return render(request, 'profiles/banned.html', status=403)

        if not request.user.is_anonymous:
            if BannedUser.objects.filter(user=request.user).exists():
                return render(request, 'profiles/banned.html', status=403)
            profile = request.user.user
            if ip is not None and profile.ip != ip:
                profile.ip = ip
                profile.save(update_fields=['ip'])

        return get_response(request)

    return middleware
