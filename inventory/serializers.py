from rest_framework import serializers
from .models import (
    RawMaterial, Stock, Supplier, PurchaseOrder, PurchaseOrderItem,
    MaterialReceiving, MaterialReceivingItem
)

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'

class MaterialReceivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialReceiving
        fields = '__all__'

class MaterialReceivingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialReceivingItem
        fields = '__all__'