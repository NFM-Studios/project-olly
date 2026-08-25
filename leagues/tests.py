import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from leagues.models import League, LeagueDivision, LeagueSettings, LeagueTeam
from matches.models import GameChoice, PlatformChoice
from profiles.models import Notification, UserProfile
from singletournaments.models import SingleTournamentRuleset
from teams.models import Team


class LeagueJoinLeaveTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='leagueuser', password='pass')
        self.player1 = User.objects.create_user(username='leagueplayer1', password='pass')
        self.player2 = User.objects.create_user(username='leagueplayer2', password='pass')
        self.game = GameChoice.objects.create(name='CSGO')
        self.platform = PlatformChoice.objects.create(name='PC')
        self.ruleset = SingleTournamentRuleset.objects.create(name='League Rules', text='Rules',
                                                              creator=self.user)
        self.settings = LeagueSettings.objects.create(name='League Settings')
        now = timezone.now()
        self.league = League.objects.create(
            name='Test League', settings=self.settings, ruleset=self.ruleset,
            open_register=now - datetime.timedelta(hours=1),
            close_register=now + datetime.timedelta(hours=1),
            start=now + datetime.timedelta(days=7),
            game=self.game, platform=self.platform, size=8, teamformat=0, req_credits=0)
        self.team = Team.objects.create(name='LeagueTeam')
        self.team.founder = self.user
        self.team.save()
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.founder_teams.add(self.team)
        self.profile.credits = 100
        self.profile.save()

    def test_join_league_adds_team_and_deducts_credits(self):
        self.league.req_credits = 50
        self.league.save()
        self.client.login(username='leagueuser', password='pass')
        response = self.client.post(reverse('leagues:join', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.credits, 50)
        self.assertEqual(self.league.teams.count(), 1)
        self.assertTrue(self.league.teams.filter(team=self.team).exists())
        # a division is created and the team placed into it
        self.assertEqual(self.league.divisions.count(), 1)
        league_team = LeagueTeam.objects.get(team=self.team)
        self.assertTrue(self.league.divisions.first().teams.filter(pk=league_team.pk).exists())
        # a notification was sent to the acting user
        self.assertTrue(Notification.objects.filter(type='league', pk1=self.league.pk,
                                                    user_notifications=self.profile).exists())

    def test_join_league_full_rejected(self):
        self.league.size = 1
        self.league.save()
        other_team = Team.objects.create(name='OtherTeam')
        other_team.founder = self.user
        other_team.save()
        self.league.teams.add(LeagueTeam.objects.create(team=other_team))
        self.client.login(username='leagueuser', password='pass')
        response = self.client.post(reverse('leagues:join', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.league.teams.count(), 1)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.credits, 100)

    def test_join_league_registration_closed_rejected(self):
        self.league.close_register = timezone.now() - datetime.timedelta(hours=1)
        self.league.allow_register = False
        self.league.save()
        self.client.login(username='leagueuser', password='pass')
        response = self.client.post(reverse('leagues:join', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.league.teams.count(), 0)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.credits, 100)

    def test_join_league_registration_not_open_rejected(self):
        self.league.open_register = timezone.now() + datetime.timedelta(hours=1)
        self.league.allow_register = False
        self.league.save()
        self.client.login(username='leagueuser', password='pass')
        response = self.client.post(reverse('leagues:join', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.league.teams.count(), 0)

    def test_join_league_non_leader_rejected(self):
        # a user who isn't the founder or captain of the team cannot join it
        other_user = User.objects.create_user(username='leagueother', password='pass')
        self.client.login(username='leagueother', password='pass')
        response = self.client.post(reverse('leagues:join', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.league.teams.count(), 0)

    def test_join_league_balances_across_divisions(self):
        self.settings.max_division_size = 1
        self.settings.save()
        division1 = LeagueDivision.objects.create()
        division2 = LeagueDivision.objects.create()
        self.league.divisions.add(division1, division2)
        self.client.login(username='leagueuser', password='pass')
        self.client.post(reverse('leagues:join', args=[self.league.pk]), {'team': self.team.pk})
        # a second team joins and must be placed into the other division
        other_team = Team.objects.create(name='BalancedTeam')
        other_team.founder = self.user
        other_team.save()
        self.profile.founder_teams.add(other_team)
        self.client.post(reverse('leagues:join', args=[self.league.pk]), {'team': other_team.pk})
        league_team1 = LeagueTeam.objects.get(team=self.team)
        league_team2 = LeagueTeam.objects.get(team=other_team)
        self.assertEqual(division1.teams.count() + division2.teams.count(), 2)
        self.assertNotEqual(division1.teams.filter(pk=league_team1.pk).exists(),
                            division1.teams.filter(pk=league_team2.pk).exists())

    def test_leave_league_removes_team_without_refund(self):
        self.league.req_credits = 50
        self.league.save()
        self.client.login(username='leagueuser', password='pass')
        self.client.post(reverse('leagues:join', args=[self.league.pk]), {'team': self.team.pk})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.credits, 50)
        response = self.client.post(reverse('leagues:leave', args=[self.league.pk]),
                                    {'team': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.league.teams.count(), 0)
        self.assertFalse(LeagueTeam.objects.filter(team=self.team).exists())
        # no refund is given on leaving
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.credits, 50)