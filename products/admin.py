from django.contrib import admin
from .models import *
# Register your models here.

class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductImageTabularInline]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)

class CategoryAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
