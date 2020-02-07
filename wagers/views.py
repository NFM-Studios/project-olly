from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, View
from profiles.models import UserProfile
from datetime import datetime, timedelta
from .forms import WagerRequestForm, WagerChallengeForm
from .models import *
from matches.models import Match
from teams.models import Team
from django.db.models import Q
from django.utils import timezone
#import pytz


class WagerRequestList(ListView):
    model = WagerRequest

    def get(self, request):
        # current = pytz.UTC
        # current = datetime.utcnow()
        current = timezone.now()
        wager_list = WagerRequest.objects.filter(challenge_accepted=False, expired=False)
        for x in wager_list:
            if x.expiration < current:
                # it is expired set it to expired
                x.expired = True
                x.save()
        final = wager_list.filter(expired=False)
        return render(request, 'wagers/' + request.tenant + '/wager_request_list.html', {'wager_list': final})

    def get_queryset(self):
        return WagerRequest.objects.filter(challenge_accepted=False, expired=False)


class WagerRequestDetail(DetailView):
    model = WagerChallenge

    def get(self, request, **kwargs):
        template = 'wagers/' + request.tenant + '/wager_request_detail.html'
        user = request.user
        pk = self.kwargs['pk']
        wrequest = get_object_or_404(WagerRequest, pk=pk)
        if wrequest.wmatch:
            return render(request, template, {'wrequest': wrequest, 'wmatch': wrequest.wmatch})
        return render(request, template, {'wrequest': wrequest})


def delete_wager_request(request, pk):
    userprofile = UserProfile.objects.get(user=request.user)
    wager = WagerRequest.objects.get(pk=pk)
    teams = Team.objects.filter(Q(founder=request.user))
    yes = False
    for team in teams:
        if team == wager.team:
            # check to see there
            yes = True
    if not yes:
        messages.error(request,
                       'Error, we could not cancel the wager request. Only the founder of the team can cancel the Wager Request')
        return redirect('wagers:request_detail', pk=pk)
    if wager.challenge_accepted or wager.wmatch:
        messages.error(request,
                       'We cannot cancel your wager request because it has already been accepted, please contact support for more assistance.')
        return redirect('wagers:request_detail', pk=pk)
    wager.delete()
    messages.success(request, 'Your wager request has been removed.')
    return redirect('wagers:list')


class WagerRequestCreateView(View):
    # model = WagerRequest
    form_class = WagerRequestForm

    def get(self, request):
        template = 'wagers/' + request.tenant + '/wager_request_create.html'
        form = self.form_class(user=request.user)
        return render(request, template, {'form': form})

    def post(self, request):
        # self.user = request.user
        form = self.form_class(request.POST, user=request.user)
        # form.user = request.user
        if form.is_valid():
            myrequest = form.instance
            userprofile = UserProfile.objects.get(user=request.user)
            if form.cleaned_data['credits'] > userprofile.credits:
                messages.error(self.request, "You do not have enough credits in your account")
                return redirect('wagers:list')
            if form.cleaned_data['credits'] == 0:
                messages.error(self.request, "You cannot wager 0 credits")
                return redirect('wagers:list')
            if form.cleaned_data['teamformat'] == 0:
                min = 1
            if form.cleaned_data['teamformat'] == 1:
                min = 2
            if form.cleaned_data['teamformat'] == 2:
                min = 3
            if form.cleaned_data['teamformat'] == 3:
                min = 4
            if form.cleaned_data['teamformat'] == 4:
                min = 5
            if form.cleaned_data['teamformat'] == 5:
                min = 6

            if form.cleaned_data['team'].get_players_count() < min:
                messages.error(self.request,
                               "Error. Your team does not have enough players on it to play in this specific format.")
                return redirect('wagers:list')
            # myrequest.creator = request.user
            """myrequest.credits = form.cleaned_data['credits']
            myrequest.game = form.cleaned_data['game']
            myrequest.platform = form.cleaned_data['platform']
            myrequest.bestof = form.cleaned_data['bestof']
            myrequest.teamformat = form.cleaned_data['teamformat']
            myrequest.info = form.cleaned_data['info']
            myrequest.team = form.cleaned_data['team']"""
            myrequest.creator = self.request.user
            myrequest.expiration = datetime.utcnow() + timedelta(minutes=30)
            myrequest.save()
            messages.success(self.request, "Your Wager Request has been created!")
            return redirect('wagers:list')
        messages.error(self.request, "Something went wrong (this shouldn't be seen)")
        return redirect('wagers:request_create')


