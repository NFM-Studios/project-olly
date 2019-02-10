from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from .views import *


class PostTestCase1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='password')
        # login = self.client.login(username='testuser', password='password')
        # post1 = Post.objects.create(title='Test Title', slug='Test_Slug', body='Testing Body Field')

    def test_listresponse(self):
        request = self.factory.get('/news')

        request.tenant = 'eot'

        request.user = self.user

        response = post_list(request)

        self.assertEqual(response.status_code, 200)

    def test_detailresponse(self):
        post1 = Post.objects.create(title='Test Title', slug='Test_Slug', body='Testing Body Field', status="published",
                                    author=self.user)

        request = self.factory.get('/news/'+post1.slug)

        request.tenant = 'eot'

        request.user = self.user

        detailresponse = post_detail(request, post1.slug)
        self.assertEqual(detailresponse.status_code, 200)

    def test_detail2response(self):
        post1 = Post.objects.create(title='Test Title2', slug='Test_Slug22', body='Testing Body Field',
                                    status="published", author=self.user)

        request = self.factory.get('/news/'+post1.slug)

        request.tenant = 'binge'

        detailresponse = post_detail(request, post1.slug)
        self.assertEqual(detailresponse.status_code, 200)

    def test_list2response(self):
        request = self.factory.get('/news')

        request.tenant = 'binge'

        request.user = self.user

        response = post_list(request)

        self.assertEqual(response.status_code, 200)

