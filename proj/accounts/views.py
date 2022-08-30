from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from datetime import datetime, timedelta

from cashflow.models import Account, OperationAccount
from .forms import EditOpForm


class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'accounts/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = {
            'last_ops': OperationAccount.objects.order_by('-date')[:5],
            'pending_bills': [],
            'uncategorized_ops': OperationAccount.objects.order_by('-date').filter(category='')
                    }
        return queryset


class OpUpdate(RedirectToPreviousMixin, UpdateView):
    template_name = 'accounts/update_op.html'
    form_class = EditOpForm
    model = OperationAccount

    def get_context_data(self):
        context = super(OpUpdate, self).get_context_data()
        context["obj"] = self.object
        context["account"] = self.object.account
        context["title"] = "Edit item"
        return context


class LastOpsView(LoginRequiredMixin, ListView):
    model = OperationAccount
    template_name = 'accounts/last_ops.html'
    login_url = 'home:login'
    context_object_name = 'item_list'
    queryset = OperationAccount.objects.all().order_by('-date')
    paginate_by = 15


class LastOpsByDayView(LoginRequiredMixin, ListView):
    template_name = 'accounts/last_ops_by_day.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self, day_offset=0):
        today = datetime.now()
        range_start = today - timedelta(days=day_offset)
        range_end = range_start + timedelta(days=1)
        return OperationAccount.objects.order_by('-date').filter(date__range=[range_start.date(), range_end.date()])

    def get_queryset(self):
        result = dict()
        counter = 0

        days = [
            "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
        ]

        today = datetime.today()

        for item in range(0, 7): # Returns last 5 days
            result[f"{days[(today - timedelta(days=counter)).weekday()]} {(today - timedelta(days=counter)).strftime('%d/%m')}"] = self.card_operations(day_offset=counter)
            counter += 1

        return {
            "operations": result,
            "accounts": Account.objects.all()
        }


class LastOpsByAccountView(LoginRequiredMixin, ListView):
    template_name = 'accounts/last_ops_by_account.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self):
        result = dict()
        for account in Account.objects.all():
            # card_result = list()
            result[f'{account.owner} {account.number}'] = OperationAccount.objects.order_by('-date').filter(account_id=account.id)[:15]
            # result[f'{card.brand} {card.number}'] = OperationAccount.objects.order_by('-date').filter(card_id=card.id)[:15]
        return result

    def get_queryset(self):
        return {
            "operations": self.card_operations(),
            "accounts": Account.objects.all()
        }
