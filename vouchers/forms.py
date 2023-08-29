from django.forms import ModelForm, inlineformset_factory, DateInput, TextInput, NumberInput, HiddenInput
from vouchers.models import Voucher, Particular, Voucher_Product
from masters.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('contact', 'name', 'firm', 'gst', 'pan', 'aadhar', 'email', 'address', 'city', 'pincode')

class VoucherForm(ModelForm):
    class Meta:
        model = Voucher
        fields = ('voucher_number', 'type', 'date', 'state')
        widgets = {
            'voucher_number': NumberInput(attrs={'readonly':True}),
            'date': DateInput(attrs={'type':'date'})
        }

class ParticularForm(ModelForm):
    class Meta:
        model = Particular
        exclude = ('voucher',)
        widgets = {
            'net_weight': NumberInput(attrs={'readonly':True})
        }

ProductFormSet = inlineformset_factory(Voucher, Voucher_Product, exclude=('voucher',), extra=0, can_delete=True)

ParticularFormSet = inlineformset_factory(Voucher, Particular, exclude=('voucher',), extra=0, can_delete=True)
