from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta

from .models import Card, Account, Bill, OperationCard, OperationAccount, OperationBill


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'cashflow/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        """Return the last five published values."""
        return {}


class LastOpsView(LoginRequiredMixin, ListView):
    template_name = 'cashflow/last_ops.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self, day_offset=0):
        today = datetime.now()
        range_start = today - timedelta(days=day_offset)
        range_end = today
        return OperationCard.objects.order_by('-date').filter(date__range=[range_start.date(), range_end.date()])

    # def get_queryset(self):
    #     return self.card_operations(day_offset=15)

    def get_queryset(self):
        return {
            "operations": self.card_operations(day_offset=15),
            "cards": list(Card.objects.all())
            }


class LastOpsByDayView(LoginRequiredMixin, ListView):
    template_name = 'cashflow/last_ops_by_day.html'
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
    template_name = 'cashflow/last_ops_by_card.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def card_operations(self):
        result = dict()
        for card in Card.objects.all():
            # card_result = list()
            result[f'{card.brand} {card.number}'] = OperationCard.objects.order_by('-date').filter(card_id=card.id)[:15]
            # result[f'{card.brand} {card.number}'] = OperationAccount.objects.order_by('-date').filter(card_id=card.id)[:15]
        return result

    def get_queryset(self):
        return {
            "operations": self.card_operations(),
            "cards": Card.objects.all()
        }
