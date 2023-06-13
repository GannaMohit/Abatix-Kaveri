from django.forms import ModelForm, inlineformset_factory, DateInput, TextInput, NumberInput, HiddenInput
from vouchers.models import Voucher, Particular
from masters.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'contact', 'email', 'address', 'city', 'pincode', 'state')

class VoucherForm(ModelForm):
    class Meta:
        model = Voucher
        fields = ('type', 'voucher_number', 'date')
        widgets = {
            'date': DateInput(attrs={'type':'date'})
        }

class ParticularForm(ModelForm):
    class Meta:
        model = Particular
        exclude = ('voucher',)

widgets = {
    'metal': HiddenInput(attrs={'readonly':True}),
    'category': HiddenInput(attrs={'readonly':True}),
    'purity': HiddenInput(attrs={'readonly':True}),
    'gross_weight': TextInput(attrs={'readonly':True}),
    'net_weight': TextInput(attrs={'readonly':True}),
    'rate': TextInput(attrs={'readonly':True}),
    'subtotal': TextInput(attrs={'readonly':True}),
    'sgst': HiddenInput(attrs={'readonly':True}),
    'cgst': HiddenInput(attrs={'readonly':True}),
    'igst': HiddenInput(attrs={'readonly':True}),
    'tcs': HiddenInput(attrs={'readonly':True}),
    'total': TextInput(attrs={'readonly':True})
}

fields = ('metal', 'purity', 'category', 'gross_weight', 'net_weight', 'rate', 'subtotal', 'sgst', 'cgst', 'igst', 'tcs', 'total')
ParticularFormSet = inlineformset_factory(Voucher, Particular, fields=fields, extra=0, can_delete=True, widgets=widgets)
