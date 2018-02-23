from django.db import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from store.get_username import get_username
from django.contrib.auth.models import User
from profiles.models import UserProfile
# Create your models here.


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.reciever_email != settings.PAYPAL_EMAIL:
            return
        if ipn_obj.custom == "15cred":
            price = 5.00
        elif ipn_obj.custom == "25cred":
            price = 20.00
        elif ipn_obj.custom == "50cred":
            price = 45.00
        else:
            price = 0.00
        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == "USD":
            req = get_username()
            if ipn_obj.custom == "15cred":
                req.user.credits += 15  # I have no clue if this will work because paypal won't send ipns
                tx = Transaction(account=req, cost=5.00)
                tx.save()
            if ipn_obj.custom == "25cred":
                req.user.credits += 25  # I have no clue if this will work because paypal won't send ipns
                tx = Transaction(account=req, cost=20.00)
                tx.save()
            if ipn_obj.custom == "50cred":
                req.user.credits += 50  # I have no clue if this will work because paypal won't send ipns
                tx = Transaction(account=req, cost=45.00)
                tx.save()


valid_ipn_received.connect(show_me_the_money)


class Transaction(models.Model):
    def __str__(self):
        return str(self.user)
    date = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    account = models.CharField(max_length=50)


def deduct_credits(request, num):
    up = UserProfile.objects.get(user__username=request.user)
    up.credits -= num
    up.save()


def give_credits(request, num):  # might not be needed. added it anyway.
    up = UserProfile.objects.get(user__username=request.user)
    up.credits += num
    up.save()


class Transfer(models.Model):
    def __str__(self):
        return str(self.user)
    date = models.DateTimeField(auto_now=True)
    credits = models.DecimalField(max_digits=6, decimal_places=0)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
