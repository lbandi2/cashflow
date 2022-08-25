from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from datetime import datetime, timedelta
import random
import calendar

from cashflow.models import Card, Account, Bill, OperationCard, OperationAccount, OperationBill, OperationCategories
from .forms import EditOpForm


class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'credit_cards/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = {
            'last_ops': OperationCard.objects.order_by('-date')[:5],
            'pending_bills': Bill.objects.order_by('-due_date').filter(is_paid=False),
            'uncategorized_ops': OperationCard.objects.order_by('-date').filter(category='')
                    }
        return queryset


class OpUpdate(RedirectToPreviousMixin, UpdateView):
    template_name = 'credit_cards/update_op.html'
    form_class = EditOpForm
    model = OperationCard

    def get_context_data(self):
        context = super(OpUpdate, self).get_context_data()
        context["obj"] = self.object
        context["card"] = self.object.card
        context["title"] = "Edit item"
        return context


class LastOpsView(LoginRequiredMixin, ListView):
    model = OperationCard
    template_name = 'credit_cards/last_ops.html'
    login_url = 'home:login'
    context_object_name = 'item_list'
    queryset = OperationCard.objects.all().order_by('-date')
    paginate_by = 15

class LastOpsByDayView(LoginRequiredMixin, ListView):
    template_name = 'credit_cards/last_ops_by_day.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self, day_offset=0):
        today = datetime.now()
        range_start = today - timedelta(days=day_offset)
        range_end = range_start + timedelta(days=1)
        return OperationCard.objects.order_by('-date').filter(date__range=[range_start.date(), range_end.date()])

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
            "cards": Card.objects.all()
        }


class LastOpsByCardView(LoginRequiredMixin, ListView):
    template_name = 'credit_cards/last_ops_by_card.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self):
        result = dict()
        for card in Card.objects.all():
            result[f'{card.brand} {card.number}'] = OperationCard.objects.order_by('-date').filter(card_id=card.id)[:15]
        return result

    def get_queryset(self):
        return {
            "operations": self.card_operations(),
            "cards": Card.objects.all()
        }


class ChartsView(ListView):
    template_name = 'credit_cards/charts.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def chart_ops_range(self, date_start, date_end, top=0):
        res = {}
        all_items = [item.category.title() if item.category != '' else 'Sin categoria' for item in list(OperationCard.objects.order_by('-date').filter(date__gte=date_start).filter(date__lt=date_end))]
        for item in all_items:
            res[item] = all_items.count(item)
        max_values = res
        if top != 0:
            section = slice(0, top)
            max_values = dict(sorted(res.items(), key=lambda x: x[1], reverse=True)[section])
        colors = []
        for _ in range(len(max_values)):
            rand_color = ["#"+''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
            colors.extend(rand_color)
        return {"keys": list(max_values.keys()), "values": list(max_values.values()), "colors": colors}

    def chart_all_ops(self, top=0):
        res = {}
        all_items = [item.category.title() if item.category != '' else 'Sin categoria' for item in list(OperationCard.objects.all())]
        for item in all_items:
            res[item] = all_items.count(item)
        max_values = res
        if top != 0:
            section = slice(0, top)
            max_values = dict(sorted(res.items(), key=lambda x: x[1], reverse=True)[section])
        colors = []
        for _ in range(len(max_values)):
            rand_color = ["#"+''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
            colors.extend(rand_color)
        return {"keys": list(max_values.keys()), "values": list(max_values.values()), "colors": colors}

    def get_queryset(self):
        dt = datetime.now()
        dt_last = (dt.replace(day=1) + timedelta(days=32)).replace(day=1)
        start = dt.replace(day=1).strftime('%Y-%m-%d')
        end = dt_last.strftime('%Y-%m-%d')
        return {
            "por_categoria": self.chart_all_ops(),
            "este_mes": self.chart_ops_range(date_start=start, date_end=end)
            }
