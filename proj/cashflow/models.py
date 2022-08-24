from django.db import models
from django.urls import reverse

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

    def is_checked(self):
        """Checks that all related operations are matched with mail operations"""
        ops = [item.is_matched for item in self.operations()]
        return all(ops)

    def inconsistencies(self):
        """Returns the number of inconsistencies"""
        matched = [item for item in self.operations() if item.is_matched]
        return len(self.operations()) - len(matched)


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

    def get_absolute_url(self):
        return reverse("op_bill", args=[self.id])

class OperationCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=20)
    amount = models.FloatField()
    entity = models.CharField(max_length=50)
    category = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.date} [{self.type.upper()}] {self.entity.upper()} ${self.amount:,.2f}"

    def date_string(self):
        return self.date.strftime('%Y-%m-%d')


class OperationAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=20)
    amount = models.FloatField()
    entity = models.CharField(max_length=50)
    category = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.date} [{self.type.upper()}] {self.entity.upper()} ${self.amount:,.2f}"

    def date_string(self):
        return self.date.strftime('%Y-%m-%d')


class OperationCategories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class AccountCategories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name