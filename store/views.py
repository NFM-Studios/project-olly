from decimal import Decimal
from urllib.parse import urlsplit

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from paypal.standard.forms import PayPalPaymentsForm

from profiles.models import UserProfile
from .forms import TransferCreditsForm
from .invoice_generator import generateinvoice
from .models import Product, Transaction


def _paypal_notify_url(request):
    site_url = settings.SITE_URL.rstrip('/')
    try:
        parsed = urlsplit(site_url)
    except ValueError:
        parsed = None
    if parsed and parsed.scheme in ('http', 'https') and parsed.netloc:
        return site_url + '/paypal/'
    return request.build_absolute_uri('/paypal/')


def store(request):
    products = Product.objects.filter(active=True)
    return render(request, 'store/store.html', {'products': products})


def detail(request, pk):
    product = Product.objects.get(id=pk)
    invoice_id = generateinvoice()
    paypal_dict = {
        "business": product.business,
        "amount": product.amount,
        "item_name": product.name,
        "invoice": str(invoice_id),
        "notify_url": _paypal_notify_url(request),
        "custom": "{'item_name' : '%s', 'user' : '%s'}" % (product.item_name, str(request.user)),

    }
    product_pk = product.pk
    product = {
        'item': product.name,
        'cost': product.amount
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'store/product.html', {'product': product, 'form': form, 'product_pk': product_pk})


@login_required
def stripe_checkout(request, pk):
    if not settings.STRIPE_ENABLED:
        messages.error(request, "Stripe payments are not enabled")
        return redirect('store:store')
    try:
        product = Product.objects.get(id=pk, active=True)
    except Product.DoesNotExist:
        messages.error(request, "Product not found")
        return redirect('store:store')
    store_url = request.build_absolute_uri(reverse('store:store'))
    unit_amount = int(Decimal(str(product.amount)) * 100)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': unit_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        client_reference_id=str(request.user.pk),
        metadata={
            'product_item_name': product.item_name,
            'username': request.user.username,
        },
        success_url=store_url + '?stripe=success',
        cancel_url=store_url + '?stripe=cancel',
    )
    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user = None
        client_reference_id = session.get('client_reference_id')
        if client_reference_id:
            try:
                user = User.objects.get(pk=client_reference_id)
            except (User.DoesNotExist, ValueError):
                user = None
        if user is None:
            username = session.get('metadata', {}).get('username')
            try:
                user = User.objects.get(username=username)
            except (User.DoesNotExist, TypeError):
                return HttpResponse(status=400)
        item_name = session.get('metadata', {}).get('product_item_name')
        try:
            product = Product.objects.get(item_name=item_name)
        except (Product.DoesNotExist, TypeError):
            return HttpResponse(status=400)
        item_type, _, num_str = item_name.partition('_')
        if item_type in ['cred', 'credit', 'credits']:
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return HttpResponse(status=400)
            num = int(num_str)
            profile.credits += num
            profile.save()
            tx = Transaction(cost=product.amount, account=user.username, num=num, type='Credits-Stripe')
            tx.save()
    return HttpResponse(status=200)


'''
to get IPNs to work, login to the business account and enable IPNs under selling tools/instant payment notifications
'''


class Transfer(View):
    template_name = 'store/transfer.html'
    form_class = TransferCreditsForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'store/transfer.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            num = form.cleaned_data['credits']
            dest_username = form.cleaned_data['destination_user']
            up = UserProfile.objects.get(user__username=request.user)
            if dest_username == request.user.username:
                messages.error(request, "You can't transfer credits to yourself")
                return render(request, self.template_name, {'form': form})
            try:
                d_up = UserProfile.objects.get(user__username=dest_username)
            except UserProfile.DoesNotExist:
                messages.error(request, "That isn't a valid user")
                return render(request, self.template_name, {'form': form})
            if num <= 0:
                messages.error(request, "You can't transfer 0 or negative credits")
                return render(request, self.template_name, {'form': form})
            if up.credits - num < 0:
                messages.error(request, "You don't have enough credits")
                return render(request, self.template_name, {'form': form})
            with transaction.atomic():
                up.credits -= num
                d_up.credits += num
                up.save()
                d_up.save()
                messages.success(request, "Transferred credits")
                xfer = form.save(commit=False)
                xfer.destination = dest_username
                xfer.origin = request.user.username
                xfer.credits = num
                xfer.save()
                return redirect(reverse('profiles:profile_no_username'))

        return render(request, self.template_name, {'form': form})
