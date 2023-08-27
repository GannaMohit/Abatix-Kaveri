from django import forms
from sales.models import Invoice, Payment, Invoice_Product, Untagged, Invoice_Advance
from masters.models import Customer

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('date', 'invoice_number', 'state')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'invoice_number': forms.NumberInput(attrs={'readonly':True})
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'aadhar', 'contact', 'address', 'city', 'pincode')

class UntaggedForm(forms.ModelForm):
    class Meta:
        model = Untagged
        exclude = ('invoice',)
        widgets = {
            'net_weight': forms.NumberInput(attrs={'readonly':True})
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('advance','invoice')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
        }

fields = (
    'product',
    'rate',
    'subtotal',
    'sgst',
    'cgst',
    'igst',
    'tcs',
    'total'
)

class InvoiceAdvanceForm(forms.ModelForm):
    class Meta:
        model = Invoice_Advance
        fields = ('advance',)

ProductFormSet = forms.inlineformset_factory(Invoice, Invoice_Product, fields=fields, extra=0, can_delete=True)

UntaggedFormSet = forms.inlineformset_factory(Invoice, Untagged, fields="__all__", extra=0, can_delete=True)

AdvanceFormSet = forms.inlineformset_factory(Invoice, Invoice_Advance, fields=('advance',), extra=0, can_delete=True)

PaymentFormSet = forms.inlineformset_factory(Invoice, Payment, exclude=('advance','invoice',), extra=0, can_delete=True)