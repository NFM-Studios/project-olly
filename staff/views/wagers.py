from staff.auth import staff_required
from django.http import HttpResponseNotAllowed

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from staff.forms import *
from wagers.models import *


@staff_required
def wagers_list(request):
    active = WagerRequest.objects.filter(Q(expired=False))
    active = active.filter(Q(challenge_accepted=False))
    active = active.filter(Q(wmatch__isnull=True))
    return render(request, 'staff/wagers/wagers.html', {'wagers': active})


@staff_required
def wagers_request_detail(request, pk):
    wrequest = get_object_or_404(WagerRequest, pk=pk)
    return render(request, 'staff/wagers/wager_request_detail.html', {'wrequest': wrequest})


@staff_required
def delete_wager_request(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    # wrequest = get_object_or_404(WagerRequest, pk=pk)
    wrequest = WagerRequest.objects.get(id=pk)
    # if not wrequest:
    # lets try to delete it now
    wrequest.delete()
    # wrequest.save()
    messages.success(request, 'Succuessfully deleted Wager Request')
    return redirect('staff:wagers_list')
