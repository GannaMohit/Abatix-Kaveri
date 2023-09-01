from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from sales.models import Invoice, Payment, Invoice_Product, Untagged, Invoice_Advance, Advance
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
        fields = ('contact', 'name', 'firm', 'gst', 'pan', 'aadhar', 'address', 'city', 'pincode')

    def clean_name(self):
        return self.cleaned_data['name'].title()
    
    def clean_firm(self):
        return self.cleaned_data['firm'].title()
    
    def clean_city(self):
        return self.cleaned_data['city'].title()

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advance'].queryset = Advance.objects.filter(redeemed=False)

ProductFormSet = forms.inlineformset_factory(Invoice, Invoice_Product, fields=fields, extra=0, can_delete=True)

UntaggedFormSet = forms.inlineformset_factory(Invoice, Untagged, fields="__all__", extra=0, can_delete=True)

AdvanceFormSet = forms.inlineformset_factory(Invoice, Invoice_Advance, fields=('advance',), extra=0, can_delete=True)

PaymentFormSet = forms.inlineformset_factory(Invoice, Payment, exclude=('advance','invoice',), extra=0, can_delete=True)