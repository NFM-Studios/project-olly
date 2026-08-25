from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

import stripe
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from profiles.models import UserProfile
from .models import Product, Transaction


class ProductAmountTest(TestCase):
    def test_amount_accepts_and_saves_decimal(self):
        product = Product.objects.create(
            active=True,
            business='billing@example.com',
            amount=Decimal('19.99'),
            item_name='cred_100',
            name='100 Credits',
        )
        product.refresh_from_db()
        self.assertIsInstance(product.amount, Decimal)
        self.assertEqual(product.amount, Decimal('19.99'))

    def test_amount_default_is_zero(self):
        product = Product.objects.create(
            active=True,
            business='billing@example.com',
            amount=Decimal('0'),
            item_name='cred_50',
            name='50 Credits',
        )
        product.refresh_from_db()
        self.assertEqual(product.amount, Decimal('0'))


class StripeCheckoutDisabledTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='stripeuser', password='pass')
        self.product = Product.objects.create(
            active=True, business='store@example.com', amount=4.99,
            item_name='cred_10', name='10 Credits'
        )
        self.client.force_login(self.user)

    def test_disabled_redirects_to_store_without_calling_stripe(self):
        with patch('stripe.checkout.Session.create') as mock_create:
            response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('store:store'))
        mock_create.assert_not_called()

    def test_disabled_does_not_create_session_for_inactive_product(self):
        self.product.active = False
        self.product.save()
        with patch('stripe.checkout.Session.create') as mock_create:
            response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('store:store'))
        mock_create.assert_not_called()

    def test_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


@override_settings(STRIPE_ENABLED=True)
class StripeCheckoutEnabledTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='stripeuser', password='pass')
        self.product = Product.objects.create(
            active=True, business='store@example.com', amount=4.99,
            item_name='cred_10', name='10 Credits'
        )
        self.client.force_login(self.user)
        self.session_url = 'https://checkout.stripe.com/c/pay/test_session'

    def test_creates_session_and_redirects(self):
        with patch('stripe.checkout.Session.create', return_value=SimpleNamespace(url=self.session_url)) as mock_create:
            response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.session_url)
        mock_create.assert_called_once()
        kwargs = mock_create.call_args.kwargs
        self.assertEqual(kwargs['mode'], 'payment')
        self.assertEqual(kwargs['client_reference_id'], str(self.user.pk))
        self.assertEqual(kwargs['metadata'], {
            'product_item_name': self.product.item_name,
            'username': self.user.username,
        })
        line_item = kwargs['line_items'][0]
        self.assertEqual(line_item['quantity'], 1)
        self.assertEqual(line_item['price_data']['currency'], 'usd')
        self.assertEqual(line_item['price_data']['product_data']['name'], self.product.name)
        self.assertEqual(line_item['price_data']['unit_amount'], 499)
        self.assertTrue(kwargs['success_url'].endswith('?stripe=success'))
        self.assertTrue(kwargs['cancel_url'].endswith('?stripe=cancel'))

    def test_unit_amount_converted_from_decimal_amount(self):
        # amount is a Decimal; conversion must stay safe for both Decimal and float
        self.product.amount = Decimal('4.99')
        self.product.save()
        with patch('stripe.checkout.Session.create', return_value=SimpleNamespace(url=self.session_url)) as mock_create:
            response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        line_item = mock_create.call_args.kwargs['line_items'][0]
        self.assertEqual(line_item['price_data']['unit_amount'], 499)

    def test_inactive_product_redirects_to_store(self):
        self.product.active = False
        self.product.save()
        with patch('stripe.checkout.Session.create') as mock_create:
            response = self.client.post(reverse('store:stripe_checkout', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('store:store'))
        mock_create.assert_not_called()


class StripeWebhookTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='stripeuser', password='pass')
        self.product = Product.objects.create(
            active=True, business='store@example.com', amount=4.99,
            item_name='cred_10', name='10 Credits'
        )
        self.url = reverse('store:stripe_webhook')

    def completed_event(self, client_reference_id=None, username=None):
        metadata = {'product_item_name': self.product.item_name}
        if username:
            metadata['username'] = username
        session = {'client_reference_id': client_reference_id, 'metadata': metadata}
        return {'type': 'checkout.session.completed', 'data': {'object': session}}

    def post_event(self, event):
        with patch('stripe.Webhook.construct_event', return_value=event):
            return self.client.post(self.url, data=b'payload', content_type='application/json',
                                    HTTP_STRIPE_SIGNATURE='test_sig')

    def test_valid_event_credits_user_and_creates_transaction(self):
        response = self.post_event(self.completed_event(client_reference_id=str(self.user.pk)))
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.credits, 10)
        tx = Transaction.objects.get()
        self.assertEqual(tx.account, self.user.username)
        self.assertEqual(tx.num, 10)
        self.assertEqual(tx.type, 'Credits-Stripe')
        self.assertEqual(tx.cost, Decimal('4.99'))

    def test_valid_event_falls_back_to_username_metadata(self):
        response = self.post_event(self.completed_event(client_reference_id=None, username=self.user.username))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.get(user=self.user).credits, 10)
        self.assertEqual(Transaction.objects.get().account, self.user.username)

    def test_invalid_signature_returns_400(self):
        with patch('stripe.Webhook.construct_event',
                   side_effect=stripe.error.SignatureVerificationError('bad sig', 'payload', 'header')):
            response = self.client.post(self.url, data=b'payload', content_type='application/json',
                                        HTTP_STRIPE_SIGNATURE='bad_sig')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UserProfile.objects.get(user=self.user).credits, 0)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_malformed_payload_returns_400(self):
        with patch('stripe.Webhook.construct_event', side_effect=ValueError('bad payload')):
            response = self.client.post(self.url, data=b'not json', content_type='application/json',
                                        HTTP_STRIPE_SIGNATURE='test_sig')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UserProfile.objects.get(user=self.user).credits, 0)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_unhandled_event_type_returns_200(self):
        event = {'type': 'payment_intent.succeeded', 'data': {'object': {}}}
        response = self.post_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.get(user=self.user).credits, 0)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_unknown_user_returns_400(self):
        response = self.post_event(self.completed_event(client_reference_id='999999', username='nobody'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_unknown_product_returns_400(self):
        event = self.completed_event(client_reference_id=str(self.user.pk))
        event['data']['object']['metadata']['product_item_name'] = 'widget_5'
        response = self.post_event(event)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UserProfile.objects.get(user=self.user).credits, 0)
        self.assertEqual(Transaction.objects.count(), 0)