from django.contrib import admin
from .models import RawMaterial, Stock, Supplier, PurchaseOrder, PurchaseOrderItem, MaterialReceiving, MaterialReceivingItem

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'quantity_available', 'reorder_level', 'cost_per_unit')
    search_fields = ('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('material', 'quantity', 'transaction_type', 'date', 'reference')
    list_filter = ('transaction_type', 'date')
    search_fields = ('material__name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'email')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'order_date', 'expected_delivery', 'status', 'total_amount')
    list_filter = ('status', 'supplier')
    search_fields = ('po_number', 'supplier__name')
    date_hierarchy = 'order_date'

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'material', 'quantity', 'unit_price', 'received_quantity')
    search_fields = ('purchase_order__po_number', 'material__name')

@admin.register(MaterialReceiving)
class MaterialReceivingAdmin(admin.ModelAdmin):
    list_display = ('receiving_number', 'purchase_order', 'receiving_date', 'received_by')
    search_fields = ('receiving_number', 'purchase_order__po_number')
    list_filter = ('receiving_date',)

@admin.register(MaterialReceivingItem)
class MaterialReceivingItemAdmin(admin.ModelAdmin):
    list_display = ('receiving', 'purchase_order_item', 'received_quantity')
    search_fields = ('receiving__receiving_number', 'purchase_order_item__material__name')