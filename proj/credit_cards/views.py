from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import JsonResponse

from datetime import datetime, timedelta
import random

from cashflow.models import Card, Bill, OperationCard
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
            'pending_bills_subtotal': self.get_pending_bills_subtotal(),
            'uncategorized_ops': OperationCard.objects.order_by('-date').filter(category_id=None),
            "unbilled_spending": self.unbilled_spending_per_card(),
            "unbilled_spending_total": self.unbilled_spending(type='total'),
            "unbilled_spending_min": self.unbilled_spending(type='min')
                    }
        return queryset

    def unbilled_spending_per_card(self):
        spending = []
        for card in Card.objects.all():
            if not card.account.is_corporate and not card.type == 'debit':         # exclude corporate and debit cards
                spent_min = self.card_unbilled_spending(card.id, type='min')
                spent_total = self.card_unbilled_spending(card.id, type='total')
                spending.append([card, spent_min, spent_total])
        return spending

    def unbilled_spending(self, type):
        total = 0
        for card in Card.objects.all():
            if not card.account.is_corporate and not card.type == 'debit':         # exclude corporate and debit cards
                if type == 'total':
                    spent = self.card_unbilled_spending(card.id, type='total')
                else:
                    spent = self.card_unbilled_spending(card.id, type='min')
                total += spent
        return total

    def card_unbilled_spending(self, card_id, type):
        amount = 0
        bills = Bill.objects.order_by('-due_date').filter(card_id=card_id) # get last bill for card
        if bills:
            ops = OperationCard.objects.order_by('-date')\
                .filter(card_id=card_id)\
                .filter(date__gt=bills[0].end_date) # use last bill to get end of last billable period
            for item in ops:
                if type == 'min':
                    amount += item.amount / item.dues
                elif type == 'total':
                    amount += item.amount
        return amount

    def get_pending_bills_subtotal(self):
        subtotal = 0
        for bill in Bill.objects.order_by('-due_date').filter(is_paid=False):
            subtotal += bill.min_pay
        return subtotal


class OpUpdate(RedirectToPreviousMixin, UpdateView):
    template_name = 'credit_cards/update_op.html'
    form_class = EditOpForm
    model = OperationCard


class UnbilledSpending(ListView):
    model = Card
    template_name = 'credit_cards/unbilled_spending.html' 
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return {
            "operations": self.card_unbilled_spending(self.kwargs["card"]),
            "total": sum([item.amount for item in self.card_unbilled_spending(self.kwargs["card"])]),
            "min": sum([item.amount / item.dues for item in self.card_unbilled_spending(self.kwargs["card"])])
            }

    def get_context_data(self):
        context = super(UnbilledSpending, self).get_context_data()
        context["card"] = Card.objects.get(pk=self.kwargs["card"])
        return context

    def card_unbilled_spending(self, card_id):
        bills = Bill.objects.order_by('-due_date').filter(card_id=card_id) # get last bill for card
        if bills:
            ops = OperationCard.objects.order_by('-date')\
                .filter(card_id=card_id)\
                .filter(date__gt=bills[0].end_date) # use last bill to get end of last billable period
        return ops


# class LastOpsView(LoginRequiredMixin, ListView):
#     model = OperationCard
#     template_name = 'credit_cards/last_ops.html'
#     login_url = 'home:login'
#     context_object_name = 'item_list'
#     queryset = OperationCard.objects.all().order_by('-date')
#     paginate_by = 15


def LastOpsView(request, page):
    query = OperationCard.objects.all().order_by('-date')
    paginator = Paginator(query, per_page=15)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
    context = {"page_obj": page_object}
    return render(request, "credit_cards/last_ops.html", context)


def LastOpsView_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 15)
    query = OperationCard.objects.all().order_by('-date')
    paginator = Paginator(query, per_page)
    page_obj = paginator.get_page(page_number)
    data = [
        {
            "date": kw.date.strftime('%Y-%m-%d %H:%M'),
            "type": kw.type,
            "entity": kw.entity,
            "amount": kw.amount,
            "category": kw.category.name
        } 
        for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)


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
        all_items = [item.category.name.title() if item.category != None else 'Sin categoria' for item in list(OperationCard.objects.order_by('-date').filter(date__gte=date_start).filter(date__lt=date_end))]
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
        all_items = [item.category.name.title() if item.category != None else 'Sin categoria' for item in list(OperationCard.objects.all())]
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
