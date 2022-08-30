from django.forms import ModelForm

from cashflow.models import OperationBill

from django import forms


class EditBillOpForm(ModelForm):
    date = forms.DateField(label='Fecha', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(label='Tipo', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    authorization = forms.FloatField(label='Autorización', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.FloatField(label='Entidad', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    original_value = forms.FloatField(label='Valor Original', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OperationBill
        fields = ('date', 'type', 'authorization', 'name', 'original_value')
