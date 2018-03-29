# Generated by Django 2.0.1 on 2018-03-29 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleEliminationTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='No name provided', max_length=50)),
                ('teamformat', models.SmallIntegerField(choices=[(0, '1v1'), (1, '2v2'), (2, '3v3'), (3, '4v4'), (4, '5v5'), (5, '6v6')], default=1)),
                ('bestof', models.SmallIntegerField(choices=[(0, 'Best of 1'), (1, 'Best of 3'), (2, 'Best of 5'), (3, 'Best of 7'), (4, 'Best of 9')], default=0)),
                ('active', models.BooleanField(default=False)),
                ('open_register', models.DateTimeField()),
                ('close_register', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('req_credits', models.PositiveSmallIntegerField(default=0)),
                ('platform', models.SmallIntegerField(choices=[(0, 'Playstation 4'), (1, 'Xbox One'), (2, 'PC'), (3, 'Mobile'), (4, 'Nintendo Switch'), (5, 'Playstation 3'), (6, 'Xbox 360')], default=0)),
                ('game', models.SmallIntegerField(choices=[(0, 'No Game Set'), (1, 'Call of Duty Black Ops 3'), (2, 'Call of Duty WWII'), (3, 'Fortnite'), (4, 'Destiny 2'), (5, 'Counter-Strike: Global Offensive'), (6, 'Player Unknowns Battlegrounds'), (7, 'Rainbow Six Siege'), (8, 'Overwatch'), (9, 'League of Legends'), (10, 'Hearthstone'), (11, 'World of Warcraft'), (12, 'Smite'), (13, 'Rocket League'), (14, 'Battlefield 1')], default=0)),
                ('start', models.DateTimeField()),
                ('size', models.PositiveSmallIntegerField(choices=[(4, 4), (8, 8), (16, 16), (32, 32), (64, 64), (128, 128)], default=32)),
                ('prize1', models.CharField(default='no prize specified', max_length=50)),
                ('prize2', models.CharField(default='no prize specified', max_length=50)),
                ('prize3', models.CharField(default='no prize specified', max_length=50)),
                ('second', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondplaceteam', to='teams.Team')),
                ('teams', models.ManyToManyField(blank=True, to='teams.Team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winningteam', to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='SingleTournamentRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roundnum', models.PositiveSmallIntegerField(default=1)),
                ('matchesnum', models.PositiveSmallIntegerField(default=2)),
                ('matches', models.ManyToManyField(to='matches.Match')),
                ('teams', models.ManyToManyField(to='teams.Team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withtournamentround', to='singletournaments.SingleEliminationTournament')),
            ],
        ),
        migrations.CreateModel(
            name='SingleTournamentTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed', models.PositiveIntegerField(default=0)),
                ('round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaminround', to='singletournaments.SingleTournamentRound')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actualteam', to='teams.Team')),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intournament', to='singletournaments.SingleEliminationTournament')),
            ],
        ),
    ]
