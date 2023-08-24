from django import forms
from sales.models import Advance, Payment
from masters.models import Customer

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = Advance
        fields = ('advance_number', 'date', 'state')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'aadhar', 'contact', 'email', 'address', 'city', 'pincode')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('advance', 'invoice')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

PaymentFormSet = forms.inlineformset_factory(Advance, Payment, exclude=('advance','invoice',), extra=0, can_delete=True)
