# Generated by Django 3.0.8 on 2020-07-20 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mappings', '0002_auto_20200720_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapping',
            name='versioned_object_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
