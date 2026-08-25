import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from matches.models import GameChoice, PlatformChoice
from profiles.models import UserProfile
from singletournaments.models import SingleTournamentRuleset
from teams.models import Team

from .models import DoubleEliminationRound, DoubleEliminationTeam, DoubleEliminationTournament


class DoubleEliminationTestCase(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='de_founder', password='pass')
        self.player1 = User.objects.create_user(username='de_player1', password='pass')
        self.player2 = User.objects.create_user(username='de_player2', password='pass')
        self.game = GameChoice.objects.create(name='CSGO')
        self.platform = PlatformChoice.objects.create(name='PC')
        self.ruleset = SingleTournamentRuleset.objects.create(name='Standard', text='Rules',
                                                              creator=self.founder)
        now = timezone.now()
        self.tournament = DoubleEliminationTournament.objects.create(
            name='Test DE Tournament', teamformat=1, bestof=1, active=True,
            open_register=now - datetime.timedelta(hours=1),
            close_register=now + datetime.timedelta(hours=1),
            start=now + datetime.timedelta(days=1),
            ruleset=self.ruleset, game=self.game, platform=self.platform,
            size=8, req_credits=0)
        self.team = Team.objects.create(name='DETeam')
        self.team.founder = self.founder
        self.team.save()
        self.team.players.add(self.player1)
        self.team.players.add(self.player2)
        profile = UserProfile.objects.get(user=self.founder)
        profile.founder_teams.add(self.team)
        profile.save()


