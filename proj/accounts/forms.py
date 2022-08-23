from django.forms import ModelForm

from cashflow.models import OperationAccount, OperationCategories, AccountCategories

from django import forms


CATEGORIES = sorted({(item.name, item.name) for item in OperationCategories.objects.all()})
ACCOUNT_CATEGORIES = sorted({(item.name, item.name) for item in AccountCategories.objects.all()})


class EditOpForm(ModelForm):
    date = forms.DateTimeField(label='Fecha', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    type = forms.CharField(label='Tipo', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    amount = forms.FloatField(label='Monto', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    entity = forms.CharField(label='Entidad', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    category = forms.CharField(label='Categoría', max_length=20, widget=forms.Select(choices=sorted(CATEGORIES + ACCOUNT_CATEGORIES)))

    class Meta:
        model = OperationAccount
        fields = ('id', 'date', 'type', 'entity', 'amount', 'category')

# class PasswordForm(PasswordChangeForm):
#     old_password = forms.CharField(label='Current password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
#     new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
#     new_password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password1', 'new_password2')
