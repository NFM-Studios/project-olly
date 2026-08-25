from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserProfile


class UserProfileRankTest(TestCase):
    def test_calculate_rank_among_three_profiles(self):
        user1 = User.objects.create_user(username='rank1', password='pass')
        user2 = User.objects.create_user(username='rank2', password='pass')
        user3 = User.objects.create_user(username='rank3', password='pass')
        p1 = user1.user
        p2 = user2.user
        p3 = user3.user
        p1.xp = 10
        p2.xp = 30
        p3.xp = 20
        p1.save()
        p2.save()
        p3.save()

        p1.calculate_rank()
        p2.calculate_rank()
        p3.calculate_rank()

        self.assertEqual(p2.rank, 1)
        self.assertEqual(p3.rank, 2)
        self.assertEqual(p1.rank, 3)

    def test_calculate_rank_persists_to_db(self):
        user1 = User.objects.create_user(username='rankdb1', password='pass')
        user2 = User.objects.create_user(username='rankdb2', password='pass')
        p1 = user1.user
        p2 = user2.user
        p1.xp = 5
        p2.xp = 100
        p1.save()
        p2.save()

        p1.calculate_rank()

        db_rank = UserProfile.objects.get(pk=p1.pk).rank
        self.assertEqual(db_rank, 2)