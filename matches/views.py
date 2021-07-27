from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, CreateView, View
from matches.models import Match, MatchReport, MatchDispute, MapPoolChoice, MatchCheckIn
from teams.models import Team
from .forms import MatchReportCreateFormGet, MatchReportCreateFormPost, DisputeCreateForm, TeamCheckInFormGet, TeamCheckInFormPost
from profiles.models import Notification, UserProfile
import datetime


class MapPoolDetail(DetailView):
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        # pool = get_object_or_404(MapPoolChoice, pk)
        pool = MapPoolChoice.objects.get(id=pk)
        return render(request, 'matches/mappool_detail.html', {'pool': pool})


class MatchList(View):

    def get(self, request):
        # teams = Team.objects.filter(
        #    Q(captains__exact=request.user) | Q(founder=request.user) | Q(players__exact=request.user))
        profile = UserProfile.objects.get(user=request.user)
        teams = profile.player_teams.all() | profile.captain_teams.all() | profile.founder_teams.all()
        matches_away = Match.objects.filter(awayteam__in=teams)
        matches_home = Match.objects.filter(hometeam__in=teams)
        matches = matches_away | matches_home
        return render(request, 'matches/matches_list.html', {'matches': matches})


class TournamentMatchDetailView(DetailView):
    model = Match

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        match = get_object_or_404(Match, id=pk)
        if not match.bye_2 and not match.bye_1:
            team1 = Team.objects.get(id=match.hometeam_id)
            team2 = Team.objects.get(id=match.awayteam_id)
            aplayers = team2.players.all()
            hplayers = team1.players.all()
            return render(request, 'matches/match_detail.html',
                          {'x': pk, 'match': match,
                           'aplayers': aplayers,
                           'hplayers': hplayers})
        elif match.bye_1:
            team1 = Team.objects.get(id=match.hometeam_id)
            hplayers = team1.players.all()
            return render(request, 'matches/match_detail.html',
                          {'x': pk, 'match': match,
                           'hplayers': hplayers})
        elif match.bye_2:
            return render(request, 'matches/match_detail.html',
                          {'x': pk, 'match': match})


