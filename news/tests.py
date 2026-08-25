from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from .models import Comment, Post
from .views import *


class PostTestCase1(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='password')
        # login = self.client.login(username='testuser', password='password')
        # post1 = Post.objects.create(title='Test Title', slug='Test_Slug', body='Testing Body Field')

    def test_listresponse(self):
        request = self.factory.get('/news')

        request.user = self.user

        response = post_list(request)

        self.assertEqual(response.status_code, 200)

    def test_detailresponse(self):
        post1 = Post.objects.create(title='Test Title', slug='Test_Slug', body='Testing Body Field', status="published",
                                    author=self.user)

        request = self.factory.get('/news/' + post1.slug)

        request.user = self.user

        detailresponse = post_detail(request, post1.slug)
        self.assertEqual(detailresponse.status_code, 200)

    def test_detail2response(self):
        post1 = Post.objects.create(title='Test Title2', slug='Test_Slug22', body='Testing Body Field',
                                    status="published", author=self.user)

        request = self.factory.get('/news/' + post1.slug)

        detailresponse = post_detail(request, post1.slug)
        self.assertEqual(detailresponse.status_code, 200)

    def test_list2response(self):
        request = self.factory.get('/news')

        request.user = self.user

        response = post_list(request)

        self.assertEqual(response.status_code, 200)

class CommentPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', email='c@example.com', password='pass')
        self.post = Post.objects.create(title='Comment Title', slug='comment-title',
                                        body='Comment Body', status='published', author=self.user)

    def test_comment_post_creates_comment_for_logged_in_user(self):
        self.client.login(username='commenter', password='pass')
        response = self.client.post(reverse('news:post_detail', args=[self.post.slug]),
                                    {'name': 'commenter', 'email': 'c@example.com', 'body': 'Nice post'})
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(post=self.post)
        self.assertEqual(comment.body, 'Nice post')
        self.assertEqual(comment.name, 'commenter')
        self.assertTrue(comment.active)

    def test_comment_requires_login(self):
        response = self.client.post(reverse('news:post_detail', args=[self.post.slug]),
                                    {'name': 'anon', 'email': 'a@example.com', 'body': 'Spam'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(post=self.post).exists())

    def test_invalid_comment_form_does_not_create_comment(self):
        self.client.login(username='commenter', password='pass')
        response = self.client.post(reverse('news:post_detail', args=[self.post.slug]),
                                    {'name': 'commenter', 'email': 'not-an-email', 'body': 'Bad'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(post=self.post).exists())

    def test_detail_get_renders_with_comment_context(self):
        self.client.login(username='commenter', password='pass')
        response = self.client.get(reverse('news:post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('comment_form', response.context)
        self.assertIn('comments', response.context)
