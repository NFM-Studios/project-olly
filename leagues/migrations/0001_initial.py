# Generated by Django 2.2.15 on 2020-12-09 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='League Name', max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('info', models.TextField(default='No information provided')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='league_images')),
                ('teamformat', models.SmallIntegerField(choices=[(0, '1v1'), (1, '2v2'), (2, '3v3'), (3, '4v4'), (4, '5v5'), (5, '6v6')], default=1)),
                ('bestof', models.SmallIntegerField(choices=[(0, 'Best of 1'), (1, 'Best of 3'), (2, 'Best of 5'), (3, 'Best of 7'), (4, 'Best of 9')], default=0)),
                ('allow_register', models.BooleanField(default=False)),
                ('open_register', models.DateTimeField()),
                ('close_register', models.DateTimeField()),
                ('start', models.DateTimeField()),
                ('req_credits', models.PositiveSmallIntegerField(default=0)),
                ('size', models.PositiveSmallIntegerField(default=8)),
                ('disable_userreport', models.BooleanField(default=False)),
                ('prize1', models.CharField(default='no prize specified', max_length=50)),
                ('prize2', models.CharField(default='no prize specified', max_length=50)),
                ('prize3', models.CharField(default='no prize specified', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueFreeAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='Include information about Free Agent here')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='League Ruleset', max_length=50)),
                ('ot_losses', models.BooleanField(default=True)),
                ('pts_ot_loss', models.PositiveSmallIntegerField(default=1)),
                ('ot_wins', models.BooleanField(default=False)),
                ('pts_ot_win', models.PositiveSmallIntegerField(default=3)),
                ('pts_win', models.PositiveSmallIntegerField(default=3)),
                ('pts_loss', models.PositiveSmallIntegerField(default=0)),
                ('allow_tie', models.BooleanField(default=False)),
                ('num_games', models.PositiveIntegerField(default=10)),
                ('auto_schedule', models.BooleanField(default=False)),
                ('auto_matchup', models.BooleanField(default=False)),
                ('num_divisions', models.PositiveSmallIntegerField(default=2)),
                ('max_division_size', models.PositiveSmallIntegerField(default=5)),
                ('require_xbl', models.BooleanField(default=False)),
                ('require_psn', models.BooleanField(default=False)),
                ('require_steam', models.BooleanField(default=False)),
                ('require_epic', models.BooleanField(default=False)),
                ('require_lol', models.BooleanField(default=False)),
                ('require_battlenet', models.BooleanField(default=False)),
                ('require_activision', models.BooleanField(default=False)),
                ('allow_fa', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveSmallIntegerField(default=0)),
                ('losses', models.PositiveSmallIntegerField(default=0)),
                ('ot_losses', models.PositiveSmallIntegerField(default=0)),
                ('ot_wins', models.PositiveSmallIntegerField(default=0)),
                ('ties', models.PositiveSmallIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
