from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from matches.models import Match, MatchCheckIn, MatchDispute, MatchReport
from matches.templatetags.olly_extras import bestof, js_datetime, js_string, teamformat
from matches.views import create_checkin
from teams.models import Team


class MatchReportCreateViewTest(TestCase):
    def setUp(self):
        self.founder1 = User.objects.create_user(username='founder1', password='pass')
        self.captain1 = User.objects.create_user(username='captain1', password='pass')
        self.founder2 = User.objects.create_user(username='founder2', password='pass')
        self.team1 = Team.objects.create(name='Team1')
        self.team1.founder = self.founder1
        self.team1.save()
        self.team1.captain.add(self.captain1)
        self.team2 = Team.objects.create(name='Team2')
        self.team2.founder = self.founder2
        self.team2.save()
        self.match = Match.objects.create(hometeam=self.team1, awayteam=self.team2,
                                          disable_userreport=False)

    def test_report_happy_path_for_captain(self):
        self.client.login(username='captain1', password='pass')
        response = self.client.post(reverse('matches:report', args=[self.match.pk]),
                                    {'match': self.match.pk, 'reported_winner': self.team1.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MatchReport.objects.filter(match=self.match, reporting_team=self.team1).exists())
        self.match.refresh_from_db()
        self.assertTrue(self.match.team1reported)
        self.assertEqual(self.match.team1reportedwinner, self.team1)

    def test_report_winner_restricted_to_match_teams(self):
        # a team that is not part of this match cannot be reported as the winner
        other_team = Team.objects.create(name='Other Team')
        self.client.login(username='captain1', password='pass')
        response = self.client.post(reverse('matches:report', args=[self.match.pk]),
                                    {'match': self.match.pk, 'reported_winner': other_team.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchReport.objects.filter(match=self.match).exists())
        self.match.refresh_from_db()
        self.assertFalse(self.match.team1reported)

    def test_report_invalid_form_rejected(self):
        self.client.login(username='captain1', password='pass')
        response = self.client.post(reverse('matches:report', args=[self.match.pk]), {})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchReport.objects.filter(match=self.match).exists())


class JsDatetimeFilterTest(TestCase):
    def test_formats_datetime_as_iso8601(self):
        self.assertEqual(js_datetime(datetime(2021, 1, 15, 12, 0, 0)), '2021-01-15T12:00:00')

    def test_formats_aware_datetime_with_offset(self):
        value = datetime(2021, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(js_datetime(value), '2021-01-15T12:00:00+00:00')

    def test_none_renders_empty(self):
        self.assertEqual(js_datetime(None), '')

    def test_escapes_unsafe_characters(self):
        self.assertEqual(js_datetime('"><script>alert(1)</script>'),
                         '\\u0022\\u003E\\u003Cscript\\u003Ealert(1)\\u003C/script\\u003E')


class JsStringFilterTest(TestCase):
    def test_escapes_unsafe_characters(self):
        self.assertEqual(js_string('"><script>alert(1)</script>'),
                         '\\u0022\\u003E\\u003Cscript\\u003Ealert(1)\\u003C/script\\u003E')

    def test_none_renders_empty(self):
        self.assertEqual(js_string(None), '')


class TeamformatFilterTest(TestCase):
    def test_maps_all_known_values(self):
        expected = {0: '1v1', 1: '2v2', 2: '3v3', 3: '4v4', 4: '5v5', 5: '6v6'}
        for value, label in expected.items():
            self.assertEqual(teamformat(value), label)

    def test_unknown_values(self):
        self.assertEqual(teamformat(99), 'Unknown')
        self.assertEqual(teamformat(None), 'Unknown')
        self.assertEqual(teamformat('not a number'), 'Unknown')


class BestofFilterTest(TestCase):
    def test_maps_all_known_values(self):
        expected = {1: 'Best of 1', 2: 'Best of 2', 3: 'Best of 3', 4: 'Best of 4', 5: 'Best of 5'}
        for value, label in expected.items():
            self.assertEqual(bestof(value), label)

    def test_unknown_values(self):
        self.assertEqual(bestof(99), 'Unknown')
        self.assertEqual(bestof(None), 'Unknown')
        self.assertEqual(bestof('not a number'), 'Unknown')
class MatchIndexSmokeTest(TestCase):
    def test_meta_indexes_defined(self):
        names = {index.name for index in Match._meta.indexes}
        self.assertIn('match_datetime_idx', names)
        self.assertIn('match_completed_idx', names)
        self.assertIn('match_teams_idx', names)

    def test_match_creation_with_indexes(self):
        match = Match.objects.create(type='w')
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(Match.objects.filter(pk=match.pk).count(), 1)


def _attach_messages(request):
    SessionMiddleware(lambda r: None).process_request(request)
    request.session.save()
    MessageMiddleware(lambda r: None).process_request(request)


class CheckInEnforcementTest(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='checkin_founder', password='pass')
        self.player = User.objects.create_user(username='checkin_player', password='pass')
        self.other = User.objects.create_user(username='checkin_other', password='pass')
        self.team = Team.objects.create(name='CheckinTeam')
        self.team.founder = self.founder
        self.team.save()
        self.team.players.add(self.player)
        # teamformat 0 = 1v1, minimum checkin size is 1
        self.match = Match.objects.create(hometeam=self.team, awayteam=None,
                                          teamformat=0, disable_userreport=False)

    def test_team_checkin_enforces_min_team_size(self):
        self.client.login(username='checkin_founder', password='pass')
        response = self.client.post(reverse('matches:team_checkin', args=[self.match.pk, self.team.pk]), {})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchCheckIn.objects.filter(match=self.match).exists())

    def test_create_checkin_enforces_min_team_size(self):
        self.client.login(username='checkin_founder', password='pass')
        request = RequestFactory().post(reverse('matches:detail', args=[self.match.pk]))
        request.user = self.founder
        _attach_messages(request)
        response = create_checkin(request, self.match.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchCheckIn.objects.filter(match=self.match).exists())

    def test_create_checkin_rejects_non_member(self):
        self.client.login(username='checkin_founder', password='pass')
        request = RequestFactory().post(reverse('matches:detail', args=[self.match.pk]),
                                        {'players': [self.other.pk]})
        request.user = self.founder
        _attach_messages(request)
        response = create_checkin(request, self.match.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchCheckIn.objects.filter(match=self.match).exists())

    def test_create_checkin_valid_flow(self):
        self.client.login(username='checkin_founder', password='pass')
        request = RequestFactory().post(reverse('matches:detail', args=[self.match.pk]),
                                        {'players': [self.founder.pk, self.player.pk]})
        request.user = self.founder
        _attach_messages(request)
        response = create_checkin(request, self.match.pk)
        self.assertEqual(response.status_code, 302)
        checkin = MatchCheckIn.objects.get(match=self.match)
        self.assertEqual(checkin.team, self.team)
        self.assertEqual(checkin.reporter, self.founder)
        self.assertEqual(checkin.players.count(), 2)

    def test_create_checkin_requires_captain_or_founder(self):
        self.client.login(username='checkin_other', password='pass')
        request = RequestFactory().post(reverse('matches:detail', args=[self.match.pk]),
                                        {'players': [self.other.pk]})
        request.user = self.other
        _attach_messages(request)
        response = create_checkin(request, self.match.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchCheckIn.objects.filter(match=self.match).exists())


class MatchDisputeFlowTest(TestCase):
    def setUp(self):
        self.captain1 = User.objects.create_user(username='dispute_cap1', password='pass')
        self.founder1 = User.objects.create_user(username='dispute_founder1', password='pass')
        self.captain2 = User.objects.create_user(username='dispute_cap2', password='pass')
        self.founder2 = User.objects.create_user(username='dispute_founder2', password='pass')
        self.team1 = Team.objects.create(name='DisputeTeam1')
        self.team1.founder = self.founder1
        self.team1.save()
        self.team1.captain.add(self.captain1)
        self.team2 = Team.objects.create(name='DisputeTeam2')
        self.team2.founder = self.founder2
        self.team2.save()
        self.team2.captain.add(self.captain2)
        self.match = Match.objects.create(hometeam=self.team1, awayteam=self.team2,
                                          disable_userreport=False)

    def test_conflicting_reports_create_dispute(self):
        self.client.login(username='dispute_cap1', password='pass')
        self.client.post(reverse('matches:report', args=[self.match.pk]),
                         {'match': self.match.pk, 'reported_winner': self.team1.pk})
        self.client.login(username='dispute_cap2', password='pass')
        response = self.client.post(reverse('matches:report', args=[self.match.pk]),
                                    {'match': self.match.pk, 'reported_winner': self.team2.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MatchDispute.objects.filter(match=self.match).exists())
        self.match.refresh_from_db()
        self.assertTrue(self.match.disputed)
        self.assertIsNone(self.match.winner)

    def test_agreeing_reports_declare_winner_without_dispute(self):
        self.client.login(username='dispute_cap1', password='pass')
        self.client.post(reverse('matches:report', args=[self.match.pk]),
                         {'match': self.match.pk, 'reported_winner': self.team1.pk})
        self.client.login(username='dispute_cap2', password='pass')
        response = self.client.post(reverse('matches:report', args=[self.match.pk]),
                                    {'match': self.match.pk, 'reported_winner': self.team1.pk})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MatchDispute.objects.filter(match=self.match).exists())
        self.match.refresh_from_db()
        self.assertEqual(self.match.winner, self.team1)
        self.assertEqual(self.match.loser, self.team2)
