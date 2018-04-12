from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound
from teams.models import Team, TeamInvite
from matches.models import Match, MatchReport, MatchDispute
from .forms import MatchReportCreateForm, DisputeCreateForm


class TournamentMatchDetailView(DetailView):
    model = Match
    template_name = 'matches/tournament_matches_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        match = Match.objects.get(id=pk)
        return render(request, self.template_name, {'x': pk, 'match': match})


class MatchReportCreateView(CreateView):
    form_class = MatchReportCreateForm
    template_name = 'matches/matches_report.html'

    def form_valid(self, form):
        report = form.instance
        report.reporting_user = self.request.user
        match = Match.objects.get(id=form.data['match'])
        team1 = Team.objects.get(id=match.hometeam_id)
        team2 = Team.objects.get(id=match.awayteam_id)
        team1_reporters = TeamInvite.objects.filter(team=team1, hasPerms=True)
        team2_reporters = TeamInvite.objects.filter(team=team2, hasperms=True)
        reporter_team = TeamInvite.objects.get(user=self.request.user, team=[team1, team2]).team
        if report.reporter in team1_reporters or report.reporter in team2_reporters:
            report.match = match
            report.reporting_team = reporter_team.id
            report.reported_winner = form.data['winner']
            if reporter_team == team1:
                match.team1reported = True
                match.team1reportedwinner = report.reported_winner
                match.team1reportedwinner_id = report.reported_winner.id
            elif reporter_team == team2:
                match.team2reported = True
                match.team2reportedwinner = report.reported_winner
                match.team2reportedwinner_id = report.reported_winner.id
            else:
                messages.error(self.request, "Something went wrong (this shouldn't be seen)")
                return redirect('singletournaments:list')
            match.save()
            report.save()
            if match.team1reported and match.team2reported:
                reports = MatchReport.objects.filter(match_id=form.data['match'])
                report1 = MatchReport.objects.get(team=team1)
                report2 = MatchReport.objects.get(team=team2)
                if reports[0].reported_winner != reports[1].reported_winner:
                    messages.warning(self.request, "Both teams have reported different winners; a dispute has been created")
                    dispute = DisputeCreateForm(None)
                    dispute.auto_id = form.data['match']
                    dispute.match = form.data['match']
                    dispute.team1 = team1
                    dispute.team2 = team2
                    dispute.team1origreporter = report1.reporter
                    dispute.team2origreporter = report2.reporter
                    return redirect('matches:dispute', pk=form.data['match'])
            self.success_url = reverse('matches:detail', args=[match.id])
            messages.success(self.request, 'Your Report has been successfully submitted')
            return super(MatchReportCreateView, self).form_valid(form)
        else:
            messages.error(self.request, "You don't have permissions to report on this match")
            return redirect('singletournaments:list')


class MatchDisputeReportCreateView(CreateView):
    form_class = DisputeCreateForm
    template_name = 'matches/tournament_matches_dispute.html'

    def get(self, request, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form, **kwargs):
        match = Match.objects.get(id=self.kwargs['pk'])
        dispute = form.instance
        dispute.reporting_user = self.request.user
        dispute.match_id = self.kwargs['pk']
        dispute.teamproof = form.data['teamproof']
        dispute.teamproof_1 = form.data['teamproof_1']
        dispute.teamproof_2 = form.data['teamproof_2']
        dispute.teamproof_3 = form.data['teamproof_3']
        dispute.team1_id = match.hometeam_id
        dispute.team2_id = match.awayteam_id



