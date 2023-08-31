from django import forms
from sales.models import Advance, Payment
from masters.models import Customer

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = Advance
        fields = ('advance_number', 'date', 'state')
        widgets = {
            'advance_number': forms.TextInput(attrs={'readonly':True}),
            'date': forms.DateInput(attrs={'type':'date'})
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('contact', 'name', 'firm', 'gst', 'pan', 'aadhar', 'email', 'address', 'city', 'pincode')

    def clean_name(self):
        return self.cleaned_data['name'].title()
    
    def clean_firm(self):
        return self.cleaned_data['firm'].title()
    
    def clean_city(self):
        return self.cleaned_data['city'].title()

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('advance', 'invoice')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

PaymentFormSet = forms.inlineformset_factory(Advance, Payment, exclude=('advance','invoice',), extra=0, can_delete=True)
