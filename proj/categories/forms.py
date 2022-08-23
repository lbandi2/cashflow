from django.forms import ModelForm

from cashflow.models import OperationCategories

from django import forms


# CATEGORIES = sorted({(item.name, item.name) for item in OperationCategories.objects.all()})


class EditCatForm(ModelForm):
    name = forms.CharField(label='Nombre', max_length=20)

    class Meta:
        model = OperationCategories
        fields = ['name']
