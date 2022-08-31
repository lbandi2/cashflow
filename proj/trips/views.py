from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.http import request, HttpResponseRedirect

from datetime import datetime, timedelta

from cashflow.models import OperationCard, Trip
from .forms import AddTripForm, EditTripForm


class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


# class TripEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
#     template_name = 'trips/edit_trip.html'
#     form_class = EditTripForm
#     model = Trip

#     def get_context_data(self):
#         context = super(TripEditView, self).get_context_data()
#         context["obj"] = self.object
#         context["title"] = "Edit item"
#         context["trip"] = self.object.id
#         context["operations"] = OperationCard.objects\
#             .filter(date__gte=self.object.start_date - timedelta(days=3))\
#             .filter(date__lte=self.object.end_date + timedelta(days=3))
#         return context

# class TripEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView): #TODO: redirect mixin goes back more than once, weird
class TripEditView(LoginRequiredMixin, UpdateView):
    template_name = 'trips/edit_trip.html'
    form_class = EditTripForm
    model = Trip
    success_url = reverse_lazy('trips:index')

    def form_valid(self, form):
        # print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self):
        context = super(TripEditView, self).get_context_data()
        return context

    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        trip = Trip.objects.get(id=id_)
        if trip.start_date < datetime.now().date():
            operations = OperationCard.objects\
                .filter(date__gte=trip.start_date - timedelta(days=3))\
                .filter(date__lte=trip.end_date + timedelta(days=3))
        else:
            operations = OperationCard.objects.order_by('-date')\
                .filter(date__gte=datetime.now() - timedelta(days=30))
        operations_id = [op.id for op in operations]
        return render(request, self.template_name, {
                                                    'trip': trip.id,
                                                    'operations': operations,
                                                    'operations_id': operations_id,
                                                    'form': EditTripForm(instance=trip)
                                                    }
                                                )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        checked_ops = {int(item.strip('_is_checked')) for item in list(request.POST.keys()) if 'is_checked' in item}
        all_ops = {int(item) for item in request.POST['operations_id'].strip('[').strip(']').split(', ')}
        update_true = []
        update_false = []
        for item in all_ops:
            op = OperationCard.objects.get(pk=item)
            if item in checked_ops and op.trip_id is None:
                op.trip_id = self.object.id
                update_true.append(op.id)
            elif item not in checked_ops and op.trip_id is not None:
                op.trip_id = None
                update_false.append(op.id)
            # op.save()
        OperationCard.objects.filter(id__in=update_true).update(trip_id = self.object.id)
        OperationCard.objects.filter(id__in=update_false).update(trip_id = None)
        return super().post(request, *args, **kwargs)


class TripIndexView(LoginRequiredMixin, ListView):
    template_name = 'trips/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        trips = Trip.objects.all()
        return {
            'trips': trips,
            }


class TripAddView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    template_name = 'trips/add.html'
    form_class = AddTripForm
    model = Trip
    login_url = 'home:login'

    def get_context_data(self):
        context = super(TripAddView, self).get_context_data()
        context["title"] = "Agregar"
        return context


class TripDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'trips/delete.html'
    model = Trip
    success_url = reverse_lazy('trips:index')