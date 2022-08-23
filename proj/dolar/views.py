from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime, timedelta

from django.views.generic import TemplateView

from .models import Cotizacion


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'dolar/index.html'
    login_url = 'home:login'
    context_object_name = 'latest_quote_list'

    def get_latest_ars(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(name='blue')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='bna')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='bbva')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='santander')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='patagonia')[:2],
        ]

    def get_latest_cop(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(currency='cop')[:2],
        ]

    def get_queryset(self):
        """Return the last five published values."""
        return {"ars": self.get_latest_ars(), "cop": self.get_latest_cop()}


class ArchiveView(LoginRequiredMixin, ListView):
    template_name = 'dolar/archive.html'
    context_object_name = 'quote_list'
    login_url = 'home:login'

    def get_last_entries(self, currency, name, days_back=15):
        today = datetime.now().date()
        date_end = today - timedelta(days=days_back)
        cotiz = Cotizacion.objects.order_by('-datetime').filter(currency=currency).filter(name=name).filter(datetime__gte = date_end)
        return list(cotiz)

    def get_ars(self):
        blue = self.get_last_entries('ars', 'blue')
        bna = self.get_last_entries('ars', 'bna')
        bbva = self.get_last_entries('ars', 'bbva')
        santander = self.get_last_entries('ars', 'santander')
        patagonia = self.get_last_entries('ars', 'patagonia')
        return [blue, bna, bbva, santander, patagonia]

    def get_cop(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(currency='cop')[:50],
        ]


    def get_queryset(self):
        """Return the last five published values."""
        return {"ars": self.get_ars(), "cop": self.get_cop()}


class HistoryView(LoginRequiredMixin, ListView):
    template_name = 'dolar/history.html'
    context_object_name = 'quote_list'
    login_url = 'home:login'

    def __init__(self, currency, name):
        self.currency = currency
        self.name = name

    def get_last_entries(self, currency, name, days_back=15):
        today = datetime.now().date()
        date_end = today - timedelta(days=days_back)
        cotiz = Cotizacion.objects.order_by('-datetime').filter(currency=currency).filter(name=name).filter(datetime__gte = date_end)
        return list(cotiz)

    def get_values(self):
        values = self.get_last_entries(self.currency, self.name)
        return values

    def get_queryset(self):
        """Return the last value for earch day."""
        return {"values": self.get_values()}


class BNAHistory(HistoryView):
    def __init__(self, currency='ars', name='bna'):
        super().__init__(currency, name)


class BBVAHistory(HistoryView):
    def __init__(self, currency='ars', name='bbva'):
        super().__init__(currency, name)


class BlueHistory(HistoryView):
    def __init__(self, currency='ars', name='blue'):
        super().__init__(currency, name)


class SantanderHistory(HistoryView):
    def __init__(self, currency='ars', name='santander'):
        super().__init__(currency, name)


class PatagoniaHistory(HistoryView):
    def __init__(self, currency='ars', name='patagonia'):
        super().__init__(currency, name)


class COPHistory(HistoryView):
    def __init__(self, currency='cop', name='generic'):
        super().__init__(currency, name)


class DetailView(LoginRequiredMixin, DetailView):
    model = Cotizacion
    template_name = 'home/detail.html'
    context_object_name = 'quote'
    login_url = 'quotes:login'



