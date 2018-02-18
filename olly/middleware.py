from django.shortcuts import render
from ipware import get_client_ip
from profiles.models import UserProfile, BannedUser

class CheckBanListMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        #ip = get_real_ip(request)
        ip = get_client_ip(request)
        ip = ip[0]
        #print(ip)

        if not (request.path_info == '/profile/banned/'):
            if ip is not None:
                if not request.user.is_anonymous:
                    user = UserProfile.objects.get(user__username=request.user.username)
                    user.ip = ip  # change field
                    user.save() # this will update only
                    if not BannedUser.objects.filter(ip=ip).exists():
                        if BannedUser.objects.filter(user=request.user):
                            return render(request, 'profiles/banned.html')
                if BannedUser.objects.filter(ip=ip).exists():
                    return render(request, 'profiles/banned.html')
            