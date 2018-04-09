from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SingleEliminationTournamentJoin
from .models import SingleTournamentRound, SingleEliminationTournament, SingleTournamentTeam
from teams.models import TeamInvite, Team
from django.contrib import messages
from profiles.models import UserProfile
from store.models import deduct_credits


class List(View):
    template_name = 'singletournaments/singletournament_list.html'

    def get(self, request):
        return render(request, self.template_name)


'''class SingleTournamentJoin(View):
    template_name = 'singletournaments/singletournament_join.html'
    form_class = SingleEliminationTournamentJoin

    def get(self, request):
        teams = TeamInvite.objects.filter(user_id=request.user.id, hasPerms=True)
        if teams.exists():
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, message="You aren't a captain or founder of any team!")
            return redirect('singletournaments:list')

    def post(self, request):
        form = self.form_class(request.POST)
        try:
            invite = TeamInvite.objects.get(user=request.user, team=form.data['teams'])
        except:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:list')
        if invite.hasPerms:
            tournament = SingleEliminationTournament.objects.get(id=form.data['tournaments'])
            if tournament.teamformat == 0: players = 1
            elif tournament.teamformat == 1: players = 2
            elif tournament.teamformat == 2: players = 3
            elif tournament.teamformat == 3: players = 4
            elif tournament.teamformat == 4: players = 5
            elif tournament.teamformat == 5: players = 6
            team = Team.objects.get(id=int(form.data['teams']))
            users = TeamInvite.objects.filter(team=form.data['teams'])
            teams = tournament.teams.all()
            teameligible = False
            if teams.count() >= 2:
                messages.error(request, "This tournament is full")
                return redirect('singletournaments:list')
            for invite in users:
                user = UserProfile.objects.get(user_id=invite.user.id)
                if not user.xbl_verified or not user.psn_verified:
                    teameligible = False
                    messages.error(request, "One or more users does not have Xbox Live or PSN set")
                    return redirect('teams:list')
                elif int(user.credits) < int(tournament.req_credits):
                    teameligible = False
                    messages.error(request, "One or more players does not have enough credits")
                    return redirect('teams:list')
                else:
                    teameligible = True
                if not teameligible:
                    messages.error(request, "Not all members of your team are eligible to join")
            if len(users) > players:
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
            else:
                tournament.teams.add(new_team)
                for user in new_team_users:
                    deduct_credits(user, tournament.req_credits)
                tournament.save()
                tournament_team = SingleTournamentTeam(team_id=team.id, round_id=1, tournament_id=tournament.id)
                tournament_team.save()
                messages.success(request, message="Joined tournament")
                return redirect('singletournaments:list')
        else:
            messages.error(request, message="You can't join a tournament if you aren't the captain or founder")
            return redirect('singletournaments:list')'''


class SingleTournamentDetail(View):
    template_name = 'singletournaments/singletournament_detail.html'
    form_class = SingleEliminationTournamentJoin

    def get(self, request, **kwargs):
        form = self.form_class(None)
        pk = self.kwargs['pk']
        tournament = SingleEliminationTournament.objects.get(id=pk)
        return render(request, self.template_name, {'x': pk, 'tournament': tournament, 'form': form})

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        form = self.form_class(request.POST)
        try:
            invite = TeamInvite.objects.get(user=request.user, team=form.data['teams'], hasPerms=True)
        except:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('singletournaments:detail', pk)
        tournament = SingleEliminationTournament.objects.get(id=pk)
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
        users = TeamInvite.objects.filter(team=form.data['teams'])
        teams = tournament.teams.all()
        teameligible = False
        if teams.count() >= 2:
            messages.error(request, "This tournament is full")
            return redirect('singletournaments:detail', pk)
        for invite in users:
            user = UserProfile.objects.get(user_id=invite.user.id)
            if not user.xbl_verified or not user.psn_verified:
                teameligible = False
                messages.error(request, "One or more users does not have Xbox Live or PSN set")
                return redirect('teams:list')
            elif int(user.credits) < int(tournament.req_credits):
                teameligible = False
                messages.error(request, "One or more players does not have enough credits")
                return redirect('teams:list')
            else:
                teameligible = True
            if not teameligible:
                messages.error(request, "Not all members of your team are eligible to join")
        if len(users) > players:
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
            return redirect('singletournaments:detail', pk)
        for user in new_team_users:
            if user in tournament_teams_users:
                messages.error(request, "There is overlap between users in teams in the tournament")
                return redirect('singletournaments:detail', pk)
        else:
            tournament.teams.add(new_team)
            for user in new_team_users:
                deduct_credits(user, tournament.req_credits)
            tournament.save()
            tournament_team = SingleTournamentTeam(team_id=new_team.id, round_id=1, tournament_id=tournament.id)
            tournament_team.save()
            messages.success(request, message="Joined tournament")
            return redirect('singletournaments:detail', pk)


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
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2})

        elif tournament.size == 8:
            # get 3 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket8.html'
            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
            round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                           'round3': round3})

        elif tournament.size == 16:
            # get 4 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket16.html'
            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
            round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
            round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                           'round3': round3, 'round4': round4})

        elif tournament.size == 32:
            # get 5 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket32.html'
            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
            round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
            round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
            round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                           'round3': round3, 'round4': round4, 'round5': round5})


        elif tournament.size == 64:
            # get 6 rounds to pass to the view
            template_name = 'singletournaments/singletournament_bracket64.html'
            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
            round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
            round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
            round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)
            round6 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=6)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                           'round3': round3, 'round4': round4, 'round5': round5, 'round6': round6})


        elif tournament.size == 128:
            # get 7 rounds to pass to the  view
            template_name = 'singletournaments/singletournament_bracket128.html'
            round1 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=1)
            round2 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=2)
            round3 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=3)
            round4 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=4)
            round5 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=5)
            round6 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=6)
            round7 = SingleTournamentRound.objects.get(tournament=tournament, roundnum=7)

            return render(request, self.template_name,
                          {'x': pk, 'tournament': tournament, 'teams': teams, 'round1': round1, 'round2': round2,
                           'round3': round3, 'round4': round4, 'round5': round5, 'round6': round6, 'round7': round7})

