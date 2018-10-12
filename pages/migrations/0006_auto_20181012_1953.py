# Generated by Django 2.0.4 on 2018-10-12 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20181012_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide1big',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide1link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide1small',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide2big',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide2link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide2small',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide3big',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide3link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingeslide3small',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop1',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop1link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop2',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop2link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop3',
            field=models.TextField(blank=True, default='Coming Soon!', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='bingetop3link',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='slide1link',
            field=models.TextField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='slide2link',
            field=models.TextField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='staticinfo',
            name='slide3link',
            field=models.TextField(blank=True, default='#', null=True),
        ),
    ]
