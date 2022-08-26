from django.forms import ModelForm

from cashflow.models import OperationCard, OperationCategories

from django import forms


CATEGORIES = sorted({(item.name, item.name) for item in OperationCategories.objects.all()})

class EditOpForm(ModelForm):
    date = forms.DateTimeField(label='Fecha', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(label='Tipo', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.FloatField(label='Monto', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    entity = forms.CharField(label='Entidad', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dues = forms.CharField(label='Cuotas', widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label='Categoría', max_length=20, widget=forms.Select(choices=CATEGORIES, attrs={'class': 'form-control'}))

    class Meta:
        model = OperationCard
        fields = ('id', 'date', 'type', 'entity', 'amount', 'category', 'dues')

# class PasswordForm(PasswordChangeForm):
#     old_password = forms.CharField(label='Current password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
#     new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
#     new_password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password1', 'new_password2')
