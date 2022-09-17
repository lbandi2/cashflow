from django.forms import ModelForm

from cashflow.models import OperationCategories, Keyword

from django import forms


class EditCatForm(ModelForm):
    name = forms.CharField(label='Nombre', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OperationCategories
        fields = ['name']

class AddKwForm(ModelForm):
    name = forms.CharField(label='Nombre', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # category = forms.ModelChoiceField(label='Categoría', queryset=OperationCategories.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Keyword
        # fields = ['name', 'category']
        fields = ['name']

    # def __init__(self, *args, **kwargs):
    #     # category = kwargs.pop('category')
    #     print(self.kwargs)
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].initial = category
    # #     self.fields['category'].widget = forms.HiddenInput()