class BracketGenerationTest(DoubleEliminationTestCase):
    def make_user(self, username):
        return User.objects.create_user(username=username, password='pass')

    def make_team(self, name, founder_user, xp):
        team = Team.objects.create(name=name)
        team.founder = founder_user
        team.save()
        profile = UserProfile.objects.get(user=founder_user)
        profile.xp = xp
        profile.save()
        return team

    def make_tournament(self, name, size, xp_seed=False):
        now = timezone.now()
        return DoubleEliminationTournament.objects.create(
            name=name, teamformat=1, bestof=1, active=True,
            open_register=now - datetime.timedelta(hours=1),
            close_register=now + datetime.timedelta(hours=1),
            start=now + datetime.timedelta(days=1),
            ruleset=self.ruleset, game=self.game, platform=self.platform,
            size=size, req_credits=0, xp_seed=xp_seed)

    def test_generate_bracket_4_teams(self):
        t = self.make_tournament('FourTeamTournament', 4)
        teams = [self.make_team('T%d' % i, self.make_user('four_u%d' % i), i * 10) for i in range(4)]
        t.teams.add(*teams)
        result = t.generate_bracket()
        self.assertIn('Bracket generated', result)
        self.assertTrue(t.bracket_generated)
        # winners round 1 has 2 matches
        round1 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=1)
        self.assertEqual(round1.matches.count(), 2)
        self.assertFalse(any(m.bye_1 for m in round1.matches.all()))
        # all rounds exist as empty shells: 2 winners rounds + 2 losers rounds
        self.assertEqual(t.winners_rounds.count(), 2)
        self.assertEqual(t.losers_rounds.count(), 2)
        # every round after round 1 is empty until advanced
        round2 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=2)
        self.assertEqual(round2.matches.count(), 0)
        losers1 = DoubleEliminationRound.objects.get(tournament=t, bracket='losers', roundnum=1)
        self.assertEqual(losers1.matches.count(), 0)

    def test_generate_bracket_8_teams_and_advance_creates_losers_round(self):
        t = self.make_tournament('EightTeamTournament', 8)
        teams = [self.make_team('E%d' % i, self.make_user('eight_u%d' % i), i * 10) for i in range(8)]
        t.teams.add(*teams)
        t.generate_bracket()
        round1 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=1)
        self.assertEqual(round1.matches.count(), 4)
        self.assertEqual(t.winners_rounds.count(), 3)
        self.assertEqual(t.losers_rounds.count(), 4)
        # complete winners round 1: team with higher index wins each match
        for i, match in enumerate(round1.matches.all().order_by('id')):
            winner = match.hometeam if match.hometeam.name == 'E%d' % (i * 2 + 1) else match.awayteam
            match.winner = winner
            match.loser = match.hometeam if match.winner != match.hometeam else match.awayteam
            match.completed = True
            match.save()
        result = t.advance_round(winners=True)
        self.assertIn('Advanced winners round 1', result)
        # winners round 2 has 2 matches with correct teams
        round2 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=2)
        self.assertEqual(round2.matches.count(), 2)
        # losers round 1 has 2 matches (losers of winners round 1 pair up)
        losers1 = DoubleEliminationRound.objects.get(tournament=t, bracket='losers', roundnum=1)
        self.assertEqual(losers1.matches.count(), 2)

    def test_generate_bracket_5_teams_in_8_size_awards_byes(self):
        t = self.make_tournament('FiveTeamTournament', 8, xp_seed=True)
        teams = [self.make_team('B%d' % i, self.make_user('five_u%d' % i), i * 10) for i in range(5)]
        t.teams.add(*teams)
        t.generate_bracket()
        round1 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=1)
        matches = list(round1.matches.all())
        # 5 teams in an 8-size bracket: 1 real match + 3 byes
        self.assertEqual(len(matches), 4)
        bye_matches = [m for m in matches if m.bye_1]
        regular_matches = [m for m in matches if not m.bye_1]
        self.assertEqual(len(bye_matches), 3)
        self.assertEqual(len(regular_matches), 1)
        # the byes go to the highest seeds (highest xp teams)
        for m in bye_matches:
            self.assertEqual(m.winner, m.awayteam)
            self.assertTrue(m.completed)
            self.assertIsNone(m.hometeam)
        # advancing winners round 1: 4 teams remain in winners round 2
        for m in regular_matches:
            m.winner = m.hometeam
            m.loser = m.awayteam
            m.completed = True
            m.save()
        result = t.advance_round(winners=True)
        self.assertIn('Advanced winners round 1', result)
        round2 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=2)
        self.assertEqual(round2.matches.count(), 2)
        # the single losers-round-1 participant gets a bye match
        losers1 = DoubleEliminationRound.objects.get(tournament=t, bracket='losers', roundnum=1)
        self.assertEqual(losers1.matches.count(), 1)
        self.assertTrue(losers1.matches.first().bye_1)

    def test_xp_seed_orders_bracket_by_xp(self):
        t = self.make_tournament('XpSeededDE', 4, xp_seed=True)
        team_high = self.make_team('HighXp', self.make_user('xp_u1'), 100)
        team_mid = self.make_team('MidXp', self.make_user('xp_u2'), 50)
        team_low = self.make_team('LowXp', self.make_user('xp_u3'), 25)
        team_none = self.make_team('NoXp', self.make_user('xp_u4'), 0)
        t.teams.add(team_high, team_mid, team_low, team_none)
        t.generate_bracket()
        entries = {e.team_id: e.seed for e in DoubleEliminationTeam.objects.filter(tournament=t)}
        self.assertEqual(entries[team_high.pk], 1)
        self.assertEqual(entries[team_mid.pk], 2)
        self.assertEqual(entries[team_low.pk], 3)
        self.assertEqual(entries[team_none.pk], 4)
        round1 = DoubleEliminationRound.objects.get(tournament=t, bracket='winners', roundnum=1)
        matches = list(round1.matches.all())
        # adjacent pairing after seeding: [0]vs[1], [2]vs[3]
        self.assertEqual(matches[0].awayteam, team_high)
        self.assertEqual(matches[0].hometeam, team_mid)
        self.assertEqual(matches[1].awayteam, team_low)
        self.assertEqual(matches[1].hometeam, team_none)

    def test_generate_bracket_refuses_to_regenerate(self):
        t = self.make_tournament('RegenTournament', 4)
        teams = [self.make_team('R%d' % i, self.make_user('regen_u%d' % i), i) for i in range(4)]
        t.teams.add(*teams)
        t.generate_bracket()
        result = t.generate_bracket()
        self.assertEqual(result, 'Bracket already generated')


