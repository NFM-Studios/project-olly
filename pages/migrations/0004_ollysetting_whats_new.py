# Generated by Django 2.2.15 on 2021-07-19 20:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_ollysetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='ollysetting',
            name='whats_new',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]