from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from staff.forms import *
from wagers.models import *


def wagers_list(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        active = WagerRequest.objects.filter(Q(expired=False))
        active = active.filter(Q(challenge_accepted=False))
        active = active.filter(Q(wmatch__isnull=True))
        return render(request, 'staff/wagers/wagers.html', {'wagers': active})


def wagers_request_detail(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        wrequest = get_object_or_404(WagerRequest, pk=pk)
        return render(request, 'staff/wagers/wager_request_detail.html', {'wrequest': wrequest})


def delete_wager_request(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        # wrequest = get_object_or_404(WagerRequest, pk=pk)
        wrequest = WagerRequest.objects.get(id=pk)
        # if not wrequest:
        # lets try to delete it now
        wrequest.delete()
        # wrequest.save()
        messages.success(request, 'Succuessfully deleted Wager Request')
        return redirect('staff:wagers_list')
