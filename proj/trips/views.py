from multiprocessing.sharedctypes import Value
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.http import request, HttpResponseRedirect

from datetime import datetime, timedelta

from itertools import chain

from cashflow.models import OperationCard, OperationAccount, Trip
from .forms import AddTripForm, EditTripForm


class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class TripIndexView(LoginRequiredMixin, ListView):
    template_name = 'trips/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        trips = Trip.objects.all().order_by('-start_date')
        return {
            'trips': trips,
            }


# class TripEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView): #TODO: redirect mixin goes back more than once, weird
class TripEditView(LoginRequiredMixin, UpdateView):
    template_name = 'trips/edit_trip.html'
    form_class = EditTripForm
    model = Trip
    success_url = reverse_lazy('trips:index')

    def form_valid(self, form):
        print(form.cleaned_data)
        self.object = form.save()
        card = OperationCard.objects.filter(trip=self.object)
        account = OperationAccount.objects.filter(trip=self.object)
        # operations = card.union(account)
        if form.has_changed():
            for operation in card:
                if operation in form.cleaned_data.get('card_operations'):
                    operation.trip = self.object
                else:
                    operation.trip = None
                operation.save()
            for operation in account:
                if operation in form.cleaned_data.get('account_operations'):
                    operation.trip = self.object
                else:
                    operation.trip = None
                operation.save()
        # return HttpResponseRedirect(reverse_lazy('trips:index'))
        return redirect('trips:index')

class TripAddView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    template_name = 'trips/add_trip.html'
    form_class = AddTripForm
    model = Trip
    success_url = reverse_lazy('trips:index')

    def form_valid(self, form):
        self.object = form.save()
        for item in form.cleaned_data.get('operations'):
            item.trip = self.object
            item.save()

        return HttpResponseRedirect(reverse_lazy('trips:index'))


class TripDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'trips/delete.html'
    model = Trip
    success_url = reverse_lazy('trips:index')