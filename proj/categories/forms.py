from django.forms import ModelForm

from cashflow.models import OperationCategories, Keyword

from django import forms


class EditCatForm(ModelForm):
    name = forms.CharField(label='Nombre', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OperationCategories
        fields = ['name']

# class EditCatForm(ModelForm):
#     name = forms.CharField(label='Nombre', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     kw_name = forms.CharField(label='Frase o palabra', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = OperationCategories
#         fields = ['name']


class AddKwForm(ModelForm):
    name = forms.CharField(label='Frase o palabra', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Keyword
        fields = ['name']
