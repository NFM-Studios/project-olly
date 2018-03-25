from django.shortcuts import render
from django.views.generic import View
from .forms import SingleEliminationTournamentJoin
from .models import SingleTournamentRound, SingleEliminationTournament, SingleTournamentTeam


class List(View):
    template_name = 'singletournaments/singletournament_list.html'

    def get(self, request):
        return render(request, self.template_name)


class SingleTournamentJoin(View):
    template_name = 'singletournaments/singletournament_join.html'
    form_class = SingleEliminationTournamentJoin

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

class SingleTournamentDetail(View):
    template_name = 'singletournaments/singletournament_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        return render(request, self.template_name, {'x':pk, 'tournament':tournament})

class SingleTournamentTeamsList(View):
    template_name = 'singletournaments/singletournament_teams.html'


class SingleTournamentRules(View):
    template_name = 'singletournaments/singletournament_rules.html'

class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        if  tournament.size == 4:
            # get 2 rounds to pass to the view
            round1 = SingleTournamentRound.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.get(tournament=tournament, roundnum=2)
            template_name = 'singletournaments/singletournament_bracket4.html'
        elif tournament.size == 8:
            # get 3 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket8.html'
        elif tournament.size == 16:
            # get 4 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket16.html'
        elif tournament.size == 32:
            # get 5 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket32.html'
        elif tournamenet.size == 64:
            # get 6 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket64.html'
        elif tournament.size == 128:
            # get 7 rounds to pass to the  view
            template_name = 'singletournaments/singletournament_bracket128.html'
        return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'round1':round1, 'round2':round2})
