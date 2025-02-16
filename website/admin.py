from django.contrib import admin
from .models import Category, Tag, Item, ItemImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    search_fields = ('title', 'description')
    list_filter = ('category', 'tags')
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('images')  # Optimize image retrieval

    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Image Count'

    list_display += ('images_count',)  # Add image count to the list display


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image')
    search_fields = ('item__title',)  # Allow searching by item title