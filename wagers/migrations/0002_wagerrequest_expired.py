# Generated by Django 2.1.5 on 2019-04-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wagerrequest',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
