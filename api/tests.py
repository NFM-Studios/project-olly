from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from leagues.models import League, LeagueSettings, LeagueTeam
from matches.models import GameChoice, MapChoice, MapPoolChoice, Match, PlatformChoice
from news.models import Comment, Post
from profiles.models import Notification, UserProfile
from singletournaments.models import SingleEliminationTournament, SingleTournamentRound, \
    SingleTournamentRuleset
from teams.models import Team
from wagers.models import WagerRequest


class ApiTestCaseBase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='player1', password='pass')
        self.user2 = User.objects.create_user(username='player2', password='pass')
        self.staff = User.objects.create_user(username='staff', password='pass')
        staff_profile = UserProfile.objects.get(user=self.staff)
        staff_profile.user_type = 'admin'
        staff_profile.save()

    def force_auth(self, user=None):
        self.client.force_authenticate(user=user or self.user)
        return self.client


class TeamApiTests(ApiTestCaseBase):
    def test_anonymous_can_list_teams(self):
        Team.objects.create(name='Anonymous Team')
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_team(self):
        response = self.client.post('/api/teams/', {'name': 'Blocked Team'})
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN,
                                             status.HTTP_401_UNAUTHORIZED))

    def test_authenticated_can_create_team(self):
        self.force_auth()
        response = self.client.post('/api/teams/', {'name': 'Brand New Team'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        team = Team.objects.get(id=response.data['id'])
        self.assertEqual(team.founder, self.user)
        profile = UserProfile.objects.get(user=self.user)
        self.assertIn(team, profile.founder_teams.all())

    def test_team_name_too_short_rejected(self):
        self.force_auth()
        response = self.client.post('/api/teams/', {'name': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_team_update_denied_for_stranger(self):
        team = Team.objects.create(name='Owned Team')
        team.founder = self.user2
        team.save()
        self.force_auth()
        response = self.client.patch('/api/teams/%d/' % team.id, {'tag': 'OWN'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_update_allowed_for_founder(self):
        team = Team.objects.create(name='Owned Team')
        team.founder = self.user
        team.save()
        self.force_auth()
        response = self.client.patch('/api/teams/%d/' % team.id, {'tag': 'OWN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team.refresh_from_db()
        self.assertEqual(team.tag, 'OWN')

    def test_team_players_endpoint(self):
        team = Team.objects.create(name='Roster Team')
        team.founder = self.user
        team.players.add(self.user, self.user2)
        team.save()
        response = self.client.get('/api/teams/%d/players/' % team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = {player['username'] for player in response.data}
        self.assertEqual(usernames, {'player1', 'player2'})

    def test_team_name_filter_icontains(self):
        Team.objects.create(name='Alpha Squad')
        Team.objects.create(name='Beta Squad')
        response = self.client.get('/api/teams/', {'name': 'alpha'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Alpha Squad')

    def test_pagination_honors_page_size(self):
        for i in range(120):
            Team.objects.create(name='Paginated Team %d' % i)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 120)
        self.assertEqual(len(response.data['results']), 20)
        response = self.client.get('/api/teams/', {'page_size': 25})
        self.assertEqual(len(response.data['results']), 25)
        response = self.client.get('/api/teams/', {'page_size': 200})
        self.assertEqual(len(response.data['results']), 100)


class MeApiTests(ApiTestCaseBase):
    def test_me_requires_auth(self):
        response = self.client.get('/api/me/')
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN,
                                             status.HTTP_401_UNAUTHORIZED))

    def test_me_returns_own_profile(self):
        self.force_auth()
        profile = UserProfile.objects.get(user=self.user)
        profile.alternate_name = 'The Original'
        profile.save()
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'player1')
        self.assertEqual(response.data['profile']['alternate_name'], 'The Original')
        self.assertEqual(response.data['email'], self.user.email)

    def test_me_patch_updates_alternate_name(self):
        self.force_auth()
        response = self.client.patch('/api/me/', {'alternate_name': 'Renamed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.alternate_name, 'Renamed')

    def test_me_patch_cannot_escalate_credits(self):
        self.force_auth()
        response = self.client.patch('/api/me/', {'credits': 9999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.credits, 0)

    def test_token_authentication(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'player1')

    def test_me_notifications_list_and_mark_read(self):
        self.force_auth()
        notification = Notification.objects.create(title='Hello', link='/',
                                                   description='A notification')
        UserProfile.objects.get(user=self.user).notifications.add(notification)
        response = self.client.get('/api/me/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertFalse(response.data['results'][0]['read'])
        response = self.client.post('/api/me/notifications/', {'id': notification.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.read)

    def test_me_notifications_reject_foreign_notification(self):
        self.force_auth()
        notification = Notification.objects.create(title='Foreign', link='/')
        UserProfile.objects.get(user=self.user2).notifications.add(notification)
        response = self.client.post('/api/me/notifications/', {'id': notification.id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NewsApiTests(ApiTestCaseBase):
    def setUp(self):
        super().setUp()
        self.published = Post.objects.create(title='Published Post',
                                             slug='published-post', author=self.user,
                                             body='Public body', status='published')
        self.draft = Post.objects.create(title='Draft Post', slug='draft-post',
                                         author=self.user, body='Secret body',
                                         status='draft')

    def test_anonymous_only_sees_published_posts(self):
        response = self.client.get('/api/news/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [post['slug'] for post in response.data['results']]
        self.assertIn('published-post', slugs)
        self.assertNotIn('draft-post', slugs)

    def test_staff_sees_all_posts(self):
        self.force_auth(self.staff)
        response = self.client.get('/api/news/posts/')
        slugs = [post['slug'] for post in response.data['results']]
        self.assertIn('published-post', slugs)
        self.assertIn('draft-post', slugs)

    def test_regular_user_does_not_see_drafts(self):
        self.force_auth()
        response = self.client.get('/api/news/posts/')
        slugs = [post['slug'] for post in response.data['results']]
        self.assertNotIn('draft-post', slugs)

    def test_staff_can_create_post(self):
        self.force_auth(self.staff)
        response = self.client.post('/api/news/posts/',
                                    {'title': 'Staff Post', 'slug': 'staff-post',
                                     'body': 'Staff body', 'status': 'published'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['username'], 'staff')

    def test_regular_user_cannot_create_post(self):
        self.force_auth()
        response = self.client.post('/api/news/posts/',
                                    {'title': 'Nope', 'slug': 'nope', 'body': 'x'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comments_public_get_authenticated_post(self):
        response = self.client.get('/api/news/posts/%d/comments/' % self.published.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        self.force_auth()
        response = self.client.post('/api/news/posts/%d/comments/' % self.published.id,
                                    {'body': 'Nice article', 'name': 'Commenter'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('email', response.data)
        self.assertEqual(Comment.objects.filter(post=self.published).count(), 1)
        response = self.client.get('/api/news/posts/%d/comments/' % self.published.id)
        self.assertEqual(len(response.data), 1)

    def test_anonymous_cannot_post_comment(self):
        response = self.client.post('/api/news/posts/%d/comments/' % self.published.id,
                                    {'body': 'Nope'})
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN,
                                             status.HTTP_401_UNAUTHORIZED))


class MatchApiTests(ApiTestCaseBase):
    def setUp(self):
        super().setUp()
        self.hometeam = Team.objects.create(name='Home Squad')
        self.hometeam.founder = self.user
        self.hometeam.captain.add(self.user)
        self.hometeam.save()
        self.awayteam = Team.objects.create(name='Away Squad')
        self.awayteam.founder = self.user2
        self.awayteam.save()
        self.match = Match.objects.create(hometeam=self.hometeam,
                                          awayteam=self.awayteam)

    def test_anonymous_can_read_match(self):
        response = self.client.get('/api/matches/%d/' % self.match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['hometeam']['name'], 'Home Squad')

    def test_match_write_denied_for_non_participant(self):
        stranger = User.objects.create_user(username='stranger', password='pass')
        self.force_auth(stranger)
        response = self.client.patch('/api/matches/%d/' % self.match.id,
                                     {'info': 'hacked'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_match_write_allowed_for_hometeam_captain(self):
        self.force_auth(self.user)
        response = self.client.patch('/api/matches/%d/' % self.match.id,
                                     {'info': 'New match info'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match.refresh_from_db()
        self.assertEqual(self.match.info, 'New match info')

    def test_match_write_allowed_for_awayteam_founder(self):
        self.force_auth(self.user2)
        response = self.client.patch('/api/matches/%d/' % self.match.id,
                                     {'server': 'eu-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.match.refresh_from_db()
        self.assertEqual(self.match.server, 'eu-1')

    def test_match_create_denied_for_non_staff(self):
        self.force_auth()
        response = self.client.post('/api/matches/', {'matchnum': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_match_create_allowed_for_staff(self):
        self.force_auth(self.staff)
        response = self.client.post('/api/matches/', {'matchnum': 1,
                                                      'hometeam': self.hometeam.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['hometeam']['id'], self.hometeam.id)

    def test_match_filtering(self):
        game = GameChoice.objects.create(name='Counter-Strike')
        done = Match.objects.create(hometeam=self.hometeam,
                                    awayteam=self.awayteam, game=game,
                                    completed=True)
        response = self.client.get('/api/matches/', {'completed': 'true'})
        ids = {match['id'] for match in response.data['results']}
        self.assertEqual(ids, {done.id})
        response = self.client.get('/api/matches/', {'hometeam': self.hometeam.id})
        ids = {match['id'] for match in response.data['results']}
        self.assertEqual(ids, {self.match.id, done.id})


class TournamentApiTests(ApiTestCaseBase):
    def setUp(self):
        super().setUp()
        now = timezone.now()
        self.tournament = SingleEliminationTournament.objects.create(
            name='Champions Cup', open_register=now, close_register=now + timedelta(days=7),
            start=now + timedelta(days=14), active=True, size=8)
        self.team = Team.objects.create(name='Cup Team')
        self.tournament.teams.add(self.team)
        self.round = SingleTournamentRound.objects.create(tournament=self.tournament,
                                                          roundnum=1)

    def test_tournament_list_and_filter(self):
        response = self.client.get('/api/tournaments/', {'active': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['teams'][0]['name'], 'Cup Team')

    def test_tournament_write_denied_for_regular_user(self):
        self.force_auth()
        response = self.client.patch('/api/tournaments/%d/' % self.tournament.id,
                                     {'active': False})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tournament_rounds_endpoint(self):
        match = Match.objects.create(hometeam=self.team)
        self.round.matches.add(match)
        response = self.client.get('/api/tournaments/%d/rounds/' % self.tournament.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['roundnum'], 1)
        self.assertEqual(len(response.data[0]['matches']), 1)


class LeagueApiTests(ApiTestCaseBase):
    def setUp(self):
        super().setUp()
        now = timezone.now()
        self.settings = LeagueSettings.objects.create(name='League Settings')
        self.ruleset = SingleTournamentRuleset.objects.create(name='League Rules',
                                                              text='rules')
        self.league = League.objects.create(name='Pro League', settings=self.settings,
                                            ruleset=self.ruleset,
                                            open_register=now,
                                            close_register=now + timedelta(days=7),
                                            start=now + timedelta(days=14),
                                            active=True)
        self.team_a = Team.objects.create(name='League Team A')
        self.team_b = Team.objects.create(name='League Team B')
        self.league_team_a = LeagueTeam.objects.create(team=self.team_a, points=10)
        self.league_team_b = LeagueTeam.objects.create(team=self.team_b, points=5)
        self.league.teams.add(self.league_team_a, self.league_team_b)

    def test_league_detail_includes_ordered_standings(self):
        response = self.client.get('/api/leagues/%d/' % self.league.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        standings = response.data['standings']
        self.assertEqual(len(standings), 2)
        self.assertEqual(standings[0]['points'], 10)
        self.assertEqual(standings[1]['points'], 5)

    def test_league_filter(self):
        response = self.client.get('/api/leagues/', {'active': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class ReferenceDataApiTests(ApiTestCaseBase):
    def test_games_platforms_map_pools(self):
        game = GameChoice.objects.create(name='Rocket League')
        platform = PlatformChoice.objects.create(name='PC')
        mappool = MapPoolChoice.objects.create(name='Season Pool', game=game)
        mappool.maps.add(MapChoice.objects.create(name='DFH Stadium', game=game))
        response = self.client.get('/api/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Rocket League')
        response = self.client.get('/api/platforms/')
        self.assertEqual(response.data['results'][0]['name'], 'PC')
        response = self.client.get('/api/map-pools/')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['maps'][0]['name'],
                         'DFH Stadium')


class WagerApiTests(ApiTestCaseBase):
    def setUp(self):
        super().setUp()
        self.team = Team.objects.create(name='Wager Team')
        self.team.founder = self.user
        self.team.save()
        self.game = GameChoice.objects.create(name='Wager Game')
        self.platform = PlatformChoice.objects.create(name='Wager Platform')

    def test_wager_request_public_list_authenticated_post(self):
        self.force_auth()
        response = self.client.post('/api/wagers/requests/',
                                    {'team': self.team.id, 'game': self.game.id,
                                     'platform': self.platform.id, 'credits': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['creator'], self.user.id)
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/wagers/requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_wager_request_anonymous_post_denied(self):
        response = self.client.post('/api/wagers/requests/',
                                    {'team': self.team.id, 'game': self.game.id,
                                     'platform': self.platform.id})
        self.assertIn(response.status_code, (status.HTTP_403_FORBIDDEN,
                                             status.HTTP_401_UNAUTHORIZED))


class ApiRootAndDocsTests(ApiTestCaseBase):
    def test_api_root_and_docs(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('openapi', response.data)