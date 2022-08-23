from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from datetime import datetime, timedelta

from cashflow.models import Card, Account, Bill, OperationCard, OperationAccount, OperationBill
from .forms import EditBillOpForm

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'bills/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        """Return the last five published values."""
        return {}

class CardsView(LoginRequiredMixin, ListView):
    model = Bill
    template_name = 'bills/credit_cards.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_bills(self, paid=0):
        return Bill.objects.order_by('-due_date').filter(is_paid=paid) # TODO: filter by card/account

    def get_queryset(self):
        print(self.kwargs)
        return {
            "unpaid": self.get_bills(),
            "paid": self.get_bills(paid=1)
            }


class AccountsView(LoginRequiredMixin, ListView):
    template_name = 'bills/accounts.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def bills(self):
        return Bill.objects.order_by('-due_date') # TODO: filter by card/account

    def get_queryset(self):
        return {
            "bills": self.bills()
            }


class CardsViewDetail(ListView):
    model = Bill
    template_name = 'bills/credit_cards_view.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return OperationBill.objects.filter(bill_id=self.kwargs["bill"])

    def get_context_data(self):
        context = super(CardsViewDetail, self).get_context_data()
        context["bill"] = Bill.objects.get(pk=self.kwargs["bill"])
        return context


class BillOpViewDetail(LoginRequiredMixin, ListView):
    template_name = 'bills/edit_bill_op.html'
    # form_class = EditBillOpForm
    model = OperationBill
    context_object_name = 'item_list'

    def get_context_data(self):
        context = super(BillOpViewDetail, self).get_context_data()
        context["bill"] = Bill.objects.get(pk=self.kwargs["bill"])
        context["op_bill"] = OperationBill.objects.get(pk=self.kwargs["op_bill"])
        print(self.kwargs)
        return context

    def get_queryset(self):
        return OperationBill.objects.get(pk=self.kwargs["op_bill"])


class AccountsViewDetail(ListView):
    template_name = 'bills/accounts_view.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return OperationAccount.objects.filter(bill_id=self.kwargs["id"])


def bill_toggle_pay(request, pk):
    bill = Bill.objects.get(pk=pk)
    if bill.is_paid:
        bill.is_paid = False
    else:
        bill.is_paid = True
    bill.save()
    return redirect('bills:credit_card_view', pk)

# google timeline
# https://timeline.google.com/maps/timeline?pb=!1m2!1m1!1s2022-06-14