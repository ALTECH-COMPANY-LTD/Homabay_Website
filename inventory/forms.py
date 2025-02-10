# inventory/forms.py
from django import forms
from .models import MaterialReceiving, MaterialReceivingItem, PurchaseOrder, PurchaseOrderItem, RawMaterial, Stock, Supplier

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ['name', 'unit', 'quantity_available', 'reorder_level', 'cost_per_unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['material', 'quantity', 'transaction_type', 'reference']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget = forms.Select(choices=[
            ('in', 'Stock In'),
            ('out', 'Stock Out')
        ])


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'tax_number', 'status']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_delivery', 'notes']
        widgets = {
            'expected_delivery': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['material', 'quantity', 'unit_price']

PurchaseOrderItemFormSet = forms.inlineformset_factory(
    PurchaseOrder, PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    can_delete=True
)

class MaterialReceivingForm(forms.ModelForm):
    class Meta:
        model = MaterialReceiving
        fields = ['purchase_order', 'received_by', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class MaterialReceivingItemForm(forms.ModelForm):
    class Meta:
        model = MaterialReceivingItem
        fields = ['purchase_order_item', 'received_quantity', 'notes']

MaterialReceivingItemFormSet = forms.inlineformset_factory(
    MaterialReceiving, MaterialReceivingItem,
    form=MaterialReceivingItemForm,
    extra=1,
    can_delete=True
)