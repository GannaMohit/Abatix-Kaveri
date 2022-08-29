from django import forms
from sales.models import Invoice, Payment
from masters.models import Customer

class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "invoice_form_inputs"

    class Meta:
        model = Invoice
        fields = ('date', 'invoice_number', 'gst_invoice', 'gst_state')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "customer_form_inputs"

    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'contact', 'aadhar', 'email', 'address', 'pincode', 'city', 'state')
