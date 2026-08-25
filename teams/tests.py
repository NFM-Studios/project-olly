from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from .models import Team, TeamInvite
from django.contrib.auth.models import User
from pages.models import OllySetting
from .views import *
from .forms import RemovePlayerFormPost


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

    def test_teameditview(self):
        pass
        #request = self.factory.get('teams:edit', pk=self.team.id)
        #request.user = self.user
        #response = edit_team_view(request, pk=self.team.id)
        #self.assertEqual(response.status_code, 200)


class TeamInviteFlowTest(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='founder', password='pass')
        self.invitee = User.objects.create_user(username='invitee', password='pass')
        self.team = Team.objects.create(name='InviteTeam')
        self.team.founder = self.founder
        self.team.save()

    def _create_invite(self, captain=False):
        invite = TeamInvite.objects.create(team=self.team, user=self.invitee, inviter=self.founder,
                                           captain=captain, active=True, expire=timezone.now())
        return invite

    def test_accept_invite_as_player(self):
        invite = self._create_invite(captain=False)
        self.client.login(username='invitee', password='pass')
        response = self.client.post(reverse('teams:invite_detail', args=[invite.pk]), {'accepted': 'on'})
        self.assertEqual(response.status_code, 302)
        invite.refresh_from_db()
        self.assertTrue(invite.accepted)
        self.assertFalse(invite.active)
        self.assertIn(self.invitee, self.team.players.all())

    def test_accept_invite_as_captain(self):
        invite = self._create_invite(captain=True)
        self.client.login(username='invitee', password='pass')
        response = self.client.post(reverse('teams:invite_detail', args=[invite.pk]), {'accepted': 'on'})
        self.assertEqual(response.status_code, 302)
        invite.refresh_from_db()
        self.assertTrue(invite.accepted)
        self.assertIn(self.invitee, self.team.captain.all())

    def test_decline_invite(self):
        invite = self._create_invite()
        self.client.login(username='invitee', password='pass')
        response = self.client.post(reverse('teams:invite_detail', args=[invite.pk]), {'denied': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TeamInvite.objects.filter(pk=invite.pk).exists())


class TeamLeaveAndDissolveTest(TestCase):
    def setUp(self):
        OllySetting.objects.create(pk=1)
        self.founder = User.objects.create_user(username='founder', password='pass')
        self.player = User.objects.create_user(username='player', password='pass')
        self.team = Team.objects.create(name='LeaveTeam')
        self.team.founder = self.founder
        self.team.save()
        self.team.players.add(self.player)

    def test_leave_team_as_founder_no_500(self):
        self.client.login(username='founder', password='pass')
        response = self.client.post(reverse('teams:leave', args=[self.team.pk]), {'confirmed': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(pk=self.team.pk).exists())

    def test_leave_team_as_player(self):
        self.client.login(username='player', password='pass')
        response = self.client.post(reverse('teams:leave', args=[self.team.pk]), {'confirmed': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.player, self.team.players.all())

    def test_dissolve_team_no_500(self):
        self.client.login(username='founder', password='pass')
        response = self.client.post(reverse('teams:dissolve', args=[self.team.pk]), {'confirmed': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())


class TeamTotalXpTest(TestCase):
    def setUp(self):
        self.founder = User.objects.create_user(username='xp_founder', password='pass')
        self.team = Team.objects.create(name='XpTeam')
        self.team.founder = self.founder
        self.team.save()

    def _create_invite(self, user):
        return TeamInvite.objects.create(
            team=self.team, user=user, inviter=self.founder,
            captain=False, active=True, expire=timezone.now(),
        )

    def test_get_total_xp_sums_invited_users_xp(self):
        user1 = User.objects.create_user(username='xp_user1', password='pass')
        user2 = User.objects.create_user(username='xp_user2', password='pass')
        profile1 = user1.user
        profile2 = user2.user
        profile1.xp = 50
        profile2.xp = 30
        profile1.save()
        profile2.save()
        self._create_invite(user1)
        self._create_invite(user2)

        self.team.get_total_xp()

        self.assertEqual(self.team.totalxp, 80)

    def test_get_total_xp_with_no_invites_is_zero(self):
        self.team.totalxp = 999
        self.team.save()
        self.team.get_total_xp()
        self.assertEqual(self.team.totalxp, 0)

    def test_get_rank_assigns_rank_field(self):
        higher = Team.objects.create(name='HigherXp')
        higher.totalxp = 200
        higher.save()
        self.team.totalxp = 100
        self.team.save()

        self.team.get_rank()

        self.assertEqual(self.team.rank, 2)