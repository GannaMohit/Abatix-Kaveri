from django.forms import ModelForm, inlineformset_factory, DateInput, TextInput, NumberInput, HiddenInput
from .models import Product, Stud

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('invoice', 'home_sale', 'sold')
        widgets = {
            'purchase_date': DateInput(attrs={'type':'date'})
        }

class StudForm(ModelForm):
    class Meta:
        model = Stud
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "last-box-inputs"
            self.fields[field].widget.attrs["oninput"] = "updateTable(this)"

widgets = {
    'id': HiddenInput(attrs={'readonly':True}),
    'type': HiddenInput(attrs={'readonly':True}),
    'less': TextInput(attrs={'readonly':True}),
    'colour': TextInput(attrs={'readonly':True}),
    'shape': TextInput(attrs={'readonly':True}),
    'quantity': NumberInput(attrs={'readonly':True}),
    'weight': NumberInput(attrs={'readonly':True}),
    'unit': HiddenInput(attrs={'readonly':True}),
    'rate': NumberInput(attrs={'readonly':True}),
    'value': NumberInput(attrs={'readonly':True})
}
StudFormSet = inlineformset_factory(Product, Stud, fields='__all__', extra=0, can_delete=True, widgets=widgets)
