from rest_framework import viewsets
from .models import (
    RawMaterial, Stock, Supplier, PurchaseOrder, PurchaseOrderItem,
    MaterialReceiving, MaterialReceivingItem
)
from .serializers import (
    RawMaterialSerializer, StockSerializer, SupplierSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer,
    MaterialReceivingSerializer, MaterialReceivingItemSerializer
)

class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer

class MaterialReceivingViewSet(viewsets.ModelViewSet):
    queryset = MaterialReceiving.objects.all()
    serializer_class = MaterialReceivingSerializer

class MaterialReceivingItemViewSet(viewsets.ModelViewSet):
    queryset = MaterialReceivingItem.objects.all()
    serializer_class = MaterialReceivingItemSerializer