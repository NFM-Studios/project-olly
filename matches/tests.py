from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from matches.models import Match, MatchReport
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