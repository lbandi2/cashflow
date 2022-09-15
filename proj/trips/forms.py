from django.forms import ModelForm

from cashflow.models import Trip, OperationCard, OperationAccount
from datetime import datetime, timedelta
from itertools import chain

from django import forms


with open('country_list.txt', 'r') as f:
    COUNTRIES = [(country.strip('\n'), country.strip('\n')) for country in f]

ACCOMODATIONS = [(None, ''), ('airbnb', 'Airbnb'), ('apartment', 'Departamento'), ('hotel', 'Hotel'), ('free', 'Gratis')]

SHOPPING = [('1', 'Bajo'), ('2', 'Medio'), ('3', 'Alto')]

class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'


class EditTripForm(ModelForm):
    place = forms.CharField(label='Lugar', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='País', widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-select'}))
    start_date = forms.DateField(label='Desde', widget=MyDateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(label='Hasta', widget=MyDateInput(attrs={'class': 'form-control'}))
    is_incomplete = forms.BooleanField(label='Incompleto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    car = forms.BooleanField(label='Alquiler de auto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    accomodation = forms.CharField(label='Alojamiento', required=False, widget=forms.Select(choices=ACCOMODATIONS, attrs={'class': 'form-select'}))
    shopping = forms.CharField(label='Volumen de compras', required=False, widget=forms.Select(choices=SHOPPING, attrs={'class': 'form-select'}))
    card_operations = forms.ModelMultipleChoiceField(label='Operaciones de tarjeta',
        widget = forms.CheckboxSelectMultiple,
        queryset = OperationCard.objects.none(),
        required=False
    )
    account_operations = forms.ModelMultipleChoiceField(label='Operaciones de cuenta',
        widget = forms.CheckboxSelectMultiple,
        queryset = OperationAccount.objects.none(),
        required=False
    )

    class Meta:
        model = Trip
        fields = ['is_incomplete', 'place', 'country', 'start_date', 'end_date', 'car', 'accomodation', 'shopping', 'card_operations', 'account_operations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        trip = self.instance
        # card = OperationCard.objects.filter(trip=trip)
        # account = OperationAccount.objects.filter(trip=trip)
        # operations = card.union(account).order_by('-date')
        # self.fields['operations'].queryset = card

        self.fields['card_operations'].queryset = trip.card_operations()
        self.fields['card_operations'].initial = [item.pk for item in trip.card_operations()]
        self.fields['account_operations'].queryset = trip.account_operations()
        self.fields['account_operations'].initial = [item.pk for item in trip.account_operations()]


class AddTripForm(ModelForm):
    place = forms.CharField(label='Lugar', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='País', widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-select'}))
    start_date = forms.DateField(label='Desde', widget=MyDateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(label='Hasta', widget=MyDateInput(attrs={'class': 'form-control'}))
    is_incomplete = forms.BooleanField(label='Incompleto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    car = forms.BooleanField(label='Alquiler de auto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    accomodation = forms.CharField(label='Alojamiento', required=False, widget=forms.Select(choices=ACCOMODATIONS, attrs={'class': 'form-select'}))
    shopping = forms.CharField(label='Volumen de compras', required=False, widget=forms.Select(choices=SHOPPING, attrs={'class': 'form-select'}))
    operations = forms.ModelMultipleChoiceField(label='Operaciones de los últimos 30 días',
        widget = forms.CheckboxSelectMultiple,
        queryset = OperationCard.objects.order_by('-date').filter(date__gte=datetime.now() - timedelta(days=30)),
        required=False
    )

    class Meta:
        model = Trip
        fields = ['is_incomplete', 'place', 'country', 'start_date', 'end_date', 'car', 'accomodation', 'shopping']
