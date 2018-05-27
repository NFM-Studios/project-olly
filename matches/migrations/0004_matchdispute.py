# Generated by Django 2.0.4 on 2018-04-05 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_teaminvite_hasperms'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0003_auto_20180404_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchDispute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('team1proof', models.CharField(default='(team 1) no text inserted', max_length=300)),
                ('team2proof', models.CharField(default='(team 2) no text inserted', max_length=300)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputedMatch', to='matches.Match')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='teams.Team')),
                ('team1origreporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1OriginalReporter', to=settings.AUTH_USER_MODEL)),
                ('team1reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1Disputer', to=settings.AUTH_USER_MODEL)),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='teams.Team')),
                ('team2origreporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2OriginalReporter', to=settings.AUTH_USER_MODEL)),
                ('team2reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2Disputer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
