from django.shortcuts import render
from ipware import get_client_ip
from django.contrib import messages
from profiles.models import UserProfile, BannedUser


def ban_middleware(get_response):
    def middleware(request):
        ip = get_client_ip(request)
        ip = ip[0]

        if not (request.path_info == '/profile/banned/' and not request.path_info == '/admin'):
            if ip is not None:
                if not request.user.is_anonymous:
                    user = UserProfile.objects.get(user__username=request.user.username)
                    user.ip = ip  # change field
                    user.save()  # this will update only
                    if not BannedUser.objects.filter(ip=ip).exists():
                        if BannedUser.objects.filter(user=request.user):
                            return render(request, 'profiles/banned.html')
                if BannedUser.objects.filter(ip=ip).exists():
                    return render(request, 'profiles/banned.html')

        return get_response(request)

    return middleware


def check_2fa(get_response):
    def middleware(request):
        if request.user.is_verified():
            messages.success(request, "You enabled 2FA, congrats you're not an idiot")
        else:
            # user not logged in using two-factor
            messages.error(request, "2FA is not yet enabled on your account")

        return get_response(request)
    return middleware
