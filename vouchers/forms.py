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
        exclude = ('customer',)
        widgets = {
            'date': DateInput(attrs={'type':'date'}),
            'gross_weight': NumberInput(attrs={'readonly':True}),
            'net_weight': NumberInput(attrs={'readonly':True}),
            'pure_weight': NumberInput(attrs={'readonly':True}),
            'amount': NumberInput(attrs={'readonly':True})
        }

class ParticularForm(ModelForm):
    class Meta:
        model = Particular
        exclude = ('voucher',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["oninput"] = "updateValues(false)"

        self.fields["gross_weight"].label= "Gross Weight"
        self.fields["net_weight"].label= "Net Weight"

widgets = {
    'metal': HiddenInput(attrs={'readonly':True}),
    'category': HiddenInput(attrs={'readonly':True}),
    'purity': HiddenInput(attrs={'readonly':True}),
    'gross_weight': NumberInput(attrs={'readonly':True}),
    'net_weight': NumberInput(attrs={'readonly':True}),
    'rate': NumberInput(attrs={'readonly':True}),
    'subtotal': NumberInput(attrs={'readonly':True}),
    'sgst': HiddenInput(attrs={'readonly':True}),
    'cgst': HiddenInput(attrs={'readonly':True}),
    'igst': HiddenInput(attrs={'readonly':True}),
    'tcs': HiddenInput(attrs={'readonly':True}),
    'total': NumberInput(attrs={'readonly':True})
}

fields = ('metal', 'purity', 'category', 'gross_weight', 'net_weight', 'rate', 'subtotal', 'sgst', 'cgst', 'igst', 'tcs', 'total')
ParticularFormSet = inlineformset_factory(Voucher, Particular, fields=fields, extra=0, can_delete=True, widgets=widgets)
