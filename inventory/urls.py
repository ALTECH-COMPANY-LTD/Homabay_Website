from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RawMaterialViewSet,
    StockViewSet,
    SupplierViewSet,
    PurchaseOrderViewSet,
    PurchaseOrderItemViewSet,
    MaterialReceivingViewSet,
    MaterialReceivingItemViewSet
)

router = DefaultRouter()
router.register(r'raw-materials', RawMaterialViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'purchase-order-items', PurchaseOrderItemViewSet)
router.register(r'material-receivings', MaterialReceivingViewSet)
router.register(r'material-receiving-items', MaterialReceivingItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]