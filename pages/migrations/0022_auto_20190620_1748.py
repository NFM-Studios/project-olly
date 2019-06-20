# Generated by Django 2.2.2 on 2019-06-20 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0021_merge_20190607_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticinfo',
            name='featured_tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='featured_tournament',
                                    to='singletournaments.SingleEliminationTournament'),
        ),
    ]
