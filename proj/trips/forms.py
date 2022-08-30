from django.forms import ModelForm

from cashflow.models import OperationCard, Trip
# from .models import Trip

from django import forms


with open('country_list.txt', 'r') as f:
    COUNTRIES = [(country.strip('\n'), country.strip('\n')) for country in f]


class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'


class EditTripForm(ModelForm):
    place = forms.CharField(label='Lugar', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='País', widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-select'}))
    start_date = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Trip
        fields = ['place', 'country', 'start_date', 'end_date']


class AddTripForm(ModelForm):
    place = forms.CharField(label='Lugar', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='País', widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-select'}))
    start_date = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Trip
        fields = ['place', 'country', 'start_date', 'end_date']
