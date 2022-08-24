from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from itertools import chain

from dolar.models import Cotizacion
from cashflow.models import OperationCard, OperationAccount, Bill

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
        """Return the last five published values."""
        values = {
            "dolar": [self.get_latest_dolar('generic'), self.get_latest_dolar('blue'), self.get_latest_dolar('bna')],
            "card_ops": self.get_latest_card_ops(),
            "account_ops": self.get_latest_account_ops(),
            "combined_ops": sorted(chain(self.get_latest_account_ops(), self.get_latest_card_ops()), key=lambda instance: instance.date, reverse=True)[:8],
            "pending_bills": self.get_pending_bills()
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