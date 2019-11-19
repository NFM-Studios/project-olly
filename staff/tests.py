from django.test import TestCase, RequestFactory

from .views import *


class StaffBasicTest1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@nfmstudios.com', password='password')
        profile = UserProfile.objects.get(user__username=self.user.username)
        profile.user_type = 'superadmin'
        profile.save()
        static = StaticInfo()
        static.save()

    def test_indexresponse(self):
        print('Starting staff:index')
        request = self.factory.get(reverse('staff:index'))
        request.tenant = 'base'
        request.user = self.user
        response = staffindex(request)
        self.assertEqual(response.status_code, 200)
        print('Complete staff:index')

    def test_usersresponse(self):
        print('Starting staff:users')
        request = self.factory.get(reverse('staff:users'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:users')

    def test_tickets(self):
        print('Starting staff:tickets')
        request = self.factory.get(reverse('staff:tickets'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tickets')

    def test_ticket_cats(self):
        print('Starting staff:ticket_categories')
        request = self.factory.get(reverse('staff:ticket_categories'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tickets_categories')

    def test_ticket_cat_create(self):
        print('Starting staff:ticket_cat_create')
        request = self.factory.get(reverse('staff:ticket_cat_create'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:ticket_cat_create')

    def test_pages(self):
        print('Starting staff:pages')
        request = self.factory.get(reverse('staff:pages'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:pages')

    def test_tournaments(self):
        print('Starting staff:tournamentlist')
        request = self.factory.get(reverse('staff:tournamentlist'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tournamentlist')

    def test_tournament_rulesets(self):
        print('Starting staff:tournamentrulesetlist')
        request = self.factory.get(reverse('staff:tournamentrulesetlist'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:tournamentrulesetlist')

    def test_tournament_create(self):
        print('Starting staff:create_tournament')
        request = self.factory.get(reverse('staff:create_tournament'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_tournament')

    def test_matches_index(self):
        print('Starting staff:matches_index')
        request = self.factory.get(reverse('staff:matches_index'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:matches_index')

    def test_gamelist(self):
        print('Starting staff:gamelist')
        request = self.factory.get(reverse('staff:gamelist'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:gamelist')

    def test_create_gamechoice(self):
        print('Starting staff:create_gamechoice')
        request = self.factory.get(reverse('staff:create_gamechoice'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_gamechoice')

    def test_platformlist(self):
        print('Starting staff:platformlist')
        request = self.factory.get(reverse('staff:platformlist'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:platformlist')

    def test_create_platformchoice(self):
        print('Starting staff:create_platformchoice')
        request = self.factory.get(reverse('staff:create_platformchoice'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_platformchoice')

    def test_news_index(self):
        print('Starting staff:news_index')
        request = self.factory.get(reverse('staff:news_index'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:news_index')



    def test_create_article(self):
        print('Starting staff:create_article')
        request = self.factory.get(reverse('staff:create_article'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_article')

    def test_store(self):
        print('Starting staff:store')
        request = self.factory.get(reverse('staff:store'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:store')

    def test_transaction_list(self):
        print('Starting staff:transaction_list')
        request = self.factory.get(reverse('staff:transaction_list'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:transaction_list')

    def test_transfer_list(self):
        print('Starting staff:transfer_list')
        request = self.factory.get(reverse('staff:transfer_list'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:transfer_list')

    def test_product_list(self):
        print('Starting staff:product_list')
        request = self.factory.get(reverse('staff:product_list'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:product_list')

    def test_create_product(self):
        print('Starting staff:create_product')
        request = self.factory.get(reverse('staff:create_product'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:create_product')

    def test_teamindex(self):
        print('Starting staff:teamindex')
        request = self.factory.get(reverse('staff:teamindex'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:teamindex')

    def test_partner_list(self):
        print('Starting staff:partner_list')
        request = self.factory.get(reverse('staff:partner_list'))
        request.tenant = 'stock'
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)
        print('Completed staff:partner_list')

    print('Basic Staff tests have finished')
