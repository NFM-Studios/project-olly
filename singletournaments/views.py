from django.shortcuts import render
from django.views.generic import View
from .forms import SingleEliminationTournamentJoin


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
    template_name = 'singletournaments/singletournament_bracket.html'