class MatchReportCreateView(View):
    template_name = 'matches/matches_report.html'

    def get(self, request, pk):
        form = MatchReportCreateFormGet(request, pk)
        match = Match.objects.get(pk=pk)
        if match.disable_userreport:
            # user reports are disabled, return them to the match detail page with an error
            messages.error(request, "Match reports are disabled for this match")
            return redirect('matches:detail', pk=pk)
        return render(request, 'matches/matches_report.html', {'form': form, 'pk': pk})

    def post(self, request, pk):
        form = MatchReportCreateFormPost(request.POST)
        report = form.instance
        report.reporting_user = self.request.user
        match = Match.objects.get(id=self.kwargs['pk'])
        if not match.bye_2 and not match.bye_1:
            team1 = Team.objects.get(id=match.hometeam_id)
            team2 = Team.objects.get(id=match.awayteam_id)
            team1_reporters = team1.captains
            team2_reporters = team2.captains

            one_perms = False
            two_perms = False
            if self.request.user in team1.captain.all() or self.request.user == team1.founder:
                one_perms = True
            elif self.request.user in team2.captain.all() or self.request.user == team2.founder:
                two_perms = True
            else:
                messages.error(request, message="You don't have permission to report for any team in this match")
                if match.type == 'w':
                    return redirect('wagers:list')
                return redirect('matches:detail', pk=pk)

            if MatchReport.objects.filter(match=match.id,
                                          reporting_team=team1).exists() and one_perms:
                messages.error(request, "Your team has already reported this match")
                if match.type == 'w':
                    return redirect('wagers:list')
                return redirect('matches:detail', pk=pk)
            elif MatchReport.objects.filter(match=match.id,
                                            reporting_team=team2).exists() and two_perms:
                messages.error(request, "Your team has already reported this match")
                if match.type == 'w':
                    return redirect('wagers:list')
                return redirect('matches:detail', pk=pk)
            elif match.bye_1:
                messages.error(request, 'There is only one team in this match, reporting is unnecessary')
                return redirect('matches:list')

            elif match.bye_2:
                messages.error(request, 'There are no teams in this match')
                return redirect('matches:list')
            else:
                # if reporter_team in team1_reporters or reporter_team in team2_reporters:
                report.match = match
                reported_team = Team.objects.get(id=form.data['reported_winner'])
                report.reported_winner = reported_team
                if one_perms:
                    report.reporting_team = team1
                    match.team1reported = True
                    match.team1reportedwinner = report.reported_winner
                    match.team1reportedwinner_id = report.reported_winner.id

                elif two_perms:
                    report.reporting_team = team2
                    match.team2reported = True
                    match.team2reportedwinner = report.reported_winner
                    match.team2reportedwinner_id = report.reported_winner.id
                else:
                    messages.error(request, "ERROR: Could not verify the team that you're on")
                    return redirect('matches:detail', pk=match.id)

                match.save()
                report.save()
                if match.team1reported and match.team2reported:
                    reports = MatchReport.objects.filter(match_id=match.id)
                    report1 = MatchReport.objects.get(reporting_team=team1, match_id=match.id)
                    report2 = MatchReport.objects.get(reporting_team=team2, match_id=match.id)
                    if reports[0].reported_winner != reports[1].reported_winner:
                        dispute = MatchDispute(id=match.id, match=match, team1=team1, team2=team2,
                                               team1origreporter=report1.reporting_user,
                                               team2origreporter=report2.reporting_user)
                        dispute.save()
                        match.disputed = True
                        match.save()

                        for i in [report1.reporting_user, report2.reporting_user]:
                            test = Notification(title="A match you're playing in has been disputed")
                            test.link = 'matches:detail'
                            test.pk1 = match.pk
                            test.datetime = datetime.datetime.now()
                            test.save()
                            userprofile = UserProfile.objects.get(user=i.user)
                            userprofile.notifications.add(test)
                            userprofile.save()
                            if i.user.email_enabled:
                                current_site = get_current_site(request)
                                mail_subject = settings.SITE_NAME + ' match disputed!'
                                message = render_to_string('matches/dispute_email.html', {
                                    'user': i.username,
                                    'site': settings.SITE_NAME,
                                    'domain': current_site.domain,
                                    'pk': dispute.pk
                                })
                                to_email = i.email
                                email = EmailMessage(
                                    mail_subject, message, from_email=settings.FROM_EMAIL, to=[to_email]
                                )
                                email.send(fail_silently=True)

                        messages.warning(self.request,
                                         "Both teams have reported different winners; a dispute has been created")
                        return redirect('matches:dispute', pk=dispute.pk)
                    if match.team1reported:
                        # team 1 reported
                        if match.team1reportedwinner == team2:
                            # team1 is reporting that team2 won
                            # declare team2 as winner
                            match.winner = team2
                            match.loser = team1
                            match.save()
                        elif match.team1reportedwinner == team1:
                            # have to wait for the other team to confirm
                            pass
                    elif match.team2reported:
                        if match.team2reportedwinner == team1:
                            # team 1 wins
                            match.winner = team1
                            match.loser = team2
                            match.save()
                        elif match.team2reportedwinner == team2:
                            pass
                    if match.team1reported and match.team2reported:
                        if match.team2reportedwinner == team2 and match.team1reportedwinner == team2:
                            match.winner = team2
                            match.loser = team1
                            match.save()
                        elif match.team2reportedwinner == team1 and match.team1reportedwinner == team1:
                            match.winner = team1
                            match.loser = team2
                            match.save()
                # self.success_url = reverse('matches:detail', args=[match.id])
                messages.success(self.request, 'Your Report has been successfully submitted')
                if match.type == 'w':
                    return redirect('wagers:list')
                return redirect('matches:detail', pk=pk)
            # if match.type == 'w':
            #    return redirect('wagers:list')
            # return redirect('singletournaments:list')
    # else:
    #    messages.error(request, "A report has already been created for this match")
    #    return redirect('matches:detail', pk=pk)


