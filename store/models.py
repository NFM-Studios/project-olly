from django.db import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.contrib.auth.models import User
from profiles.models import UserProfile
# Create your models here.

'''
each product gets an elif to set price and then another to create the tx in the db and apply credits, etc to profile
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
                tx = Transaction(account=username, cost=5.00, num=15, type='Credit')
                tx.save()
            if num == "25cred":
                user.credits += 25
                user.save()
                tx = Transaction(account=username, cost=20.00, num=25, type='Credit')
                tx.save()
            if num == "50cred":
                user.credits += 50
                user.save()
                tx = Transaction(account=username, cost=45.00, num=50, type='Credit')
                tx.save()
            if num == "ev_pass":
                user.passes += 1
                user.save()
                tx = Transaction(account=username, cost=10.00, num=1, type='Pass')
                tx.save()


valid_ipn_received.connect(show_me_the_money)


class Transaction(models.Model):
    def __str__(self):
        return str(self.account)
    date = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    account = models.CharField(max_length=50)
    staff = models.CharField(max_length=50, blank=True)
    num = models.SmallIntegerField()
    type = models.CharField(max_length=50)


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

