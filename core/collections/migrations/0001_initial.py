# Generated by Django 3.0.7 on 2020-07-06 10:09

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0005_auto_20200706_1006'),
        ('concepts', '0005_auto_20200706_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_access', models.CharField(blank=True, choices=[('View', 'View'), ('Edit', 'Edit'), ('None', 'None')], default='View', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('uri', models.TextField(blank=True, null=True)),
                ('mnemonic', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-zA-Z0-9\\-\\.\\_\\@]+$'))])),
                ('version', models.CharField(max_length=255)),
                ('released', models.NullBooleanField(default=False)),
                ('retired', models.BooleanField(default=False)),
                ('is_latest_version', models.BooleanField(default=True)),
                ('name', models.TextField()),
                ('full_name', models.TextField(blank=True, null=True)),
                ('default_locale', models.TextField(blank=True, default='en')),
                ('supported_locales', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
                ('website', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('external_id', models.TextField(blank=True, null=True)),
                ('custom_validation_schema', models.TextField(blank=True, null=True)),
                ('active_concepts', models.IntegerField(default=0)),
                ('active_mappings', models.IntegerField(default=0)),
                ('last_concept_update', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('last_mapping_update', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('last_child_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('collection_type', models.TextField(blank=True)),
                ('preferred_source', models.TextField(blank=True)),
                ('repository_type', models.TextField(blank=True, default='Collection')),
                ('custom_resources_linked_source', models.TextField(blank=True)),
                ('concepts', models.ManyToManyField(to='concepts.Concept')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collections_collection_related_created_by', related_query_name='collections_collections_created_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collections_collection_related_updated_by', related_query_name='collections_collections_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='CollectionReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.TextField()),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='collections.Collection')),
            ],
            options={
                'db_table': 'collection_references',
            },
        ),
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(condition=models.Q(user=None), fields=('mnemonic', 'version', 'organization'), name='org_collection_unique'),
        ),
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(condition=models.Q(organization=None), fields=('mnemonic', 'version', 'user'), name='user_collection_unique'),
        ),
    ]