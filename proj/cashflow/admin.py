from django.contrib import admin
from cashflow.models import Account, Card, OperationCard, OperationAccount, Bill, OperationBill

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        # ('Date information', {'fields': ['creation']}),
        ('Account', {'fields': ['bank', 'owner', 'number']}),
        ('Corporate', {'fields': ['is_corporate']}),
    ]

    list_display = ('creation', 'bank', 'owner', 'number', 'is_corporate')

class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account', {'fields': ['account']}),
        ('Card', {'fields' : ['brand', 'type']}),
        ('Tier', {'fields': ['tier', 'limit']}),
        ('Number', {'fields': ['number']}),
        ('Owner', {'fields': ['owner', 'is_extension']}),
        ('Active', {'fields': ['is_active', 'expiration']})
    ]

    list_display = ('account', 'brand', 'type', 'tier', 'limit', 'number', 'owner', 'is_extension', 'is_active', 'expiration')

class BillAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Card', {'fields': ['card']}),
        ('Bill', {'fields' : ['bill_id', 'due_date']}),
        ('Period', {'fields': ['start_date', 'end_date']}),
        ('Payments', {'fields': ['min_pay', 'total_pay', 'installments_pay', 'is_paid']}),
        ('File', {'fields': ['file_link']})
    ]

    list_display = ('bill_id', 'due_date', 'is_paid')
    ordering = ('-due_date',)


class OperationBillAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bill', {'fields': ['bill']}),
        ('Date', {'fields' : ['date']}),
        ('Type', {'fields': ['type', 'authorization']}),
        ('Name', {'fields': ['name']}),
        ('Values', {'fields': ['original_value', 'agreed_rate', 'billed_rate', 'debits_and_credits', 'deferred_balance']}),
        ('Dues', {'fields': ['dues']}),
        ('Is Matched?', {'fields': ['is_matched']})
    ]

    list_display = ('date', 'type', 'name', 'original_value', 'is_matched', 'bill')
    ordering = ('-bill',)


class OperationCardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Card', {'fields': ['card']}),
        ('Date', {'fields': ['date']}),
        ('Operation', {'fields': ['type', 'amount', 'entity']}),
        ('Category', {'fields': ['category']}),
    ]

    list_display = ('date', 'type', 'entity', 'amount', 'category')
    ordering = ('-date',)


class OperationAccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account', {'fields': ['account']}),
        ('Date', {'fields': ['date']}),
        ('Operation', {'fields': ['type', 'amount', 'entity']}),
        ('Category', {'fields': ['category']}),
    ]

    list_display = ('date', 'type', 'entity', 'amount', 'category')
    ordering = ('-date',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(OperationAccount, OperationAccountAdmin)
admin.site.register(OperationCard, OperationCardAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(OperationBill, OperationBillAdmin)
