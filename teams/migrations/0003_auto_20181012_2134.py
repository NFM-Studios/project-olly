# Generated by Django 2.0.8 on 2018-10-12 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20181007_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='rank',
            field=models.PositiveSmallIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='team',
            name='totalxp',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
