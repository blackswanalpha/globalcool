from django.contrib import admin
from .models import ServiceCategory, Service, ServiceImage, ProductCategory, Product, ProductImage


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price_min', 'base_price_max', 'is_active', 'is_featured', 'booking_count']
    list_filter = ['category', 'is_active', 'is_featured', 'duration_estimate', 'created_at']
    search_fields = ['name', 'summary', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'booking_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'summary', 'description')
        }),
        ('Pricing', {
            'fields': ('base_price_min', 'base_price_max', 'price_note')
        }),
        ('Service Details', {
            'fields': ('duration_estimate', 'specifications', 'features', 'requirements')
        }),
        ('Visibility & SEO', {
            'fields': ('is_active', 'is_featured', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'booking_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ['image', 'title', 'is_featured', 'order']


# Update ServiceAdmin to include images
ServiceAdmin.inlines = [ServiceImageInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'title', 'image_type', 'is_featured', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'sale_price', 'stock_quantity', 'stock_status', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured', 'stock_status', 'created_at']
    search_fields = ['name', 'summary', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'order_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'summary', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price', 'price_note')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity', 'stock_status')
        }),
        ('Product Details', {
            'fields': ('specifications', 'dimensions', 'weight', 'features', 'warranty')
        }),
        ('Visibility & SEO', {
            'fields': ('is_active', 'is_featured', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'order_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
