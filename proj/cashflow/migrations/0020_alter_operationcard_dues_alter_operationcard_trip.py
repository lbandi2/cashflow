# Generated by Django 4.1 on 2022-08-30 14:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0019_trip_alter_operationaccount_trip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationcard',
            name='dues',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='operationcard',
            name='trip',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashflow.trip'),
        ),
    ]
