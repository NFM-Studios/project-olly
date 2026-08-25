from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from matches.models import GameChoice, PlatformChoice
from profiles.models import UserProfile
from singletournaments.models import (SingleEliminationTournament, SingleTournamentRound,
                                      SingleTournamentRuleset, SingleTournamentTeam)
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

    def test_allow_register_overrides_closed_window(self):
        self.tournament.close_register = timezone.now() - datetime.timedelta(hours=1)
        self.tournament.allow_register = True
        self.tournament.save()
        self.client.login(username='tournfounder', password='pass')
        response = self.client.post(reverse('singletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.tournament.teams.filter(pk=self.team.pk).exists())

    def test_registration_closed_rejected_without_override(self):
        self.tournament.close_register = timezone.now() - datetime.timedelta(hours=1)
        self.tournament.allow_register = False
        self.tournament.save()
        self.client.login(username='tournfounder', password='pass')
        response = self.client.post(reverse('singletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())

    def test_registration_not_open_rejected_without_override(self):
        self.tournament.open_register = timezone.now() + datetime.timedelta(hours=1)
        self.tournament.allow_register = False
        self.tournament.save()
        self.client.login(username='tournfounder', password='pass')
        response = self.client.post(reverse('singletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())


class BracketGenerationTest(TestCase):
    def setUp(self):
        self.game = GameChoice.objects.create(name='CSGO')
        self.platform = PlatformChoice.objects.create(name='PC')
        self.ruleset = SingleTournamentRuleset.objects.create(name='Rules', text='Rules')
        now = timezone.now()

        def make_user(username):
            return User.objects.create_user(username=username, password='pass')

        def make_team(name, founder_user, xp):
            team = Team.objects.create(name=name)
            team.founder = founder_user
            team.save()
            profile = UserProfile.objects.get(user=founder_user)
            profile.xp = xp
            profile.save()
            return team

        self.u1 = make_user('bracket_u1')
        self.u2 = make_user('bracket_u2')
        self.u3 = make_user('bracket_u3')
        self.u4 = make_user('bracket_u4')
        self.team_high = make_team('HighXpTeam', self.u1, 100)
        self.team_mid = make_team('MidXpTeam', self.u2, 50)
        self.team_low = make_team('LowXpTeam', self.u3, 25)
        self.team_none = make_team('NoXpTeam', self.u4, 0)

        def make_tournament(name, xp_seed):
            return SingleEliminationTournament.objects.create(
                name=name, teamformat=1, bestof=1, active=True,
                open_register=now - datetime.timedelta(hours=1),
                close_register=now + datetime.timedelta(hours=1),
                start=now + datetime.timedelta(days=1),
                ruleset=self.ruleset, game=self.game, platform=self.platform,
                size=8, req_credits=0, xp_seed=xp_seed)

        self.tournament_xp = make_tournament('XpSeededTournament', True)
        self.tournament_three = make_tournament('ThreeTeamTournament', False)

    def test_xp_seed_orders_bracket_by_xp(self):
        self.tournament_xp.teams.add(self.team_high, self.team_mid, self.team_low, self.team_none)
        self.tournament_xp.generate_bracket()
        round1 = SingleTournamentRound.objects.get(tournament=self.tournament_xp, roundnum=1)
        matches = list(round1.matches.all())
        self.assertEqual(len(matches), 2)
        # highest XP team is matched against the second highest, etc
        self.assertEqual(matches[0].awayteam, self.team_high)
        self.assertEqual(matches[0].hometeam, self.team_mid)
        self.assertEqual(matches[1].awayteam, self.team_low)
        self.assertEqual(matches[1].hometeam, self.team_none)

    def test_three_team_bracket_has_bye(self):
        self.tournament_three.teams.add(self.team_high, self.team_mid, self.team_low)
        self.tournament_three.generate_bracket()
        round1 = SingleTournamentRound.objects.get(tournament=self.tournament_three, roundnum=1)
        matches = list(round1.matches.all())
        self.assertEqual(len(matches), 2)
        bye_matches = [m for m in matches if m.bye_1]
        regular_matches = [m for m in matches if not m.bye_1]
        self.assertEqual(len(bye_matches), 1)
        self.assertEqual(len(regular_matches), 1)
        # the bye team advances automatically
        bye = bye_matches[0]
        self.assertIsNone(bye.hometeam)
        self.assertIsNotNone(bye.awayteam)
        self.assertEqual(bye.winner, bye.awayteam)
        self.assertTrue(bye.completed)
        self.assertNotIn(bye.awayteam, [m.awayteam for m in regular_matches] +
                         [m.hometeam for m in regular_matches])

    def test_even_bracket_no_byes(self):
        self.tournament_xp.teams.add(self.team_high, self.team_mid, self.team_low, self.team_none)
        self.tournament_xp.generate_bracket()
        round1 = SingleTournamentRound.objects.get(tournament=self.tournament_xp, roundnum=1)
        matches = list(round1.matches.all())
        self.assertEqual(len(matches), 2)
        self.assertFalse(any(m.bye_1 for m in matches))
        self.assertTrue(all(m.hometeam is not None and m.awayteam is not None for m in matches))