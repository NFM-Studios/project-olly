from django.shortcuts import render
from ipware import get_client_ip
from profiles.models import UserProfile, BannedUser


class CheckBanListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
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
                            return render(request, 'profiles/' + request.tenant + '/banned.html')
                if BannedUser.objects.filter(ip=ip).exists():
                    return render(request, 'profiles/' + request.tenant + '/banned.html')


def tenant_middleware(get_response):
    def middleware(request):

        host = request.get_host()
        # the following line is probably not needed
        # host = host.split(':')[1]  # we remove the protocol part: 'ibm.spinnertracking.com'
        subdomain = host.split('.')[0]
        domain = host.split('.')[-2]

        if domain == 'duelbattleroyale' or subdomain == 'duel':
            request.tenant = 'duel'
            request.package = 'bobcat'

        elif domain == 'rocesportsleague' or subdomain == 'roc':
            request.tenant = 'roc'
            request.package = 'bobcat'

        elif domain == 'bingeplay' or subdomain == 'binge':
            request.tenant = 'binge'
            request.package = 'bobcat'

        elif domain == 'esportsopentour' or subdomain == 'eot':
            request.tenant = 'eot'
            request.package = 'bobcat'

        elif domain == 'playot' or subdomain == 'online':
            request.tenant = 'ot'
            request.package = 'bobcat'
        
        elif domain == 'worldleagueofgaming' or subdomain == 'wlg':
            request.tenant = 'wlg'
            request.package = 'bobcat'

        elif domain == 'cashoutgaming' or subdomain == 'cashout':
            request.tenant = 'cashout'
            request.package = 'bobcat'
            
        else:
            request.tenant = 'stock'
            request.package = 'leopard'

        # all done, the view will receive a request with a tenant attribute
        return get_response(request)

    return middleware
