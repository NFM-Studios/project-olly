# Generated by Django 2.0.8 on 2018-10-12 02:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('singletournaments', '0004_singleeliminationtournament_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleeliminationtournament',
            name='game',
            field=models.SmallIntegerField(
                choices=[(0, 'No Game Set'), (1, 'Call of Duty Black Ops 3'), (2, 'Call of Duty WWII'), (3, 'Fortnite'),
                         (4, 'Destiny 2'), (5, 'Counter-Strike: Global Offensive'),
                         (6, 'Player Unknowns Battlegrounds'), (7, 'Rainbow Six Siege'), (8, 'Overwatch'),
                         (9, 'League of Legends'), (10, 'Hearthstone'), (11, 'World of Warcraft'), (12, 'Smite'),
                         (13, 'Rocket League'), (14, 'Battlefield 1'), (15, 'Black Ops 4')], default=0),
        ),
    ]
