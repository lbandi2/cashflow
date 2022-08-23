# Generated by Django 4.0.6 on 2022-08-04 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0009_operationaccount_operationcard_delete_operation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_id', models.CharField(max_length=15)),
                ('date_received', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('due_date', models.DateField()),
                ('min_pay', models.FloatField()),
                ('total_pay', models.FloatField()),
                ('installments_pay', models.FloatField()),
                ('file_link', models.URLField()),
                ('is_paid', models.BooleanField(default=False)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashflow.card')),
            ],
        ),
        migrations.CreateModel(
            name='OperationBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(max_length=20)),
                ('authorization', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=30)),
                ('original_value', models.FloatField()),
                ('agreed_rate', models.FloatField()),
                ('billed_rate', models.FloatField()),
                ('debits_and_credits', models.FloatField()),
                ('deferred_balance', models.FloatField()),
                ('dues', models.CharField(max_length=5)),
                ('is_matched', models.BooleanField(default=False)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashflow.bill')),
            ],
        ),
    ]
