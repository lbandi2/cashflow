from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from datetime import datetime, timedelta

from cashflow.models import Bill, OperationAccount, OperationBill
from .forms import EditBillOpForm


class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


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
        return {
            "unpaid": self.get_bills(),
            "paid": self.get_bills(paid=1)
            }


# class AccountsView(LoginRequiredMixin, ListView):
#     template_name = 'bills/accounts.html'
#     login_url = 'home:login'
#     context_object_name = 'item_list'

#     def bills(self):
#         return Bill.objects.order_by('-due_date') # TODO: filter by card/account

#     def get_queryset(self):
#         return {
#             "bills": self.bills()
#             }


class CardsViewDetail(ListView):
    model = Bill
    template_name = 'bills/credit_cards_view.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return OperationBill.objects.filter(bill_id=self.kwargs["bill"])

    def get_context_data(self):
        context = super(CardsViewDetail, self).get_context_data()
        bill = Bill.objects.get(pk=self.kwargs["bill"])
        context["bill"] = bill
        context["bill_card_ops"] = bill.unmatched_card_ops()
        return context


class BillOpUpdate(RedirectToPreviousMixin, UpdateView):
    template_name = 'bills/edit_bill_op.html'
    form_class = EditBillOpForm
    model = OperationBill

    def form_valid(self, form):
        self.object = form.save()
        if form.has_changed():
            if form.cleaned_data['ops']:
                bill_op = OperationBill.objects.get(pk=self.object.id)
                bill = Bill.objects.get(pk=bill_op.bill_id)
                bill_op.op_match = form.cleaned_data.get('ops')
                bill_op.is_matched = True
                bill_op.save()
                if len(bill.unmatched_bill_ops()) == 0:
                    bill.has_inconsistency = False
                    bill.save()
        return HttpResponseRedirect(reverse_lazy('bills:credit_cards'))

    def get_context_data(self):
        context = super(BillOpUpdate, self).get_context_data()
        op = OperationBill.objects.get(pk=self.kwargs["pk"])
        context["op_bill"] = op
        context["bill"] = op.bill
        context["bill_card_ops_num"] = len(op.bill.unmatched_card_ops())
        context["op_card"] = op.op_match
        # print(self.kwargs)
        return context

    # def get_queryset(self):
    #     return OperationBill.objects.get(pk=self.kwargs["pk"])


# class BillOpViewDetail(LoginRequiredMixin, ListView):
# class BillOpViewDetail(LoginRequiredMixin, UpdateView):
#     template_name = 'bills/edit_bill_op.html'
#     form_class = EditBillOpForm
#     model = OperationBill
#     context_object_name = 'item_list'

#     def get_context_data(self):
#         context = super(BillOpViewDetail, self).get_context_data()
#         context["bill"] = Bill.objects.get(pk=self.kwargs["bill"])
#         context["op_bill"] = OperationBill.objects.get(pk=self.kwargs["op_bill"])
#         # print(self.kwargs)
#         return context

#     def get_queryset(self):
#         return OperationBill.objects.get(pk=self.kwargs["op_bill"])


def bill_toggle_pay(request, pk):
    bill = Bill.objects.get(pk=pk)
    if bill.is_paid:
        bill.is_paid = False
    else:
        bill.is_paid = True
    bill.save()
    return redirect('bills:credit_cards')
