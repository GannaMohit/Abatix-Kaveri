from django import forms
from sales.models import Advance, Payment
from masters.models import Customer

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = Advance
        fields = ('date','customer')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'firm', 'gst', 'pan', 'contact')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('advance', 'invoice')
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "box_1_inputs"
            self.fields[field].widget.attrs["oninput"] = "updateValues(false)"

        self.fields["method"].widget.attrs["class"] = ""
        self.fields["method"].widget.attrs["oninput"] = "changeFields(this)"
        self.fields["date"].widget.attrs["id"] = "id_payment_date"
        self.fields["amount"].widget.attrs["id"] = "id_payment_amount"

widgets = {
    "method": forms.TextInput(attrs={"readonly":True}),
    "date": forms.TextInput(attrs={"readonly":True}),
    "name": forms.TextInput(attrs={"readonly":True}),
    "amount": forms.TextInput(attrs={"readonly":True}),
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
PaymentFormSet = forms.inlineformset_factory(Advance, Payment, exclude=('advance','invoice',), extra=0, can_delete=True, widgets=widgets)
