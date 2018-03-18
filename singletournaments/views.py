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



