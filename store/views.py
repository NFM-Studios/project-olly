from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .forms import TransferCreditsForm
from profiles.models import UserProfile
from django.contrib import messages
from django.views.generic import View
from .models import Transfer
from .invoice_generator import generateinvoice


def store(request):
    return render(request, 'store/store.html')


'''
each product has 2 dicts, paypal and general info that gets displayed on the site
'''


def buy_credits(request, num):
    invoice_id = generateinvoice()
    if num == '1':
        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": "5.00",
            "item_name": "15 Credits",
            "invoice": str(invoice_id),
            "notify_url": settings.SITE_URL + '/paypal/',
            "custom": "15cred,"+str(request.user),
        }
        product = {
            'item': '15 Credits',
            'cost': '$5.00',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form, "product": product}
        return render(request, "store/product.html", context)
    if num == '2':
        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": "20.00",
            "item_name": "25 Credits",
            "invoice": str(invoice_id),
            "notify_url": settings.SITE_URL + '/paypal/',
            "custom": "25cred,"+str(request.user),
        }
        product = {
            'item': '25 Credits',
            'cost': '$20.00',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form, "product": product}
        return render(request, "store/product.html", context)
    if num == '3':
        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": "45.00",
            "item_name": "50 Credits",
            "invoice": str(invoice_id),
            "notify_url": settings.SITE_URL + '/paypal/',
            "custom": "50cred,"+str(request.user),
        }
        product = {
            'item': '50 Credits',
            'cost': '$45.00',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form, "product": product}
        return render(request, "store/product.html", context)
    if num == '4':
        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": "10.00",
            "item_name": "Event pass",
            "invoice": str(invoice_id),
            "notify_url": settings.SITE_URL + '/paypal/',
            "custom": "ev_pass,"+str(request.user),
        }
        product = {
            'item': 'Event pass',
            'cost': '$10.00',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form, "product": product}
        return render(request, "store/product.html", context)


'''
to get IPNs to work, login to the business account and enable IPNs under selling tools/instant payment notifications
'''


class Transfer(View):
    template_name = 'store/transfer.html'
    form_class = TransferCreditsForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            num = form.cleaned_data['credits']
            dest_user = form.cleaned_data['destination_user']
            up = UserProfile.objects.get(user__username=request.user)
            try:
                d_up = UserProfile.objects.get(user__username=dest_user)
            except:
                messages.error(request, 'That isn\'t a valid user')
                return render(request, self.template_name, {'form': form})
            if up.credits - num < 0:
                messages.error(request, 'You don\'t have enough credits')
            elif num <= 0:
                messages.error(request, 'You can\'t transfer 0 or negative credits')
            else:
                up.credits -= num
                d_up.credits += num
                up.save()
                d_up.save()
                messages.success(request, "Transferred credits")
                xfer = form.save(commit=False)
                xfer.destination = dest_user
                xfer.origin = request.user
                xfer.credits = num
                xfer.save()
                return redirect('/profile/')

        return render(request, self.template_name, {'form': form})

