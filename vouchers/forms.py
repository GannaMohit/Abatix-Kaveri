from django import forms
from vouchers.models import Voucher, Particular

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ('type', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

# widgets = {
#     'product': forms.NumberInput(attrs={
#         'placeholder':"Add",
#         'onfocus':'addRow(this)',
#         'oninput':"validateID(this, '/stock/_fetch_product')"
#     })
# }
# ProductFormSet = forms.inlineformset_factory(Voucher, Voucher_Particulars, fields=('product',), extra=0, can_delete=True, widgets=widgets)
