# Generated by Django 4.1 on 2023-03-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0032_operationcard_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationaccount',
            name='comment',
            field=models.CharField(max_length=100, null=True),
        ),
    ]