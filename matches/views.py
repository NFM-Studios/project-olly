from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from singletournaments.models import SingleEliminationTournament
from teams.models import Team
from matches.models import Match


class TournamentMatchDetailView(DetailView):
    model = Match
    template_name = 'matches/matches_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        match = match.objects.get(id=pk)
        return render(request, self.template_name, {'x': pk, 'match': match})


class MatchReportCreateView(CreateView):
    form_class = MatchReportCreateForm
    template_name = 'matches/matches_report.html'

    def form_valid(self, form):
        report = form.instance
        report.reporter = self.request.user
        if report.reporter
        report.save()
        self.success_url = reverse('matches:detail', args=[matches.id])
        messages.success(self.request, 'Your Report has been successfully submitted')
        return super(MatchReportCreateView, self).form_valid(form)
