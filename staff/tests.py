from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from profiles.models import *
from .views import *

class StaffBasicTest1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@nfmstudios.com', password='password')
        profile = UserProfile.objects.get(user__username=self.user.username)
        profile.user_type = 'superadmin'
        profile.save()

    def test_indexresponse(self):
        request = self.factory.get('/staff')
        request.tenant = 'eot'
        request.user = self.user
        response = staffindex(request)
        self.assertEqual(response.status_code, 200)