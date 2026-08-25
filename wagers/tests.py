from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from teams.models import Team
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