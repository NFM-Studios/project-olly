# Generated by Django 2.0.4 on 2018-06-11 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singletournaments', '0007_auto_20180610_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleeliminationtournament',
            name='info',
            field=models.TextField(default='No information provided'),
        ),
    ]
