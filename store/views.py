from urllib.parse import urlsplit

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from paypal.standard.forms import PayPalPaymentsForm

from profiles.models import UserProfile
from .forms import TransferCreditsForm
from .invoice_generator import generateinvoice
from .models import Product


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
    product = {
        'item': product.name,
        'cost': product.amount
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'store/product.html', {'product': product, 'form': form})


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
