# Generated by Django 2.0 on 2018-03-02 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='text',
            field=models.TextField(default='A detailed description of your issue', help_text='A detailed description of your issue'),
        ),
    ]