class RoundAdvancementTest(DoubleEliminationTestCase):
    def setUp(self):
        super().setUp()
        self.users = []
        self.teams = []
        for i in range(4):
            user = User.objects.create_user(username='adv_u%d' % i, password='pass')
            self.users.append(user)
            team = Team.objects.create(name='AdvTeam%d' % i)
            team.founder = user
            team.save()
            team.players.add(self.player1)
            team.players.add(self.player2)
            # xp descending: AdvTeam0 has the highest xp, AdvTeam3 the lowest,
            # so the bracket pairing is deterministic
            profile = UserProfile.objects.get(user=user)
            profile.xp = 100 - (i * 25)
            profile.save()
            self.teams.append(team)
        self.tournament.size = 4
        self.tournament.xp_seed = True
        self.tournament.save()
        self.tournament.teams.add(*self.teams)
        self.tournament.generate_bracket()

    def complete_round(self, round_obj, winner_index_fn):
        for i, match in enumerate(round_obj.matches.all().order_by('id')):
            winner, loser = winner_index_fn(i, match)
            match.winner = winner
            match.loser = loser
            match.completed = True
            match.save()

    def test_winners_advance_pair_winners_in_order(self):
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        self.complete_round(round1, lambda i, m: (m.awayteam, m.hometeam))
        result = self.tournament.advance_round(winners=True)
        self.assertIn('Advanced winners round 1', result)
        round2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=2)
        self.assertEqual(round2.matches.count(), 1)
        match = round2.matches.first()
        # winners of match 1 and match 2 face each other
        self.assertIn(self.teams[0], (match.awayteam, match.hometeam))
        self.assertIn(self.teams[2], (match.awayteam, match.hometeam))
        # losers of winners round 1 pair into losers round 1
        losers1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='losers', roundnum=1)
        self.assertEqual(losers1.matches.count(), 1)
        losers_match = losers1.matches.first()
        self.assertIn(self.teams[1], (losers_match.awayteam, losers_match.hometeam))
        self.assertIn(self.teams[3], (losers_match.awayteam, losers_match.hometeam))

    def test_guard_refuses_incomplete_round(self):
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        matches = list(round1.matches.all())
        matches[0].winner = self.teams[0]
        matches[0].completed = True
        matches[0].save()
        result = self.tournament.advance_round(winners=True)
        self.assertIn('not complete', result)
        round2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=2)
        self.assertEqual(round2.matches.count(), 0)

    def test_guard_refuses_double_advance(self):
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        self.complete_round(round1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        # advancing again targets winners round 2, whose matches are not
        # completed yet
        result = self.tournament.advance_round(winners=True)
        self.assertIn('not complete', result)
        # manually pre-creating the next round's match also refuses the advance
        round2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=2)
        self.complete_round(round2, lambda i, m: (m.awayteam, m.hometeam))
        DoubleEliminationRound.objects.create(tournament=self.tournament, bracket='winners', roundnum=3)
        gf_round = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=3)
        match = self.tournament._make_match(awayteam=self.teams[0], hometeam=self.teams[1])
        match.save()
        gf_round.matches.add(match)
        result = self.tournament.advance_round(winners=True)
        self.assertIn('already been advanced', result)

    def test_full_4_team_double_elim_flow(self):
        # winners round 1: teams 0 and 2 win
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        self.complete_round(round1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        # winners round 2: team 0 wins -> winners champion
        round2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=2)
        self.complete_round(round2, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        # losers round 1: teams 1 and 3 play, team 1 wins
        losers1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='losers', roundnum=1)
        self.complete_round(losers1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=False)
        # team 3 eliminated (4th place)
        entry3 = DoubleEliminationTeam.objects.get(tournament=self.tournament, team=self.teams[3])
        self.assertTrue(entry3.eliminated)
        self.assertEqual(entry3.placement, 4)
        # losers round 2: winner of losers round 1 vs loser of winners round 2
        losers2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='losers', roundnum=2)
        self.assertEqual(losers2.matches.count(), 1)
        match = losers2.matches.first()
        self.assertIn(self.teams[1], (match.awayteam, match.hometeam))
        self.assertIn(self.teams[2], (match.awayteam, match.hometeam))
        # team 1 wins -> losers champion; team 2 eliminated (3rd place)
        self.complete_round(losers2, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=False)
        entry2 = DoubleEliminationTeam.objects.get(tournament=self.tournament, team=self.teams[2])
        self.assertTrue(entry2.eliminated)
        self.assertEqual(entry2.placement, 3)
        # grand final: winners champion (team 0) vs losers champion (team 1)
        gf = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=3)
        self.assertEqual(gf.matches.count(), 1)
        gf_match = gf.matches.first()
        self.assertIn(self.teams[0], (gf_match.awayteam, gf_match.hometeam))
        self.assertIn(self.teams[1], (gf_match.awayteam, gf_match.hometeam))
        # winners champion wins the grand final -> tournament complete
        gf_match.winner = self.teams[0]
        gf_match.loser = self.teams[1]
        gf_match.completed = True
        gf_match.save()
        result = self.tournament.advance_round(winners=True)
        self.assertIn('Tournament complete', result)
        self.assertEqual(self.tournament.winner, self.teams[0])
        self.assertEqual(self.tournament.second, self.teams[1])
        self.assertEqual(self.tournament.third, self.teams[2])
        entry0 = DoubleEliminationTeam.objects.get(tournament=self.tournament, team=self.teams[0])
        entry1 = DoubleEliminationTeam.objects.get(tournament=self.tournament, team=self.teams[1])
        self.assertEqual(entry0.placement, 1)
        self.assertEqual(entry1.placement, 2)
        self.assertTrue(entry1.eliminated)

    def test_grand_final_bracket_reset(self):
        # winners round 1: teams 0 and 2 win
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        self.complete_round(round1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        # winners round 2: team 0 wins -> winners champion
        round2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=2)
        self.complete_round(round2, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        # losers round 1: team 1 wins
        losers1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='losers', roundnum=1)
        self.complete_round(losers1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=False)
        # losers round 2: team 1 beats team 2 -> losers champion
        losers2 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='losers', roundnum=2)
        self.complete_round(losers2, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=False)
        # grand final: losers champion (team 1) wins -> bracket reset
        gf = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=3)
        gf_match = gf.matches.first()
        gf_match.winner = self.teams[1]
        gf_match.loser = self.teams[0]
        gf_match.completed = True
        gf_match.save()
        result = self.tournament.advance_round(winners=True)
        self.assertIn('Bracket reset', result)
        reset_round = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=4)
        self.assertEqual(reset_round.matches.count(), 1)
        reset_match = reset_round.matches.first()
        self.assertIn(self.teams[0], (reset_match.awayteam, reset_match.hometeam))
        self.assertIn(self.teams[1], (reset_match.awayteam, reset_match.hometeam))
        # team 1 wins the reset grand final -> champion
        reset_match.winner = self.teams[1]
        reset_match.loser = self.teams[0]
        reset_match.completed = True
        reset_match.save()
        result = self.tournament.advance_round(winners=True)
        self.assertIn('Tournament complete', result)
        self.assertEqual(self.tournament.winner, self.teams[1])
        self.assertEqual(self.tournament.second, self.teams[0])

    def test_reset_bracket(self):
        round1 = DoubleEliminationRound.objects.get(tournament=self.tournament, bracket='winners', roundnum=1)
        self.complete_round(round1, lambda i, m: (m.awayteam, m.hometeam))
        self.tournament.advance_round(winners=True)
        result = self.tournament.reset_bracket()
        self.assertIn('Bracket reset', result)
        self.assertFalse(self.tournament.bracket_generated)
        self.assertEqual(self.tournament.de_rounds.count(), 0)
        self.assertEqual(DoubleEliminationRound.objects.filter(tournament=self.tournament).count(), 0)
        entries = DoubleEliminationTeam.objects.filter(tournament=self.tournament)
        self.assertTrue(all(not e.eliminated and e.placement == 0 for e in entries))


