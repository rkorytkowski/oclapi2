# Generated by Django 3.0.8 on 2020-07-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('concepts', '0001_initial'),
        ('collections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='concepts',
            field=models.ManyToManyField(to='concepts.Concept'),
        ),
    ]
