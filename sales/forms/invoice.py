from django import forms
from sales.models import Invoice, Payment, Invoice_Product, Untagged, Invoice_Advance
from masters.models import Customer

class InvoiceForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs["class"] = "invoice_form_inputs"

    class Meta:
        model = Invoice
        fields = ('date', 'invoice_number', 'gst_state')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'invoice_number': forms.NumberInput(attrs={'readonly':True})
        }

class CustomerForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs["class"] = "customer_form_inputs"

    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'aadhar', 'contact', 'address', 'city', 'pincode')

class UntaggedForm(forms.ModelForm):
    class Meta:
        model = Untagged
        exclude = ('invoice',)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('advance','invoice')

widgets = {
    'subtotal': forms.NumberInput(attrs={"readonly":True}),
    'total': forms.NumberInput(attrs={"readonly":True})
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

ProductFormSet = forms.inlineformset_factory(Invoice, Invoice_Product, fields=fields, extra=0, can_delete=True, widgets=widgets)

UntaggedFormSet = forms.inlineformset_factory(Invoice, Untagged, fields="__all__", extra=0, can_delete=True)

AdvanceFormSet = forms.inlineformset_factory(Invoice, Invoice_Advance, fields=('advance',), extra=0, can_delete=True, widgets={'advance': forms.NumberInput(attrs={'readonly': True})})

widgets = {
    "method": forms.TextInput(attrs={"readonly":True}),
    "amount": forms.TextInput(attrs={"readonly":True}),
    "date": forms.TextInput(attrs={"readonly":True}),
    "name": forms.TextInput(attrs={"readonly":True}),
    "card_bank": forms.HiddenInput(),
    "card_number": forms.HiddenInput(),
    "cheque_number": forms.HiddenInput(),
    "cheque_branch": forms.HiddenInput(),
    "cheque_account_number": forms.HiddenInput(),
    "cheque_ifsc": forms.HiddenInput(),
    "upi_vpa": forms.HiddenInput(),
    "upi_mobile": forms.HiddenInput(),
    "wire_account_number": forms.HiddenInput(),
    "wire_utr": forms.HiddenInput(),
    "wire_bank": forms.HiddenInput()
}

PaymentFormSet = forms.inlineformset_factory(Invoice, Payment, exclude=('advance','invoice',), extra=0, can_delete=True, widgets=widgets)