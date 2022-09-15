# Generated by Django 4.1 on 2022-08-30 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0021_alter_trip_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='accomodation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='car',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trip',
            name='is_incomplete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trip',
            name='shopping',
            field=models.CharField(blank=True, default=False, max_length=10, null=True),
        ),
    ]