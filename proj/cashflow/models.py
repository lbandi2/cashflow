from django.db import models
from django.urls import reverse

# from trips.models import Trip
# import locale
from datetime import datetime, timedelta
from itertools import chain

from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Q

class Account(models.Model):
    bank = models.CharField(max_length=30)
    owner = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    creation = models.DateField(auto_now_add=True)
    is_corporate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.number}] {self.owner}"

    def name(self):
        return self.owner.split(' ')[0]

class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    brand = models.CharField(max_length=10)
    tier = models.CharField(max_length=10, null=True, blank=True) # gold, platinum
    type = models.CharField(max_length=10) # debit or credit
    limit = models.FloatField(null=True, blank=True)
    number = models.CharField(max_length=20)
    owner = models.CharField(max_length=50)
    expiration = models.DateField(null=True, blank=True)
    is_extension = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.type.upper()}] {self.brand.upper()} {self.tier.title() if self.tier else ''}{'Corporate' if self.account.is_corporate else ''} {self.number} - {self.owner}"

    def bills(self):
        return Bill.objects.filter(id=self.id)

    def name(self):
        return self.owner.split(' ')[0]

class Bill(models.Model):
    bill_id = models.CharField(max_length=15, null=False, blank=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_received = models.DateField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)
    min_pay = models.FloatField(null=False, blank=False)
    total_pay = models.FloatField(null=False, blank=False)
    installments_pay = models.FloatField(null=False, blank=False)
    file_link = models.URLField()
    has_inconsistency = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"[{'PAID' if self.is_paid else 'UNPAID'}] {self.start_date} {self.end_date} {self.card}"

    def operations(self):
        return OperationBill.objects.filter(bill_id=self.id)

    def card_operations(self):
        return OperationCard.objects\
                .filter(card=self.card)\
                .filter(date__gte=self.start_date - timedelta(days=3))\
                .filter(date__lte=self.end_date + timedelta(days=3))

    def is_checked(self):
        """Checks that all related operations are matched with mail operations"""
        ops = [item.is_matched for item in self.operations().filter(type='expense')]
        return all(ops)

    def inconsistencies(self):
        """Returns the number of inconsistencies"""
        matched = [item for item in self.operations() if item.is_matched and item.type == 'expense']
        taxes = [item for item in self.operations() if item.type != 'expense']
        return len(self.operations()) - len(matched) - len(taxes)

    def unmatched_card_ops(self):
        # matched = [item.op_match_id for item in self.operations() if item.op_match_id or item.type != 'expense']
        matched = [item.op_match_id for item in OperationBill.objects.all() if item.op_match_id or item.type != 'expense']
        return OperationCard.objects\
                .exclude(id__in=matched)\
                .filter(date__gte=self.start_date)\
                .filter(date__lte=self.end_date)\
                .filter(card=self.card)

    def unmatched_bill_ops(self):
        return self.operations().filter(is_matched=False).filter(type='expense')


class Trip(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    place = models.CharField(max_length=50)
    country = models.CharField(max_length=25)
    car = models.BooleanField(default=False)
    accomodation = models.CharField(max_length=50, null=True, blank=True) # choice (hotel, apt)
    shopping = models.CharField(max_length=10, default=1, null=True, blank=True) # low/med/high
    is_incomplete = models.BooleanField(default=False, blank=True, null=True)


    class Meta:
        db_table = 'trips_trip'
        managed = True

    def __str__(self):
        # locale.setlocale(locale.LC_TIME, "es_ES")
        start_date = self.start_date.strftime('%b').title().strip('.')
        end_date = self.end_date.strftime('%b').title().strip('.')
        year = self.start_date.strftime('%Y')
        date_string_short = f"({year})"
        if start_date == end_date:
            date_string = f"({start_date} {year})"
        else:
            date_string = f"({start_date}-{end_date} {year})"
        if self.place != self.country:
            text_string = f"{self.place}, {self.country[0:3].upper()} "
        else:
            text_string = f"{self.place} "
        if len(text_string + date_string) >= 30:
            return text_string + date_string_short
        else:
            return text_string + date_string

    # def operations(self):
    #     card_ops = OperationCard.objects.filter(trip_id=self.id)
    #     account_ops = OperationAccount.objects.filter(trip_id=self.id)
    #     return sorted(chain(card_ops, account_ops), key=lambda instance: instance.date, reverse=True)

    def card_operations(self):
        return OperationCard.objects.filter(trip_id=self.id).order_by('-date')

    def account_operations(self):
        return OperationAccount.objects.filter(trip_id=self.id).order_by('-date')

    def operations(self):
        # card_ops = OperationCard.objects.filter(trip_id=self.id)
        # account_ops = OperationAccount.objects.filter(trip_id=self.id)
        return self.card_operations().union(self.account_operations())

    def num_operations(self):
        return len(self.operations())

    def total_amount(self):
        amount = 0
        for item in self.operations():
            amount += item.amount
        return amount

    def daily_spend(self):
        days = (self.end_date - self.start_date).days
        return self.total_amount() / days


class OperationCategories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def operations(self):
        card_ops = OperationCard.objects.order_by('-date').filter(category=self.id)
        account_ops = OperationAccount.objects.order_by('-date').filter(category=self.id)
        return sorted(chain(card_ops, account_ops), key=lambda instance: instance.date, reverse=True)

    def num_operations(self):
        return len(self.operations())


class OperationCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=20)
    amount = models.FloatField()
    entity = models.CharField(max_length=50)
    category = models.ForeignKey(OperationCategories, null=True, blank=True, default=None, on_delete = models.SET_NULL)
    dues = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    trip = models.ForeignKey(Trip, null=True, blank=True, on_delete = models.SET_NULL)

    def __str__(self):
        return f"{self.date.strftime('%m-%d')} [{self.entity.upper()}] ${self.amount:,.2f}"

    def date_string(self):
        return self.date.strftime('%Y-%m-%d')


class OperationAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=20)
    amount = models.FloatField()
    entity = models.CharField(max_length=50)
    # category = models.CharField(max_length=20, null=True, blank=True)
    category = models.ForeignKey(OperationCategories, null=True, blank=True, default=None, on_delete = models.SET_NULL)
    dues = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    trip = models.ForeignKey(Trip, null=True, blank=True, on_delete = models.SET_NULL)

    def __str__(self):
        return f"{self.date} [{self.type.upper()}] {self.entity.upper()} ${self.amount:,.2f}"

    def date_string(self):
        return self.date.strftime('%Y-%m-%d')


class OperationBill(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    type = models.CharField(max_length=20)
    authorization = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    original_value = models.FloatField()
    agreed_rate = models.FloatField()
    billed_rate = models.FloatField()
    debits_and_credits = models.FloatField()
    deferred_balance = models.FloatField()
    dues = models.CharField(max_length=5)
    is_matched = models.BooleanField(default=False)
    op_match = models.ForeignKey(OperationCard, null=True, blank=True, on_delete = models.SET_NULL)

    # def get_absolute_url(self):
    #     return reverse("op_bill", args=[self.id])

    def __str__(self):
        return f"{self.date.strftime('%m-%d')} [{self.name.upper()}] ${self.original_value:,.2f}"

    def get_absolute_url(self):
        return reverse(
            "bill_op_view", args=[str(self.bill.id), str(self.id)]
        )

