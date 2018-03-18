from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from singletournaments.models import SingleEliminationTournament
from teams.models import Team
from matches.models import Match


class TournamentMatchDetailView(DetailView):
    model = Match

class MatchReportCreateView(CreateView):
    form_class = MatchReportCreateForm
    template_name = 'matches/matches_report.html'

    def form_valid(self, form):
        report = form.instance
        report.reporter = self.request.user
        report.
        report.save()
        self.success_url = reverse('matches:detail', args=[matches.id])
        messages.success(self.request, 'Your Report has been successfully submitted')
        return super(MatchReportCreateView, self).form_valid(form)
