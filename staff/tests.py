from django.test import TestCase, RequestFactory

from .views import *


class StaffBasicTest1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@nfmstudios.com', password='password')
        profile = UserProfile.objects.get(user__username=self.user.username)
        profile.user_type = 'superadmin'
        profile.save()

    def test_indexresponse(self):
        print('Starting staff:index')
        request = self.factory.get(reverse('staff:index'))
        request.tenant = 'eot'
        request.user = self.user
        response = staffindex(request)
        self.assertEqual(response.status_code, 200)
        print('Complete staff:index')

    def test_usersresponse(self):
        print('Starting staff:users')
        request = self.factory.get(reverse('staff:users'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:users')

    def test_tickets(self):
        print('Starting staff:tickets')
        request = self.factory.get(reverse('staff:tickets'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tickets')

    def test_ticket_cats(self):
        print('Starting staff:ticket_categories')
        request = self.factory.get(reverse('staff:ticket_categories'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tickets_categories')

    def test_ticket_cat_create(self):
        print('Starting staff:ticket_cat_create')
        request = self.factory.get(reverse('staff:ticket_cat_create'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:ticket_cat_create')

    def test_pages(self):
        print('Starting staff:pages')
        request = self.factory.get(reverse('staff:pages'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:pages')

    def test_tournaments(self):
        print('Starting staff:tournamentlist')
        request = self.factory.get(reverse('staff:tournamentlist'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tournamentlist')

    def test_tournament_rulesets(self):
        print('Starting staff:tournamentrulesetlist')
        request = self.factory.get(reverse('staff:tournamentrulesetlist'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tournamentrulesetlist')

    def test_tournament_create(self):
        print('Starting staff:create_tournament')
        request = self.factory.get(reverse('staff:create_tournament'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_tournament')

    def test_matches_index(self):
        print('Starting staff:matches_index')
        request = self.factory.get(reverse('staff:matches_index'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:matches_index')

    def test_gamelist(self):
        print('Starting staff:gamelist')
        request = self.factory.get(reverse('staff:gamelist'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:gamelist')

    def test_create_gamechoice(self):
        print('Starting staff:create_gamechoice')
        request = self.factory.get(reverse('staff:create_gamechoice'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_gamechoice')

    def test_platformlist(self):
        print('Starting staff:platformlist')
        request = self.factory.get(reverse('staff:platformlist'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:platformlist')

    def test_create_platformchoice(self):
        print('Starting staff:create_platformchoice')
        request = self.factory.get(reverse('staff:create_platformchoice'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_platformchoice')

    def test_news_index(self):
        print('Starting staff:news_index')
        request = self.factory.get(reverse('staff:news_index'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:news_index')

    def test_news_list(self):
        print('Starting staff:news_list')
        request = self.factory.get(reverse('staff:news_list'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:news_list')

    def test_create_article(self):
        print('Starting staff:create_article')
        request = self.factory.get(reverse('staff:create_article'))
        request.tenant = 'eot'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_article')

    

    print('Basic Staff tests have finished')
