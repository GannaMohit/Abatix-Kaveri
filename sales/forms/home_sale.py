from django import forms
from sales.models import Home_Sale, Home_Sale_Product

class HomeSaleForm(forms.ModelForm):
    class Meta:
        model = Home_Sale
        fields = ('date',)
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }
widgets = {
    'product': forms.NumberInput(attrs={
        'placeholder':"Add",
        'onfocus':'addRow(this)',
        'oninput':"validateID(this, '/stock/_fetch_product')"
    })
}
ProductFormSet = forms.inlineformset_factory(Home_Sale, Home_Sale_Product, fields=('product',), extra=0, can_delete=True, widgets=widgets)
