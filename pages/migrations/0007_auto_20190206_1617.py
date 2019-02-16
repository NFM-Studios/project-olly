# Generated by Django 2.0.10 on 2019-02-06 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0006_auto_20181012_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticinfo',
            name='facebookpage',
            field=models.URLField(default='#', verbose_name='facebook_page'),
        ),
        migrations.AddField(
            model_name='staticinfo',
            name='instagrampage',
            field=models.URLField(default='#', verbose_name='instagram_page'),
        ),
        migrations.AddField(
            model_name='staticinfo',
            name='twitchchannel',
            field=models.URLField(default='#', verbose_name='twitch_channel'),
        ),
        migrations.AddField(
            model_name='staticinfo',
            name='twitterprofile',
            field=models.URLField(default='#', verbose_name='twitter_profile'),
        ),
        migrations.AddField(
            model_name='staticinfo',
            name='youtubechannel',
            field=models.URLField(default='#', verbose_name='youtube_channel'),
        ),
    ]
