from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'dimensions')  
    search_fields = ('name', 'category')  
    list_filter = ('category',)  
    ordering = ('category', 'name')  
    list_per_page = 20  

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'dimensions', 'features', 'category', 'image')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'
    list_display = (*list_display, 'image_preview')  