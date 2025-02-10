# production/admin.py
from django.contrib import admin
from .models import ProductionLine, ProductionRun, ProductionOutput, RawMaterialRequirement

class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

class ProductionRunAdmin(admin.ModelAdmin):
    list_display = ('production_line', 'start_time', 'status', 'target_output', 'actual_output')
    search_fields = ('production_line__name', 'status')
    list_filter = ('status', 'production_line')

class ProductionOutputAdmin(admin.ModelAdmin):
    list_display = ('production_run', 'quantity', 'rejects', 'timestamp')
    search_fields = ('production_run__production_line__name',)
    list_filter = ('production_run__production_line',)

class RawMaterialRequirementAdmin(admin.ModelAdmin):
    list_display = ('production_run', 'material', 'quantity_required')
    search_fields = ('production_run__production_line__name', 'material__name')
    list_filter = ('production_run__production_line',)

admin.site.register(ProductionLine, ProductionLineAdmin)
admin.site.register(ProductionRun, ProductionRunAdmin)
admin.site.register(ProductionOutput, ProductionOutputAdmin)
admin.site.register(RawMaterialRequirement, RawMaterialRequirementAdmin)