class WagerChallengeCreate(View):
    # model = WagerChallenge

    def get(self, request, pk):
        # self.user = request.user
        template = 'wagers/' + request.tenant + '/wager_challenge_create.html'
        form = WagerChallengeForm(user=request.user)
        myrequest = WagerRequest.objects.get(pk=pk)
        return render(request, template, {'form': form, 'myrequest': myrequest})

    def post(self, request, pk):
        form = WagerChallengeForm(request.POST, user=request.user)
        myrequest = WagerRequest.objects.get(pk=pk)
        challenge = form.instance
        challenge.creator = self.request.user
        if form.is_valid():
            challenger = UserProfile.objects.get(user__username=challenge.creator)
            if challenger.credits < myrequest.credits:
                messages.error(self.request, "You do not have enough credits in your account to challenge this team")
                return redirect('wagers:list')
            if challenge.team == myrequest.team:
                messages.error(self.request, "A team cannot challenge it's own wager")
                return redirect('wagers:list')
            for y in challenge.team.players.all():
                for x in myrequest.team.players.all():
                    if x == y:
                        messages.error(self.request, "A player cannot be on both teams at the same time")
                        return redirect('wagers:list')
            challenge.save()
            myrequest.challenge_accepted = True
            myrequest.challenge = challenge
            myrequest.save()
            match = Match(type='w', game=myrequest.game, platform=myrequest.platform, hometeam=myrequest.team,
                          awayteam=challenge.team,
                          bestof=myrequest.bestof, teamformat=myrequest.teamformat,
                          info="Home Team: " + myrequest.info + "\n" + "Away Team: " + challenge.info)
            match.save()
            wmatch = WagerMatch(match=match, credits=myrequest.credits)
            wmatch.save()
            myrequest.wmatch = wmatch
            myrequest.save()
            challenger.credits = challenger.credits - myrequest.credits
            challenge.save()
            myrequest.creator.credits = myrequest.creator.credits - myrequest.credits
            myrequest.save()
            messages.success(request,
                             "Wager Challenge Created! You have 30 minutes to play your match and report the scores")
            return redirect('wagers:match_detail', pk=wmatch.pk)

        messages.error(self.request, "Something went wrong (this shouldn't be seen")
        return redirect('wagers:request_detail', pk=pk)


class WagerMatchDetail(View):

    def get(self, request, pk):
        template = 'wagers/' + request.tenant + '/wager_match_detail.html'
        wmatch = get_object_or_404(WagerMatch, pk=pk)
        match = wmatch.match
        team1 = Team.objects.get(id=match.hometeam_id)
        team2 = Team.objects.get(id=match.awayteam_id)
        aplayers = team2.players.all()
        hplayers = team1.players.all()
        return render(request, template, {'match': match, 'wmatch': wmatch, 'aplayers': aplayers, 'hplayers': hplayers})


class MyWagersList(ListView):

    def get(self, request):
        # current = pytz.UTC
        # current = datetime.utcnow()
        user = self.request.user
        teams = Team.objects.filter(Q(captain__username__contains=user) | Q(founder=user))
        old_requests = WagerRequest.objects.filter(Q(expired=True) | Q(challenge_accepted=True))
        for x in old_requests:
            for y in teams:
                if x.team == y:
                    old_results = old_requests + x

        old_matches = WagerMatch.objects.filter()
        return render(request, 'wagers/' + request.tenant + '/wager_request_list.html', {'wager_list': final})

    def get_queryset(self):
        return WagerRequest.objects.filter(challenge_accepted=False, expired=False)
