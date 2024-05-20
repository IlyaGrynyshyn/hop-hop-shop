from django.contrib import admin

from shop.models import Category, Product, ProductImage, ProductAttributes


class PhotoAdmin(admin.StackedInline):
    model = ProductImage


class ProductAttributesAdmin(admin.StackedInline):
    model = ProductAttributes


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "slug",
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        PhotoAdmin,
        ProductAttributesAdmin,
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
