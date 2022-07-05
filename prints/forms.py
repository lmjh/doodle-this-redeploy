from decimal import Decimal

from django import forms

from .widgets import ProductImageInput
from .models import ProductImage, Product, ProductVariant


class ProductImageForm(forms.ModelForm):
    """
    A form to create product images
    """

    class Meta:
        model = ProductImage
        fields = "__all__"

    # use custom ProductImageInput widget for image field
    image = forms.ImageField(
        label="image", required=True, widget=ProductImageInput
    )


class ProductForm(forms.ModelForm):
    """
    A form to create products
    """

    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantForm(forms.ModelForm):
    """
    A form to create product variants
    """

    class Meta:
        model = ProductVariant
        fields = "__all__"

    price = forms.DecimalField(min_value=Decimal("0.01"))
