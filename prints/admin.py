from django.contrib import admin
from .models import Category, ProductImage, Product, ProductVariant
from .forms import ProductImageForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "name",
    )


class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "name_slug",
        "image_type",
        "image",
        "overlay_width",
        "overlay_x_offset",
        "overlay_y_offset",
    )

    # use custom ProductImageForm
    form = ProductImageForm

    class Media:
        # include js and css files for product image form
        js = ("admin/js/productImage.js",)
        css = {"all": ("admin/css/product-image.css",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "name",
        "category",
        "variant_type",
        "description",
        "image",
    )


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "name",
        "product",
        "sku",
        "price",
        "description",
        "image",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
