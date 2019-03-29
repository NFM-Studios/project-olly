from django.test import TestCase, RequestFactory
from .views import *
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

