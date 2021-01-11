from django.test import TestCase, RequestFactory
from .models import Team
from django.contrib.auth.models import User
from .views import *


class TeamTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="blank")
        self.team = Team.objects.create(name="Team1")
        self.team.founder = self.user
        self.factory = RequestFactory()

    def test_founder(self):
        self.assertEqual(self.team.founder, self.user)

    def test_player(self):
        user2 = User.objects.create(username="player1", password="blank")
        self.team.players.add(user2)
        self.team.save()
        self.assertIn(user2, self.team.players.all())

    def test_2players(self):
        user2 = User.objects.create(username="player1", password="blank")
        user3 = User.objects.create(username="player2", password="blank")
        self.team.players.add(user2)
        self.team.players.add(user3)
        self.team.save()
        self.assertIn(user2, self.team.players.all())
        self.assertIn(user3, self.team.players.all())

    def test_removeplayer(self):
        user2 = User.objects.create(username="player1", password="blank")
        self.team.players.add(user2)
        self.team.save()
        self.assertIn(user2, self.team.players.all())
        self.team.players.remove(user2)
        self.assertNotIn(user2, self.team.players.all())

    def test_remove2players(self):
        user2 = User.objects.create(username="player1", password="blank")
        user3 = User.objects.create(username="player2", password="blank")
        self.team.players.add(user2)
        self.team.players.add(user3)
        self.team.save()
        self.assertIn(user2, self.team.players.all())
        self.assertIn(user3, self.team.players.all())
        self.team.players.remove(user2)
        self.team.players.remove(user3)
        self.assertNotIn(user2, self.team.players.all())
        self.assertNotIn(user3, self.team.players.all())

    def test_teamdetailview(self):
        request = self.factory.get('teams:detail', pk=self.team.id)
        request.user = self.user
        response = MyTeamDetailView.get(None, request, pk=self.team.id)
        self.assertEqual(response.status_code, 200)
