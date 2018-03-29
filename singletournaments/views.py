from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SingleEliminationTournamentJoin
from .models import SingleTournamentRound, SingleEliminationTournament
from teams.models import TeamInvite
from django.contrib import messages


class List(View):
    template_name = 'singletournaments/singletournament_list.html'

    def get(self, request):
        return render(request, self.template_name)


class SingleTournamentJoin(View):
    template_name = 'singletournaments/singletournament_join.html'
    form_class = SingleEliminationTournamentJoin

    def get(self, request):
        teams = TeamInvite.objects.filter(user_id=request.user.id, captain__in=['founder', 'captain'])
        if teams.exists():
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, message="You aren't a captain or founder of any teams!")
            return redirect('singletournaments:list')

    def post(self, request):
        form = self.form_class(request.POST)
        try:
            invite = TeamInvite.objects.get(user=request.user, team=form.data['teams'])
        except:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:list')
        if invite.captain == 'captain' or invite.captain == 'founder':
            tournament = SingleEliminationTournament.objects.get(name=form.data['tournaments'])
            team = form.data['teams']
            try:
                tournament.teams.add(team)
            except:
                messages.error(request, message="This team is already in this tournament")
                return redirect('singletournaments:list')
            tournament.save()
            messages.success(request, message="Joined tournament")
            return redirect('singletournaments:list')
        else:
            messages.error(request, message="You can't join a tournament if you aren't the captain or founder")
            return redirect('singletournaments:list')


class SingleTournamentDetail(View):
    template_name = 'singletournaments/singletournament_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        return render(request, self.template_name, {'x': pk, 'tournament': tournament})


class SingleTournamentTeamsList(View):
    template_name = 'singletournaments/singletournament_teams.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams
        return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'teams': teams})


class SingleTournamentRules(View):
    template_name = 'singletournaments/singletournament_rules.html'


class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        if tournament.size == 4:
            # get 2 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket4.html'


            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.ojbects.get(tournament=tournament, roundnum=2)
            return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2})

        elif tournament.size == 8:
            # get 3 rounds to pass to the view

            round1 = SingleTournamentRound.objects.get
            template_name = 'singletournaments/singletournament_bracket8.html'
        elif tournament.size == 16:
            # get 4 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket16.html'
        elif tournament.size == 32:
            # get 5 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket32.html'
        elif tournament.size == 64:
            # get 6 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket64.html'
        elif tournament.size == 128:
            # get 7 rounds to pass to the  view
            template_name = 'singletournaments/singletournament_bracket128.html'
        return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'round1': round1, 'round2': round2})