class MatchDisputeReportCreateView(CreateView):
    form_class = DisputeCreateForm

    def get(self, request, **kwargs):
        form = self.form_class(None)
        return render(request, 'matches/tournament_matches_dispute.html',
                      {'form': form, 'dispute': kwargs['pk']})

    def form_valid(self, form, **kwargs):
        match = Match.objects.get(id=self.kwargs['pk'])
        dispute = form.instance
        dispute.reporting_user = self.request.user
        dispute.match_id = self.kwargs['pk']
        dispute.teamproof_1 = form.data['teamproof_1']
        dispute.teamproof_2 = form.data['teamproof_2']
        dispute.teamproof_3 = form.data['teamproof_3']
        dispute.team1_id = match.hometeam_id
        dispute.team2_id = match.awayteam_id
        matchreport = MatchReport.objects.get(match_id=match.id, reporting_user_id=self.request.user.id)
        matchreport_1 = MatchReport.objects.filter(match_id=match.id).exclude(
            reporting_user_id=self.request.user.id).get()
        if matchreport.reporting_team == match.hometeam:
            dispute.team1origreporter = matchreport.reporting_user
            dispute.team2origreporter = matchreport_1.reporting_user
        else:
            dispute.team2origreporter = matchreport.reporting_user
            dispute.team1origreporter = matchreport_1.reporting_user
        dispute.save()
        return redirect('matches:detail', pk=self.kwargs['pk'])


def match_checkin(request, pk):
    match = Match.objects.get(pk=pk)
    profile = UserProfile.objects.get(user__username=request.user.username)
    user = request.user
    away = match.awayteam
    home = match.hometeam
    if (user in away.captain.all() or user in home.captain.all()) or (user == away.founder or user == home.founder):
        return render(request, 'matches/match_checkin.html', {'match': match})
    else:
        messages.error(request, "You don't have permission to checkin for this match")
        return redirect('matches:detail', pk=pk)


def team_checkin(request, pk, teamid):
    # get the team they're trying to checkin from the get
    team = Team.objects.get(pk=teamid)
    # get the match from the pk in the url
    match = Match.objects.get(pk=pk)
    # get logged in user
    profile = UserProfile.objects.get(user__username=request.user.username)
    user = request.user
    if user == team.founder:
        pass
    elif user == team.captain.all():
        pass
    else:
        # they don't have perms - gtfo
        messages.error(request, "FFFFFYou do not have permissions to checkin this team")
        return redirect('matches:detail', pk=pk)
    if request.method == 'GET':
        # send the form, render
        form = TeamCheckInFormGet(team=team)
        return render(request, 'matches/team_checkin.html', {'form': form, 'match': match, 'teamid': teamid})
    elif request.method == 'POST':
        # lets make it and get the data
        # TODO: find a way to get the team instance in the form
        form = TeamCheckInFormPost(request.POST)
        if form.is_valid():
            temp = MatchCheckIn()
            temp.save()
            temp.match = match
            temp.team = team
            temp.reporter = user
            # TODO: verify posted data from form of field 'players'
            for playerid in form.data.getlist('players'):
                playerid = int(playerid)
                player = User.objects.get(pk=playerid)
                temp.players.add(player)
            temp.save()
            messages.success(request, 'Your team has been checked in, checkin #' + str(temp.pk))
            return redirect('matches:detail', pk=match.pk)
        else:
            print('dammit')
            print(form.cleaned_data)
            messages.error(request, "Form error, this should not occur")
            return redirect('matches:detail', pk=pk)


def create_checkin(request, pk):
    pass
