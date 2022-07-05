from django.db import models


def product_image_path(instance, filename):
    """
    Constructs and returns a path for product images to be uploaded to.
    """
    return f"products/images/{instance.name_slug}{instance.image_type}"


class Category(models.Model):
    """
    A model for categorising printed products
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120, null=False, blank=True)

    def __str__(self):
        return self.display_name


class ProductImage(models.Model):
    """
    A model to represent product preview images
    """

    class ImageType(models.TextChoices):
        """
        Defines options for the image_type field
        """

        JPEG = ".jpg"
        PNG = ".png"

    name_slug = models.SlugField(
        max_length=50, null=False, blank=False, unique=True
    )
    image_type = models.CharField(
        max_length=4,
        null=False,
        blank=False,
        choices=ImageType.choices,
        default=ImageType.JPEG,
    )
    image = models.ImageField(
        null=False, blank=False, upload_to=product_image_path
    )
    # the following values set the position for the overlayed user's drawing on
    # the product details pages
    overlay_width = models.CharField(
        max_length=5, null=False, blank=False, default="70%"
    )
    overlay_x_offset = models.CharField(
        max_length=5, null=False, blank=False, default="15%"
    )
    overlay_y_offset = models.CharField(
        max_length=5, null=False, blank=False, default="15%"
    )

    def __str__(self):
        return self.name_slug + self.image_type


class Product(models.Model):
    """
    A model to represent each printed product type
    """

    class VariantType(models.TextChoices):
        """
        Defines options for the variant_type field
        """

        COLOUR = "CL"
        SIZE = "SZ"

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=120, null=False, blank=False, unique=True
    )
    display_name = models.CharField(max_length=120, null=False, blank=False)
    image = models.ForeignKey(
        ProductImage, on_delete=models.RESTRICT, blank=False, null=False
    )
    description = models.TextField(null=False, blank=False)
    variant_type = models.CharField(
        max_length=2, choices=VariantType.choices, default=VariantType.SIZE
    )

    def __str__(self):
        return self.display_name


class ProductVariant(models.Model):
    """
    A model to represent each individual product variant
    """

    class Meta:
        # no two variants of the same product should have the same name or
        # display name
        unique_together = (
            ("product", "name"),
            ("product", "display_name"),
        )

    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.RESTRICT
    )
    name = models.CharField(max_length=120, null=False, blank=False)
    display_name = models.CharField(max_length=120, null=False, blank=False)
    image = models.ForeignKey(
        ProductImage, on_delete=models.RESTRICT, blank=True, null=True
    )
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sku = models.CharField(
        max_length=120, null=False, blank=False, unique=True
    )

    def __str__(self):
        return f"{self.sku} - {self.display_name}"
