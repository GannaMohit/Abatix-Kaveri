from django.forms import ModelForm, inlineformset_factory, DateInput, NumberInput
from .models import Product, Stud

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('sold',)

class TagDetailsForm(ModelForm):
    class Meta:
        model = Product
        fields = ('purchase_date', 'lot_number', 'old_id', 'register_id', 'design_code')
        widgets = {
            'purchase_date': DateInput(attrs={'type':'date'}),
        }

class MetalDetailsForm(ModelForm):
    class Meta:
        model = Product
        fields = ('metal', 'purity', 'type', 'category', 'description')

class ProductDetailsForm(ModelForm):
    class Meta:
        model = Product
        fields = ('vendor', 'pieces', 'gross_weight', 'studs_weight', 'less_weight', 'net_weight')
        widgets = {
            'studs_weight': NumberInput(attrs={'readonly': True}),
            'less_weight': NumberInput(attrs={'readonly': True}),
            'net_weight': NumberInput(attrs={'readonly': True})
        }

class MakingDetailsForm(ModelForm):
    class Meta:
        model = Product
        fields = ('rate', 'making_charges', 'wastage', 'mrp')

class StudForm(ModelForm):
    class Meta:
        model = Stud
        exclude = ('product',)

StudFormSet = inlineformset_factory(Product, Stud, fields='__all__', extra=0, can_delete=True)
