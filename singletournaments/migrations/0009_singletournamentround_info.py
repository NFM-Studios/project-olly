# Generated by Django 2.0.8 on 2018-11-17 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singletournaments', '0008_singleeliminationtournament_twitch'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletournamentround',
            name='info',
            field=models.TextField(default='No info specified'),
        ),
    ]