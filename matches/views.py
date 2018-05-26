from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib import messages
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound
from teams.models import Team, TeamInvite
from matches.models import Match, MatchReport, MatchDispute
from .forms import MatchReportCreateFormGet, MatchReportCreateFormPost, DisputeCreateForm


class TournamentMatchDetailView(DetailView):
    model = Match
    template_name = 'matches/tournament_matches_detail.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        match = Match.objects.get(id=pk)
        return render(request, self.template_name, {'x': pk, 'match': match})


class MatchReportCreateView(View):
    template_name = 'matches/matches_report.html'

    def get(self, request, pk):
        form = MatchReportCreateFormGet(request)
        return render(request, self.template_name, {'form': form, 'pk':pk})

    def post(self, request, pk):
        form = MatchReportCreateFormPost(request.POST)
        report = form.instance
        report.reporting_user = self.request.user
        match = Match.objects.get(id=self.kwargs['pk'])
        team1 = Team.objects.get(id=match.hometeam_id)
        team2 = Team.objects.get(id=match.awayteam_id)
        team1_reporters = TeamInvite.objects.filter(team=team1, hasPerms=True)
        team2_reporters = TeamInvite.objects.filter(team=team2, hasPerms=True)

        if TeamInvite.objects.filter(user=self.request.user, team=team1).exists():
            reporter_team = TeamInvite.objects.get(user=self.request.user, team=team1)
        elif TeamInvite.objects.filter(user=self.request.user, team=team2).exists():
            reporter_team = TeamInvite.objects.get(user=self.request.user, team=team2)
        else:
            messages.error(request, message="Something went wrong, please try again (maybe reporting from the incorrect account?)")
            return redirect('matches:detail', pk=pk)

        if MatchReport.objects.filter(match=match.id, reporting_team=team1).exists() and reporter_team.id == team1.id:
            messages.error(request, "Your team has already reported this match")
            return redirect('matches:detail', pk=pk)
        elif MatchReport.objects.filter(match=match.id, reporting_team=team2).exists() and reporter_team.id == team2.id:
            messages.error(request, "Your team has already reported this match")
            return redirect('matches:detail', pk=pk)
        else:
            if reporter_team in team1_reporters or reporter_team in team2_reporters:
                report.match = match
                report.reporting_team = reporter_team.team
                reported_team = Team.objects.get(id=form.data['reported_winner'])
                report.reported_winner = reported_team
                if reporter_team.team == team1:
                    match.team1reported = True
                    match.team1reportedwinner = report.reported_winner
                    match.team1reportedwinner_id = report.reported_winner.id
                elif reporter_team.team == team2:
                    match.team2reported = True
                    match.team2reportedwinner = report.reported_winner
                    match.team2reportedwinner_id = report.reported_winner.id
                else:
                    messages.error(self.request, "Something went wrong (this shouldn't be seen)")
                    return redirect('singletournaments:list')
                match.save()
                report.save()
                if match.team1reported and match.team2reported:
                    reports = MatchReport.objects.filter(match_id=match.id)
                    report1 = MatchReport.objects.get(reporting_team=team1, match_id=match.id)
                    report2 = MatchReport.objects.get(reporting_team=team2, match_id=match.id)
                    if reports[0].reported_winner != reports[1].reported_winner:
                        messages.warning(self.request,
                                         "Both teams have reported different winners; a dispute has been created")
                        # here
                        #dispute = DisputeCreateForm()
                        #dispute.auto_id = match.id
                        #dispute.match = match
                        #dispute.team1 = team1
                        #dispute.team2 = team2
                        #dispute.team1origreporter = report1.reporting_user
                        #dispute.team2origreporter = report2.reporting_user

                        dispute = MatchDispute(match=match, team1=team1, team2=team2,
                                               team1origreporter=report1.reporting_user,
                                               team2origreporter=report2.reporting_user)
                        dispute.save()
                        # to here might not stay
                        match.disputed = True
                        match.save()
                        return redirect('matches:dispute', pk=dispute.pk)
                    if match.team1reported:
                        # team 1 reported
                        if match.team1reportedwinner == team2:
                            # team1 is reporting that team2 won
                            # declare team2 as winner
                            match.winner = team2
                            match.save()
                        elif match.team1reportedwinner == team1:
                            # have to wait for the other team to confirm
                            pass
                    elif match.team2reported:
                        if match.team2reportedwinner == team1:
                            # team 1 wins
                            match.winner = team1
                            match.save()
                        elif match.team2reportedwinner == team2:
                            pass
                    if match.team1reported and match.team2reported:
                        if match.team2reportedwinner == team2 and match.team1reportedwinner == team2:

                            match.winner = team2
                            match.save()
                        elif match.team2reportedwinner == team1 and match.team1reportedwinner == team1:
                            match.winner = team1
                            match.save()
                #self.success_url = reverse('matches:detail', args=[match.id])
                messages.success(self.request, 'Your Report has been successfully submitted')
                return redirect('matches:detail', pk=pk)
            else:
                messages.error(self.request, "You don't have permissions to report on this match")
                return redirect('singletournaments:list')
        #else:
        #    messages.error(request, "A report has already been created for this match")
        #    return redirect('matches:detail', pk=pk)


class MatchDisputeReportCreateView(CreateView):
    form_class = DisputeCreateForm
    template_name = 'matches/tournament_matches_dispute.html'

    def get(self, request, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'dispute': kwargs['pk']})

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
        dispute.save()



