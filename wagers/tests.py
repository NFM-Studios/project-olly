from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
import datetime

from matches.models import GameChoice, PlatformChoice
from profiles.models import UserProfile
from teams.models import Team
from wagers.models import WagerMatch, WagerRequest
from wagers.views import MyWagersList


class MyWagersListTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='wageruser', password='pass')

    def test_my_wagers_list_renders(self):
        # regression: MyWagersList used an undefined 'final' variable and crashed
        team = Team.objects.create(name='WagerTeam')
        team.founder = self.user
        team.save()
        request = self.factory.get('/wagers/mine/')
        request.user = self.user
        response = MyWagersList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_my_wagers_list_renders_with_old_requests(self):
        # regression: old_results = old_requests + x raised TypeError on active requests
        from wagers.models import WagerRequest
        from matches.models import GameChoice, PlatformChoice

        team = Team.objects.create(name='WagerTeam2')
        team.founder = self.user
        team.save()
        game = GameChoice.objects.create(name='CSGO')
        platform = PlatformChoice.objects.create(name='PC')
        WagerRequest.objects.create(team=team, creator=self.user, game=game, platform=platform,
                                    bestof=1, teamformat=1, expired=True)
        request = self.factory.get('/wagers/mine/')
        request.user = self.user
        response = MyWagersList.as_view()(request)
        self.assertEqual(response.status_code, 200)
class WagerChallengeLifecycleTest(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username='wager_creator', password='pass')
        self.challenger = User.objects.create_user(username='wager_challenger', password='pass')
        self.game = GameChoice.objects.create(name='CSGO')
        self.platform = PlatformChoice.objects.create(name='PC')
        self.creator_team = Team.objects.create(name='CreatorTeam')
        self.creator_team.founder = self.creator
        self.creator_team.save()
        self.challenger_team = Team.objects.create(name='ChallengerTeam')
        self.challenger_team.founder = self.challenger
        self.challenger_team.save()
        # use update() so no stale profile instance gets cached on the user
        UserProfile.objects.filter(user=self.creator).update(credits=200)
        UserProfile.objects.filter(user=self.challenger).update(credits=200)
        self.myrequest = WagerRequest.objects.create(
            team=self.creator_team, creator=self.creator, credits=50,
            game=self.game, platform=self.platform, bestof=1, teamformat=0,
            expiration=timezone.now() + datetime.timedelta(minutes=30))

    def test_challenge_acceptance_creates_wager_match_and_debits_credits(self):
        self.client.login(username='wager_challenger', password='pass')
        response = self.client.post(reverse('wagers:challenge_create', args=[self.myrequest.pk]),
                                    {'team': self.challenger_team.pk, 'info': 'Lets go', 'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.myrequest.refresh_from_db()
        self.assertTrue(self.myrequest.challenge_accepted)
        self.assertIsNotNone(self.myrequest.challenge)
        self.assertTrue(self.myrequest.challenge.confirm)
        wmatch = self.myrequest.wmatch
        self.assertIsNotNone(wmatch)
        self.assertEqual(wmatch.credits, 50)
        match = wmatch.match
        self.assertEqual(match.type, 'w')
        self.assertEqual(match.hometeam, self.creator_team)
        self.assertEqual(match.awayteam, self.challenger_team)
        self.assertEqual(match.game, self.game)
        self.assertEqual(match.platform, self.platform)
        self.assertEqual(match.bestof, 1)
        self.assertEqual(match.teamformat, 0)
        # both sides stake their credits (fresh queries avoid stale reverse-cache)
        self.assertEqual(UserProfile.objects.get(user=self.creator).credits, 150)
        self.assertEqual(UserProfile.objects.get(user=self.challenger).credits, 150)

    def test_expired_request_rejected(self):
        self.myrequest.expired = True
        self.myrequest.save()
        self.client.login(username='wager_challenger', password='pass')
        response = self.client.post(reverse('wagers:challenge_create', args=[self.myrequest.pk]),
                                    {'team': self.challenger_team.pk, 'info': 'Lets go', 'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WagerMatch.objects.filter(credits=50).exists())
        self.myrequest.refresh_from_db()
        self.assertFalse(self.myrequest.challenge_accepted)

    def test_accepted_request_rejected(self):
        self.myrequest.challenge_accepted = True
        self.myrequest.save()
        self.client.login(username='wager_challenger', password='pass')
        response = self.client.post(reverse('wagers:challenge_create', args=[self.myrequest.pk]),
                                    {'team': self.challenger_team.pk, 'info': 'Lets go', 'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WagerMatch.objects.filter(credits=50).exists())

    def test_challenge_insufficient_credits_rejected(self):
        self.challenger.user.credits = 10
        self.challenger.user.save()
        self.client.login(username='wager_challenger', password='pass')
        response = self.client.post(reverse('wagers:challenge_create', args=[self.myrequest.pk]),
                                    {'team': self.challenger_team.pk, 'info': 'Lets go', 'confirm': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WagerMatch.objects.filter(credits=50).exists())
        self.myrequest.refresh_from_db()
        self.assertFalse(self.myrequest.challenge_accepted)
