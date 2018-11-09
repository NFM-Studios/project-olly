from django.db import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.core.validators import RegexValidator
import ast
# Create your models here.


class Product(models.Model):
    active = models.BooleanField()
    # paypal dict info
    business = models.EmailField()
    amount = models.FloatField()
    item_name = models.CharField(max_length=50, validators=[
        RegexValidator(
            regex='^[a-zA-z]+_\d+',
            message="Item name must not have whitespace, and must be in the format 'type_num'",
            code='invalid_name'
        )
    ]
                                 )

    # displayed on store
    price = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


'''
each product gets an elif to set price and then another to create the tx in the db and apply credits, etc to profile
this needs to be able to determine what product is being bought without anything being hardcoded to allow for new items
enforce a specific structure(type_num) 
'''


# NEEDS TESTING
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    custom = ast.literal_eval(ipn_obj.custom)
    item = custom['item_name']
    username = custom['user']
    user = UserProfile.objects.get(user__username=username)
    product = Product.objects.get(item_name=item)
    item = item.split('_')
    itemtype = item[0]
    num = int(item[1])
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.business != settings.PAYPAL_EMAIL:
            tx = Transaction(cost=0, account=username, num=0, type='PayPal issue - mismatch with email')
            tx.save()
        price = int(product.amount)
        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == "USD":
            if itemtype in ['cred', 'credit', 'credits']:
                user.credits += num
                user.save()
                tx = Transaction(cost=product.amount, account=username, num=num, type='Credits')
                tx.save()
            else:
                tx = Transaction(cost=0, account=username, num=0, type='Local issue - not a valid item type')
                tx.save()
        else:
            tx = Transaction(cost=0, account=username, num=0, type='PayPal issue - price or currency mismatch')
            tx.save()
    else:
        tx = Transaction(cost=0, account=username, num=0, type='PayPal issue - payment not completed')
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

