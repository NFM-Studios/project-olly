from django.contrib import messages
from django.shortcuts import render, redirect
#from django.views.generic import View

#from matches.models import MatchReport, MatchDispute, Match, MapChoice, MapPoolChoice
from staff.forms import *


def create_league(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            form = CreateLeagueForm
            return render(request, 'staff/leagues/league_create.html', {'form': form})
        else:
            # the form is posting, lets start validating
            form = CreateLeagueForm(request.POSt, request.FILES)
            if form.is_valid():
                league = form.instance
                league.save()
                messages.success(request, 'Created League')
                #return redirect()

