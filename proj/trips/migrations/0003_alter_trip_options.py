# Generated by Django 4.1 on 2022-08-29 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_alter_trip_end_date_alter_trip_start_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'managed': False},
        ),
    ]
