from asgiref.sync import async_to_sync, sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import path

from olly.asgi import application
from profiles.models import Notification, UserProfile
from realtime.consumers import NotificationConsumer
from realtime.utils import notify_many, notify_user

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

consumer_router = URLRouter([
    path('ws/notifications/', NotificationConsumer.as_asgi()),
])


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class NotifyUserTests(TestCase):
    """Unit tests for the notify_user / notify_many helpers."""

    def setUp(self):
        self.user = User.objects.create_user(username='notifyuser', password='pass')
        self.profile = self.user.user

    def test_notify_user_creates_and_attaches_notification(self):
        notification = notify_user(
            self.user,
            title='Test notification',
            description='Some details',
            sender='Tester',
            type='team',
            link='teams:detail',
            pk1=42,
        )
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.title, 'Test notification')
        self.assertEqual(notification.description, 'Some details')
        self.assertEqual(notification.sender, 'Tester')
        self.assertEqual(notification.type, 'team')
        self.assertEqual(notification.link, 'teams:detail')
        self.assertEqual(notification.pk1, 42)
        self.assertTrue(self.profile.notifications.filter(pk=notification.pk).exists())

    def test_notify_user_accepts_userprofile(self):
        notification = notify_user(self.profile, title='Via profile')
        self.assertTrue(self.profile.notifications.filter(pk=notification.pk).exists())

    def test_notify_user_defaults(self):
        notification = notify_user(self.user, title='Defaults')
        self.assertEqual(notification.description, 'No description given')
        self.assertEqual(notification.sender, 'System')
        self.assertEqual(notification.type, 'general')
        self.assertEqual(notification.link, '')
        self.assertEqual(notification.pk1, 0)

    def test_notify_user_missing_profile_does_not_raise(self):
        UserProfile.objects.filter(user=self.user).delete()
        notification = notify_user(self.user, title='No profile')
        self.assertIsInstance(notification, Notification)
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())

    def test_notify_many_notifies_each_user(self):
        users = [self.user]
        for i in range(2):
            users.append(User.objects.create_user(username='notifyuser%d' % i, password='pass'))
        notifications = notify_many(users, title='Broadcast', type='league',
                                    link='leagues:detail', pk1=7)
        self.assertEqual(len(notifications), len(users))
        for user, notification in zip(users, notifications):
            self.assertTrue(user.user.notifications.filter(pk=notification.pk).exists())


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class NotificationConsumerTests(TransactionTestCase):
    """Websocket tests.

    TransactionTestCase is used so data created in the test thread is
    committed and visible to the consumer thread. Each test drives the whole
    websocket scenario inside a single coroutine (via one async_to_sync call)
    so the application task lives on a single, persistent event loop.

    An authenticated consumer is exercised by injecting the user into the
    communicator scope (the standard channels testing pattern); the
    unauthenticated test drives the full application with AuthMiddlewareStack.
    """

    def _run(self, scenario):
        async_to_sync(scenario)()

    def test_unauthenticated_connect_rejected(self):
        async def scenario():
            communicator = WebsocketCommunicator(application, '/ws/notifications/')
            connected, code = await communicator.connect()
            self.assertFalse(connected)
            self.assertNotEqual(code, 1000)
            await communicator.wait(timeout=1)

        self._run(scenario)

    def test_authenticated_connect_accepts_and_receives_notification(self):
        user = User.objects.create_user(username='wsuser', password='pass')
        notification = None

        async def scenario():
            nonlocal notification
            communicator = WebsocketCommunicator(consumer_router, '/ws/notifications/')
            communicator.scope['user'] = user
            connected, _ = await communicator.connect()
            self.assertTrue(connected)
            notification = await sync_to_async(notify_user)(user, title='Hello', description='World',
                                                            type='news', link='/news/', pk1=3)
            message = await communicator.receive_json_from(timeout=5)
            self.assertEqual(message['action'], 'notification')
            self.assertEqual(message['id'], notification.pk)
            self.assertEqual(message['title'], 'Hello')
            self.assertEqual(message['description'], 'World')
            self.assertEqual(message['type'], 'news')
            self.assertEqual(message['link'], '/news/')
            self.assertIn('datetime', message)
            await communicator.disconnect()

        self._run(scenario)
        self.assertTrue(user.user.notifications.filter(pk=notification.pk).exists())

    def test_notification_delivered_only_to_its_user(self):
        user1 = User.objects.create_user(username='wsuser1', password='pass')
        user2 = User.objects.create_user(username='wsuser2', password='pass')

        async def scenario():
            comm1 = WebsocketCommunicator(consumer_router, '/ws/notifications/')
            comm1.scope['user'] = user1
            comm2 = WebsocketCommunicator(consumer_router, '/ws/notifications/')
            comm2.scope['user'] = user2
            connected1, _ = await comm1.connect()
            connected2, _ = await comm2.connect()
            self.assertTrue(connected1)
            self.assertTrue(connected2)
            await sync_to_async(notify_user)(user1, title='Only for user1')
            message = await comm1.receive_json_from(timeout=5)
            self.assertEqual(message['title'], 'Only for user1')
            self.assertTrue(await comm2.receive_nothing(timeout=1))
            await comm1.disconnect()
            await comm2.disconnect()

        self._run(scenario)

    def test_ping_pong(self):
        user = User.objects.create_user(username='wsping', password='pass')

        async def scenario():
            communicator = WebsocketCommunicator(consumer_router, '/ws/notifications/')
            communicator.scope['user'] = user
            connected, _ = await communicator.connect()
            self.assertTrue(connected)
            await communicator.send_json_to({'action': 'ping'})
            response = await communicator.receive_json_from(timeout=5)
            self.assertEqual(response, {'action': 'pong'})
            await communicator.disconnect()

        self._run(scenario)