class JoinLeaveTest(DoubleEliminationTestCase):
    def setUp(self):
        super().setUp()
        self.tournament.req_credits = 5
        self.tournament.save()
        profile = UserProfile.objects.get(user=self.founder)
        profile.credits = 20
        profile.save()

    def test_join_tournament_deducts_credits_once(self):
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.tournament.teams.filter(pk=self.team.pk).exists())
        self.assertTrue(DoubleEliminationTeam.objects.filter(team=self.team, tournament=self.tournament).exists())
        profile = UserProfile.objects.get(user=self.founder)
        self.assertEqual(profile.credits, 15)

    def test_join_rejected_when_registration_closed(self):
        self.tournament.close_register = timezone.now() - datetime.timedelta(hours=1)
        self.tournament.allow_register = False
        self.tournament.save()
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())
        profile = UserProfile.objects.get(user=self.founder)
        self.assertEqual(profile.credits, 20)

    def test_join_rejected_without_credits(self):
        profile = UserProfile.objects.get(user=self.founder)
        profile.credits = 2
        profile.save()
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())

    def test_join_rejected_when_bracket_generated(self):
        self.tournament.teams.add(self.team)
        self.tournament.bracket_generated = True
        self.tournament.save()
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DoubleEliminationTeam.objects.filter(team=self.team, tournament=self.tournament).exists())

    def test_leave_tournament_no_refund(self):
        self.tournament.teams.add(self.team)
        DoubleEliminationTeam.objects.create(team=self.team, tournament=self.tournament)
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:leave', args=[self.tournament.pk]),
                                    {'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())
        self.assertFalse(DoubleEliminationTeam.objects.filter(team=self.team, tournament=self.tournament).exists())
        # no refund of credits on leave
        profile = UserProfile.objects.get(user=self.founder)
        self.assertEqual(profile.credits, 20)

    def test_leave_rejected_when_bracket_generated(self):
        self.tournament.teams.add(self.team)
        DoubleEliminationTeam.objects.create(team=self.team, tournament=self.tournament)
        self.tournament.bracket_generated = True
        self.tournament.save()
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:leave', args=[self.tournament.pk]),
                                    {'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.tournament.teams.filter(pk=self.team.pk).exists())


class ViewTest(DoubleEliminationTestCase):
    def setUp(self):
        super().setUp()
        self.other_team = Team.objects.create(name='DEOtherTeam')
        self.other_team.founder = self.founder
        self.other_team.save()
        self.other_team.players.add(self.player1)
        self.other_team.players.add(self.player2)
        self.tournament.teams.add(self.team, self.other_team)
        DoubleEliminationTeam.objects.create(team=self.team, tournament=self.tournament)
        DoubleEliminationTeam.objects.create(team=self.other_team, tournament=self.tournament)

    def test_list_view_200(self):
        response = self.client.get(reverse('doubletournaments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test DE Tournament')

    def test_list_view_hides_inactive(self):
        self.tournament.active = False
        self.tournament.save()
        response = self.client.get(reverse('doubletournaments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test DE Tournament')

    def test_detail_view_200(self):
        response = self.client.get(reverse('doubletournaments:detail', args=[self.tournament.pk]))
        self.assertEqual(response.status_code, 200)

    def test_bracket_view_200(self):
        self.tournament.generate_bracket()
        response = self.client.get(reverse('doubletournaments:bracket', args=[self.tournament.pk]))
        self.assertEqual(response.status_code, 200)

    def test_bracket_view_before_generation_200(self):
        response = self.client.get(reverse('doubletournaments:bracket', args=[self.tournament.pk]))
        self.assertEqual(response.status_code, 200)

    def test_teams_view_200(self):
        self.client.login(username='de_founder', password='pass')
        response = self.client.get(reverse('doubletournaments:teams', args=[self.tournament.pk]))
        self.assertEqual(response.status_code, 200)

    def test_ruleset_view_200(self):
        response = self.client.get(reverse('doubletournaments:ruleset', args=[self.ruleset.pk]))
        self.assertEqual(response.status_code, 200)

    def test_join_requires_login(self):
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_join_post_flow(self):
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:join', args=[self.tournament.pk]),
                                    {'teams': self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.tournament.teams.filter(pk=self.team.pk).exists())

    def test_leave_post_flow(self):
        self.client.login(username='de_founder', password='pass')
        response = self.client.post(reverse('doubletournaments:leave', args=[self.tournament.pk]),
                                    {'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.tournament.teams.filter(pk=self.team.pk).exists())