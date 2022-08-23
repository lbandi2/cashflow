from django.forms import ModelForm

from cashflow.models import OperationBill

from django import forms


class EditBillOpForm(ModelForm):
    name = forms.CharField(label='Nombre', max_length=20)
    due_date = forms.DateField()

    class Meta:
        model = OperationBill
        fields = ['name']
