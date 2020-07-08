# Generated by Django 3.0.7 on 2020-07-06 10:06

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_auto_20200622_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='mnemonic',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-zA-Z0-9\\-\\.\\_\\@]+$'))]),
        ),
    ]
