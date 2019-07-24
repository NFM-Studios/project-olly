# Generated by Django 2.2.2 on 2019-07-13 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0014_merge_20190605_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='awayteam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='awayteam', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='GameChoice', to='matches.GameChoice'),
        ),
        migrations.AlterField(
            model_name='match',
            name='hometeam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hometeam', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loser', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='map',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_map', to='matches.MapChoice'),
        ),
        migrations.AlterField(
            model_name='match',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='PlatformChoice', to='matches.PlatformChoice'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team1reportedwinner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team1reportedwinner', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2reportedwinner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team2reportedwinner', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='champions', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='matchdispute',
            name='team1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team1', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='matchdispute',
            name='team1origreporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team1OriginalReporter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='matchdispute',
            name='team2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team2', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='matchdispute',
            name='team2origreporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team2OriginalReporter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='matchdispute',
            name='teamreporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team1Disputer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='matchreport',
            name='reported_winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winnerreporting', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='matchreport',
            name='reporting_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teamreporting', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='matchreport',
            name='reporting_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userreporting', to=settings.AUTH_USER_MODEL),
        ),
    ]