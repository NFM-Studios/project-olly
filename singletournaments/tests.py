from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from matches.models import GameChoice, PlatformChoice
from profiles.models import UserProfile
from singletournaments.models import SingleEliminationTournament, SingleTournamentRuleset, SingleTournamentTeam
from teams.models import Team


class SingleTournamentTestCase(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='tournfounder', password='pass')
        self.player1 = User.objects.create_user(username='tournplayer1', password='pass')
        self.player2 = User.objects.create_user(username='tournplayer2', password='pass')
        self.game = GameChoice.objects.create(name='CSGO')
        self.platform = PlatformChoice.objects.create(name='PC')
        self.ruleset = SingleTournamentRuleset.objects.create(name='Standard', text='Rules',
                                                              creator=self.founder)
        now = timezone.now()
        self.tournament = SingleEliminationTournament.objects.create(
            name='Test Tournament', teamformat=1, bestof=1, active=True,
            open_register=now - datetime.timedelta(hours=1),
            close_register=now + datetime.timedelta(hours=1),
            start=now + datetime.timedelta(days=1),
            ruleset=self.ruleset, game=self.game, platform=self.platform,
            size=8, req_credits=0)
        self.team = Team.objects.create(name='TournamentTeam')
        self.team.founder = self.founder
        self.team.save()
        self.team.players.add(self.player1)
        self.team.players.add(self.player2)
        profile = UserProfile.objects.get(user=self.founder)
        profile.founder_teams.add(self.team)
        profile.save()

    def test_teams_list_renders(self):
        # regression: tournament.teams.all was missing the call parens
        self.client.login(username='tournfounder', password='pass')
        response = self.client.get(reverse('singletournaments:teams', args=[self.tournament.pk]))
        self.assertEqual(response.status_code, 200)

    def test_join_tournament(self):
        # regression: team.players manager iteration, len() on managers, and multi-user
        # credit deductions crashed the join view
        self.client.login(username='tournfounder', password='pass')
        response = self.client.post(reverse('singletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.tournament.teams.filter(pk=self.team.pk).exists())
        self.assertTrue(SingleTournamentTeam.objects.filter(team=self.team, tournament=self.tournament).exists())

    def test_leave_tournament(self):
        # regression: queryset | instance TypeError crashed the leave view
        self.tournament.teams.add(self.team)
        SingleTournamentTeam.objects.create(team=self.team, tournament=self.tournament)
        self.client.login(username='tournfounder', password='pass')
        response = self.client.post(reverse('singletournaments:leave', args=[self.tournament.pk]),
                                    {'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())
        self.assertFalse(SingleTournamentTeam.objects.filter(team=self.team, tournament=self.tournament).exists())