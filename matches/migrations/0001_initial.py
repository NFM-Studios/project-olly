# Generated by Django 2.0.2 on 2018-03-14 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.SmallIntegerField(choices=[(0, 'No Game Set'), (1, 'Call of Duty Black Ops 3'), (2, 'Call of Duty WWII'), (3, 'Fortnite'), (4, 'Destiny 2'), (5, 'Counter-Strike: Global Offensive'), (6, 'Player Unknowns Battlegrounds'), (7, 'Rainbow Six Siege'), (8, 'Overwatch'), (9, 'League of Legends'), (10, 'Hearthstone'), (11, 'World of Warcraft'), (12, 'Smite'), (13, 'Rocket League'), (14, 'Battlefield 1')], default=0)),
                ('platform', models.SmallIntegerField(choices=[(0, 'Playstation 4'), (1, 'Xbox One'), (2, 'PC'), (3, 'Mobile'), (4, 'Nintendo Switch'), (5, 'Playstation 3'), (6, 'Xbox 360')], default=0)),
                ('start', models.DateTimeField()),
                ('reported', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('bestof', models.SmallIntegerField(choices=[(0, 'Best of 1'), (1, 'Best of 3'), (2, 'Best of 5'), (3, 'Best of 7'), (4, 'Best of 9')], default=0)),
                ('teamformat', models.SmallIntegerField(choices=[(0, '1v1'), (1, '2v2'), (2, '3v3'), (3, '4v4'), (4, '5v5'), (5, '6v6')], default=1)),
                ('awayteam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayteam', to='teams.Team')),
                ('hometeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometeam', to='teams.Team')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champions', to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchreporting', to='matches.Match')),
                ('reported_winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winnerreporting', to='teams.Team')),
                ('reporting_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamreporting', to='teams.Team')),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userreporting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RuleSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
            ],
        ),
    ]
