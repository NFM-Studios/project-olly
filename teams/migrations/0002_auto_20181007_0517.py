# Generated by Django 2.0.8 on 2018-10-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='twitch',
            field=models.CharField(blank=True, default='None Linked', max_length=15),
        ),
        migrations.AlterField(
            model_name='team',
            name='twitter',
            field=models.CharField(blank=True, default='None Linked', max_length=15),
        ),
    ]
