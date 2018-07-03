from django.db import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.contrib.auth.models import User
from profiles.models import UserProfile
# Create your models here.


class Product(models.Model):
    # paypal dict info
    business = models.EmailField()
    amount = models.FloatField()
    item_name = models.CharField(max_length=50)

    # displayed on store
    price = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


'''
each product gets an elif to set price and then another to create the tx in the db and apply credits, etc to profile
this needs to be able to determine what product is being bought without anything being hardcoded to allow for new items
'''


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    custom_field = ipn_obj.custom.split(',', 2)
    num = custom_field[0]
    username = custom_field[1]
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_EMAIL:
            return
        if num == "15cred":
            price = 5.00
        elif num == "25cred":
            price = 20.00
        elif num == "50cred":
            price = 45.00
        elif num == "ev_pass":
            price = 10.00
        else:
            price = 0.00
        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == "USD":
            user = UserProfile.objects.get(user__username=custom_field[1])
            if num == "15cred":
                user.credits += 15
                user.save()
                tx = Transaction(account=username, cost=5.00, credits=15, passes=0)
                tx.save()
            if num == "25cred":
                user.credits += 25
                user.save()
                tx = Transaction(account=username, cost=20.00, credits=25, passes=0)
                tx.save()
            if num == "50cred":
                user.credits += 50
                user.save()
                tx = Transaction(account=username, cost=45.00, credits=50, passes=0)
                tx.save()
            if num == "ev_pass":
                user.passes += 1
                user.save()
                tx = Transaction(account=username, cost=10.00, credits=0, passes=1)
                tx.save()


valid_ipn_received.connect(show_me_the_money)


class Transaction(models.Model):
    def __str__(self):
        return str(self.user)
    date = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    account = models.CharField(max_length=50)
    credits = models.PositiveSmallIntegerField()
    passes = models.PositiveSmallIntegerField()
    staff = models.CharField(max_length=50, blank=True)


def deduct_credits(user, num):
    up = UserProfile.objects.get(user=user)
    up.credits -= num
    up.save()


def give_credits(user, num):  # might not be needed. added it anyway.
    up = UserProfile.objects.get(user=user)
    up.credits += num
    up.save()


class Transfer(models.Model):
    def __str__(self):
        return str(self.user)
    date = models.DateTimeField(auto_now=True)
    credits = models.DecimalField(max_digits=6, decimal_places=0)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)

