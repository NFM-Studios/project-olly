from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from support.models import Ticket, TicketCategory, TicketComment


class SupportTicketOwnershipTest(TestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(username='usera', email='a@example.com', password='password')
        self.user_b = User.objects.create_user(username='userb', email='b@example.com', password='password')
        self.category = TicketCategory.objects.create(name='Bug', priority=1)

    def test_user_cannot_view_another_users_ticket(self):
        ticket = Ticket.objects.create(creator=self.user_a, text='secret', category=self.category, status=0)
        self.client.force_login(self.user_b)
        response = self.client.get(reverse('support:detail', args=[ticket.pk]))
        self.assertRedirects(response, reverse('support:list'))

    def test_owner_can_view_own_ticket(self):
        ticket = Ticket.objects.create(creator=self.user_a, text='mine', category=self.category, status=0)
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('support:detail', args=[ticket.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_comment_on_another_users_ticket(self):
        ticket = Ticket.objects.create(creator=self.user_a, text='secret', category=self.category, status=0)
        self.client.force_login(self.user_b)
        response = self.client.post(reverse('support:detail', args=[ticket.pk]),
                                    {'post_comment': '1', 'comment': 'sneaky'})
        self.assertRedirects(response, reverse('support:list'))
        self.assertFalse(TicketComment.objects.filter(ticket=ticket).exists())

    def test_user_cannot_change_another_users_ticket_status(self):
        ticket = Ticket.objects.create(creator=self.user_a, text='secret', category=self.category, status=0)
        self.client.force_login(self.user_b)
        response = self.client.post(reverse('support:detail', args=[ticket.pk]), {'change_status': '1'})
        self.assertRedirects(response, reverse('support:list'))
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 0)