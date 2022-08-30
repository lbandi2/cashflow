from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from itertools import chain

from dolar.models import Cotizacion
from cashflow.models import OperationCard, OperationAccount, Bill, Card

# class PortalNavBar(LoginRequiredMixin, ListView):
#     template_name = 'portal/base.html'
#     login_url = 'home:login'
#     context_object_name = 'data'

#     def get_queryset(self):
#         """Return the last five published values."""
#         values = {
#             "pending_bills": self.get_pending_bills()
#         }
#         return values

class PortalView(LoginRequiredMixin, ListView):
    template_name = 'portal/index.html'
    login_url = 'home:login'
    context_object_name = 'data'

    def get_queryset(self):
        # print(self.kwargs)

        """Return the last five published values."""
        values = {
            "dolar": [self.get_latest_dolar('generic'), self.get_latest_dolar('blue'), self.get_latest_dolar('bna')],
            "card_ops": self.get_latest_card_ops(),
            "account_ops": self.get_latest_account_ops(),
            "combined_ops": sorted(chain(self.get_latest_account_ops(), self.get_latest_card_ops()), key=lambda instance: instance.date, reverse=True)[:8],
            "pending_bills": self.get_pending_bills(),
            "pending_bills_subtotal": self.get_pending_bills_subtotal(),
            "unbilled_spending": self.unbilled_spending_per_card(),
            "unbilled_spending_total": self.unbilled_spending_total()
        }
        return values

    def get_latest_dolar(self, name):
        return Cotizacion.objects.order_by('-datetime').filter(name=name)[:2]

    def get_latest_card_ops(self):
        return OperationCard.objects.order_by('-date')[:10]

    def get_latest_account_ops(self):
        return OperationAccount.objects.order_by('-date')[:10]

    def get_pending_bills(self):
        return Bill.objects.order_by('-due_date').filter(is_paid=False)

    def get_pending_bills_subtotal(self):
        subtotal = 0
        for bill in Bill.objects.order_by('-due_date').filter(is_paid=False):
            subtotal += bill.min_pay
        return subtotal

    def unbilled_spending_per_card(self):
        spending = []
        for card in Card.objects.all():
            if not card.account.is_corporate and not card.type == 'debit':         # exclude corporate and debit cards
                spent = self.card_unbilled_spending(card.id)
                spending.append([card, spent])
        return spending

    def unbilled_spending_total(self):
        total = 0
        for card in Card.objects.all():
            if not card.account.is_corporate and not card.type == 'debit':         # exclude corporate and debit cards
                spent = self.card_unbilled_spending(card.id)
                total += spent
        return total

    def card_unbilled_spending(self, card_id):
        amount = 0
        bills = Bill.objects.order_by('-due_date').filter(card_id=card_id) # get last bill for card
        if bills:
            ops = OperationCard.objects.order_by('-date')\
                .filter(card_id=card_id)\
                .filter(date__gt=bills[0].end_date) # use last bill to get end of last billable period
            for item in ops:
                amount += item.amount / item.dues
        return amount


class PortalSettings(LoginRequiredMixin, ListView):
    template_name = 'portal/settings.html'
    login_url = 'home:login'
    context_object_name = 'data'

    def get_queryset(self):
        return {}