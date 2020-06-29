# Generated by Django 3.0.7 on 2020-06-17 05:00

import re

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_auto_20200617_0500'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='mnemonic',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-zA-Z0-9\\-\\.\\_]+$'))]),
        ),
        migrations.AlterUniqueTogether(
            name='source',
            unique_together={('mnemonic', 'version', 'organization'), ('mnemonic', 'version', 'user')},
        ),
    ]
