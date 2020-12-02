# Generated by Django 2.2.15 on 2020-09-01 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20200901_1908'),
        ('leagues', '0016_league_teams'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguesettings',
            name='allow_fa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leagueteam',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='LeagueFreeAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='Include information about Free Agent here')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fa_profile', to='profiles.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='fa',
            field=models.ManyToManyField(blank=True, related_name='league_fas', to='leagues.LeagueFreeAgent'),
        ),
    ]
