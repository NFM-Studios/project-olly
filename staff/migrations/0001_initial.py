# Generated by Django 2.2.15 on 2021-05-18 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0009_merge_20210507_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUnbanRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_created=True)),
                ('reason', models.TextField(default='Not specified')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unban_admin', to='profiles.UserProfile')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unbanned_profile', to='profiles.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserBanRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_created=True)),
                ('reason', models.TextField(default='Not specified')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ban_admin', to='profiles.UserProfile')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='banned_profile', to='profiles.UserProfile')),
            ],
        ),
    ]
