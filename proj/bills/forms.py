from django.forms import ModelForm

from cashflow.models import OperationBill, OperationCard, Bill

from django import forms


class EditBillOpForm(ModelForm):
    date = forms.DateField(label='Fecha', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(label='Tipo', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    authorization = forms.CharField(label='Autorización', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Entidad', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    original_value = forms.FloatField(label='Valor Original', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dues = forms.CharField(label='Cuotas', disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ops = forms.ModelChoiceField(label='Operaciones del período',
        widget = forms.RadioSelect,
        queryset = OperationCard.objects.none(),
        required=False
    )

    class Meta:
        model = OperationBill
        fields = ('date', 'type', 'authorization', 'name', 'original_value', 'dues', 'ops')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opbill = self.instance
        bill = opbill.bill
        card_ops = OperationCard.objects.all()
        bill_ops = OperationBill.objects.all()
        if opbill.type != 'expense':
            self.fields['ops'].queryset = card_ops.none()
        elif card_ops.filter(id=opbill.op_match_id):
            self.fields['ops'].queryset = card_ops.filter(id=opbill.op_match_id)
            # self.fields['ops'] = forms.ModelChoiceField(label='Operaciones',
            #     widget = forms.CheckboxSelectMultiple,
            #     queryset = card_ops.filter(id=opbill.op_match_id),
            #     required=False
            # )
            self.fields['ops'].initial = [item.pk for item in card_ops.filter(id=opbill.op_match_id)]
        else:
            unmatched = bill.unmatched_card_ops()
            filtered = unmatched.exclude(id__in=bill_ops)
            # self.fields['ops'].queryset = bill.unmatched_card_ops()
            self.fields['ops'].queryset = filtered

