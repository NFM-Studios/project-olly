# Generated by Django 2.0.2 on 2018-08-03 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ip',
            field=models.CharField(default='0.0.0.0', max_length=45),
        ),
    ]
