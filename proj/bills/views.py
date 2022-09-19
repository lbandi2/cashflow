# from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
# from django.urls import reverse, reverse_lazy

from cashflow.models import Bill, OperationAccount, OperationBill, OperationCard
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
        # print(f"form.cleaned_data: \n{form.cleaned_data}")
        self.object = form.save()
        if form.has_changed():
            if form.cleaned_data['ops']:
                bill_op = OperationBill.objects.get(pk=self.object.id)
                bill = Bill.objects.get(pk=bill_op.bill_id)
                if form.cleaned_data.get('ops'):
                    bill_op.op_match = form.cleaned_data.get('ops')
                    bill_op.is_matched = True
                else:
                    bill_op.op_match = None
                    bill_op.is_matched = False
                bill_op.save()
                if len(bill.unmatched_bill_ops()) == 0:
                    bill.has_inconsistency = False
                    bill.save()
        # return HttpResponseRedirect(reverse_lazy('bills:credit_cards'))
        return redirect('bills:credit_card_view', bill=bill_op.bill.id)

    def get_context_data(self, **kwargs):
        context = super(BillOpUpdate, self).get_context_data()
        tolerance = 0.2                                                # tolerance percent +-
        unmatched = self.object.bill.unmatched_card_ops()\
            .filter(amount__lte=self.object.original_value * (1 + tolerance))\
            .filter(amount__gte=self.object.original_value * (1 - tolerance))
        context["bill_card_ops_num"] = len(unmatched)
        context["bill_card_ops"] = unmatched
        context["bill_card_op_candidate"] = None

        for op in unmatched:
            if (op.amount * (1 - 0.2)) < self.object.original_value < (op.amount * (1 + 0.2)):
                context["bill_card_op_candidate"] = OperationCard.objects.get(pk=op.id)
        else:
            for op in OperationBill.objects.all():
                if op.authorization == self.object.authorization:
                    if op.original_value == self.object.original_value:
                        if op.op_match_id:
                            context["bill_card_op_candidate"] = OperationCard.objects.get(pk=op.op_match_id)
                            context["bill_card_ops"] = OperationCard.objects.filter(pk=op.op_match_id)
                            context["bill_card_ops_num"] = len(OperationCard.objects.filter(pk=op.op_match_id))
        print(context)
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

def billop_remove_cardop(request, **kwargs):
    billop = OperationBill.objects.get(pk=kwargs['pk'])
    billop.is_matched = False
    billop.op_match = None
    billop.save()
    return redirect('bills:credit_card_view', bill=billop.bill.id)

def billop_associate_cardop(request, **kwargs):
    billop = OperationBill.objects.get(pk=kwargs['pk'])
    billop.is_matched = True
    billop.op_match = OperationCard.objects.get(pk=kwargs['op'])
    billop.save()
    return redirect('bills:credit_card_view', bill=billop.bill.id)

def bill_toggle_pay(request, pk):
    bill = Bill.objects.get(pk=pk)
    if bill.is_paid:
        bill.is_paid = False
    else:
        bill.is_paid = True
    bill.save()
    return redirect('bills:credit_cards')
