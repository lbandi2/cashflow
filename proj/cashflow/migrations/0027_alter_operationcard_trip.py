# Generated by Django 4.1 on 2022-08-31 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0026_alter_operationcard_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationcard',
            name='trip',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cashflow.trip'),
        ),
    ]
