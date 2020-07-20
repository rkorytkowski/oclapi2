# Generated by Django 3.0.8 on 2020-07-20 14:50

import core.mappings.mixins
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('internal_reference_id', models.CharField(blank=True, max_length=255, null=True)),
                ('public_access', models.CharField(blank=True, choices=[('View', 'View'), ('Edit', 'Edit'), ('None', 'None')], default='View', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('uri', models.TextField(blank=True, null=True)),
                ('version', models.CharField(max_length=255)),
                ('released', models.NullBooleanField(default=False)),
                ('retired', models.BooleanField(default=False)),
                ('is_latest_version', models.BooleanField(default=True)),
                ('custom_validation_schema', models.TextField(blank=True, null=True)),
                ('map_type', models.TextField()),
                ('to_concept_code', models.TextField(blank=True, null=True)),
                ('to_concept_name', models.TextField(blank=True, null=True)),
                ('external_id', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mappings',
            },
            bases=(core.mappings.mixins.MappingValidationMixin, models.Model),
        ),
    ]
