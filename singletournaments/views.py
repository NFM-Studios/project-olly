#import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View

from profiles.models import UserProfile
from store.models import deduct_credits, give_credits
from teams.models import TeamInvite, Team
from .forms import SingleEliminationTournamentJoinGet, SingleEliminationTournamentJoinPost, \
    SingleEliminationTournamentSort, SingleTournamentLeaveForm
from .models import SingleTournamentRound, SingleEliminationTournament, SingleTournamentTeam
from pages.models import Partner, StaticInfo


class List(View):
    form_class = SingleEliminationTournamentSort

    def get(self, request):
        form = self.form_class(None)
        tournament_list = SingleEliminationTournament.objects.all().filter(active=True)
        return render(request, 'singletournaments/singletournament_list.html',
                      {'tournament_list': tournament_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        form.is_valid()
        platform = form.cleaned_data['platform']
        game = form.cleaned_data['game']

        if game == 'all':
            tournament_list_ = SingleEliminationTournament.objects.all()
        else:
            tournament_list_ = SingleEliminationTournament.objects.filter(game=game)

        if platform == 'all':
            tournament_list1 = SingleEliminationTournament.objects.all()
        else:
            tournament_list1 = SingleEliminationTournament.objects.filter(platform=platform)

        tournament_list = tournament_list1 & tournament_list_
        return render(request, 'singletournaments/singletournament_list.html',
                      {'tournament_list': tournament_list, 'form': form})


class SingleTournamentJoin(View):

    def get(self, request, pk):
        teaminvites = TeamInvite.objects.filter(user_id=request.user.id, hasPerms=True)
        tournament = get_object_or_404(SingleEliminationTournament, id=pk)
        if teaminvites.exists():
            form = SingleEliminationTournamentJoinGet(request)
            return render(request, 'singletournaments/singletournament_join.html',
                          {'form': form, 'tournament': tournament})
        else:
            messages.error(request, message="You aren't a captain or founder of any team!")
            return redirect('singletournaments:list')

    def post(self, request, pk):
        form = SingleEliminationTournamentJoinPost(request.POST)
        try:
            invite = TeamInvite.objects.get(user=request.user, team=form.data['teams'])
        except:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:list')
        if invite.hasPerms:
            tournament = SingleEliminationTournament.objects.get(id=self.kwargs['pk'])
            if tournament.teamformat == 0:
                players = 1
            elif tournament.teamformat == 1:
                players = 2
            elif tournament.teamformat == 2:
                players = 3
            elif tournament.teamformat == 3:
                players = 4
            elif tournament.teamformat == 4:
                players = 5
            elif tournament.teamformat == 5:
                players = 6
            team = Team.objects.get(id=int(form.data['teams']))
            users = TeamInvite.objects.filter(team=form.data['teams'], accepted=True)
            teams = tournament.teams.all()
            teameligible = False
            #utc = pytz.UTC
            #now = utc.localize(datetime.datetime.now())

            """if tournament.open_register >= now:
                messages.error(request, 'Registration for this tournament is not open yet')
                return redirect('singletournaments:list')

            if tournament.close_register <= now:
                messages.error(request, 'Registration for this tournament is closed already')
                return redirect('singletournaments:list')
            """

            if not tournament.allow_register:
                messages.error(request, 'Registration for this tournament is not open currently')
                return redirect('singletournaments:list')

            if tournament.bracket_generated:
                messages.error(request, "The bracket has already been generated for this tournament, new teams aren't "
                                        "permitted")
                return redirect('singletournaments:list')

            if teams.count() >= tournament.size:
                messages.error(request, "This tournament is full")
                return redirect('singletournaments:list')
            for invite in users:
                user = UserProfile.objects.get(user_id=invite.user.id)
                """if not user.xbl_verified and tournament.platform == 1:
                    teameligible = False
                    messages.error(request, "One or more users does not have Xbox Live set")
                    return redirect('teams:list')
                elif not user.psn_verified and tournament.platform == 0:
                    teameligible = False
                    messages.error(request, "One or more users does not have PSN set")
                    return redirect('teams:list')"""
                if int(user.credits) < int(tournament.req_credits):
                    teameligible = False
                    messages.error(request, "One or more players does not have enough credits")
                    return redirect('teams:list')
                else:
                    teameligible = True
                if not teameligible:
                    messages.error(request, "Not all members of your team are eligible to join")
            if len(users) != players:
                teameligible = False
            if not teameligible:
                messages.error(request, "There was an issue with team eligibility for this tournament")
                return redirect('teams:list')
            tournament_teams_query = tournament.teams.all()
            tournament_teams = []
            tournament_teams_invites_query = None
            tournament_teams_invites = []
            tournament_teams_users = []
            new_team = Team.objects.get(id=int(form.data['teams']))
            new_team_invites = TeamInvite.objects.filter(team=new_team)
            new_team_users = []
            for team in tournament_teams_query:
                tournament_teams.append(team)
            for team in tournament_teams:
                tournament_teams_invites_query = TeamInvite.objects.filter(team=team)
            try:
                for invite in tournament_teams_invites_query:
                    tournament_teams_invites.append(invite)
            except:
                pass
            try:
                for invite in tournament_teams_invites:
                    tournament_teams_users.append(invite.user)
            except:
                pass
            for invite in new_team_invites:
                new_team_users.append(invite.user)
            if new_team in tournament_teams:
                messages.error(request, message="This team is already in this tournament")
                return redirect('singletournaments:list')
            for user in new_team_users:
                if user in tournament_teams_users:
                    messages.error(request, "There is overlap between users in teams in the tournament")
                    return redirect('singletournaments:list')

            tournament.teams.add(new_team)
            for user in new_team_users:
                deduct_credits(user, tournament.req_credits)
            tournament.save()
            tournament_team = SingleTournamentTeam(team_id=team.id, tournament_id=tournament.id)
            tournament_team.save()
            messages.success(request, message="Joined tournament")
            return redirect('singletournaments:list')
        else:
            messages.error(request, message="You can't join a tournament if you aren't the captain or founder")
            return redirect('singletournaments:list')


class SingleTournamentLeave(View):
    def get(self, request, pk):
        form = SingleTournamentLeaveForm()
        return render(request, 'singletournaments/singletournament_leave.html', {'form': form})

    def post(self, request, pk):
        form = SingleTournamentLeaveForm(request.POST)
        tournament = SingleEliminationTournament.objects.filter(id=pk)
        user_teams = Team.objects.filter(id__in=tournament.values('teams'), founder=request.user)
        if not user_teams.exists():
            messages.error(request, "You are not in this tournament")
            return redirect('singletournaments:list')
        else:
            tournament = SingleEliminationTournament.objects.get(id=pk)
            if not tournament.bracket_generated:
                form.is_valid()
                if not form.cleaned_data['confirm']:
                    messages.error(request, "You submitted without confirming that you wanted to leave")
                    return redirect('singletournaments:leave', pk=pk)
                else:
                    user_team = Team.objects.get(id__in=tournament.values('teams'), founder=request.user)
                    team = SingleTournamentTeam.objects.get(team_id=user_team.id, tournament=tournament)
                    team.delete()
                    tournament.teams.remove(user_team)
                    team_users = TeamInvite.objects.filter(team=user_team)
                    users = []
                    for invite in team_users:
                        users.append(invite.user)
                    for user in users:
                        give_credits(user=user, num=tournament.req_credits)
                    messages.success(request, "Gave %s credits to %s users" % (tournament.req_credits, len(users)))
                    messages.success(request, "Left tournament %s" % tournament.name)
                    return redirect('singletournaments:list')
            else:
                messages.error(request, "The bracket has been generated already, you cannot leave the tournament")
                return redirect('singletournaments:detail', pk=pk)


class SingleTournamentDetail(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(SingleEliminationTournament, id=pk)
        ruleset = tournament.ruleset
        teams = tournament.teams.all()
        return render(request, 'singletournaments/singletournament_detail.html',
                      {'pk': pk, 'tournament': tournament, 'ruleset': ruleset, 'teams': teams})


class SingleTournamentTeamsList(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all
        return render(request, 'singletournaments/singletournament_teams.html',
                      {'x': pk, 'tournament': tournament, 'teams': teams})


class SingleTournamentRules(View):

    def get(self, request, pk):
        pk = pk
        tournament = SingleEliminationTournament.objects.get(id=pk)
        ruleset = tournament.ruleset
        return render(request, 'singletournaments/ruleset_detail.html',
                      {'pk': pk, 'ruleset': ruleset})


class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        teams = tournament.teams.all()
        if tournament.bracket_generated:
            # show the right bracket
            rounds = SingleTournamentRound.objects.all().filter(tournament=tournament)
            return render(request, 'singletournaments/singletournament_bracket.html', {'x':pk, 'tournament': tournament,
                                                                                       'teams':teams, 'rounds': rounds})
        else:
            # show some template that its not generated yet
            return render(request, 'singletournaments/no_bracket.html',
                          {'tournament': tournament})
