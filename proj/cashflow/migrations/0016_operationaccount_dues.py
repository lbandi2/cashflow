# Generated by Django 4.1 on 2022-08-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0015_operationcard_dues'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationaccount',
            name='dues',
            field=models.IntegerField(default=1),
        ),
    ]