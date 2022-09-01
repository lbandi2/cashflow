from django.forms import ModelForm

from cashflow.models import OperationCard, Trip
# from .models import Trip

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

    class Meta:
        model = Trip
        fields = ['is_incomplete', 'place', 'country', 'start_date', 'end_date', 'car', 'accomodation', 'shopping']


class AddTripForm(ModelForm):
    place = forms.CharField(label='Lugar', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='País', widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-select'}))
    start_date = forms.DateField(label='Desde', widget=MyDateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(label='Hasta', widget=MyDateInput(attrs={'class': 'form-control'}))
    is_incomplete = forms.BooleanField(label='Incompleto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    car = forms.BooleanField(label='Alquiler de auto', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    accomodation = forms.CharField(label='Alojamiento', required=False, widget=forms.Select(choices=ACCOMODATIONS, attrs={'class': 'form-select'}))
    shopping = forms.CharField(label='Volumen de compras', required=False, widget=forms.Select(choices=SHOPPING, attrs={'class': 'form-select'}))

    class Meta:
        model = Trip
        fields = ['is_incomplete', 'place', 'country', 'start_date', 'end_date', 'car', 'accomodation', 'shopping']
