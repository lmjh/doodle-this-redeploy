import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from accounts.models import UserAccount
from prints.models import ProductVariant


# set upload directory for order drawings
def upload_to(instance, filename):
    """
    Constructs and returns a path for order drawings to be uploaded to.
    Drawings are uploaded to a folder named with the unique order number and
    prefixed with the order primary key. As the primary key will increase
    over time, new order folders are easy to find.
    """
    return (
        f"order-drawings/{instance.order.pk}"
        f"-{str(instance.order.order_number)}/{instance.save_slot}.png"
    )


# set upload directory for order drawings cache
def upload_to_cache(instance, filename):
    """
    Constructs and returns a path for cached order drawings to be uploaded to.
    Drawings are uploaded to a folder named with the stripe payment intent id.
    """
    return (
        f"order-drawings/cache/{instance.stripe_pid}/0.png"
    )


class Order(models.Model):
    """
    A model to represent customer orders
    """

    order_number = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    user_account = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    address_1 = models.CharField(max_length=80, null=False, blank=False)
    address_2 = models.CharField(max_length=80, null=True, blank=True)
    town = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=40, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(null=False, blank=False)
    email_address = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    order_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    shopping_cart = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )
    date = models.DateTimeField(auto_now_add=True)

    def update_total(self):
        """
        Calculates order_cost from sum of order items and grand_total from
        order_total plus delivery cost
        """
        self.order_cost = (
            self.order_items.aggregate(Sum("order_item_total"))[
                "order_item_total__sum"
            ]
            or 0
        )
        self.delivery_cost = settings.STANDARD_DELIVERY_FEE
        self.grand_total = self.order_cost + self.delivery_cost
        self.save()

    def __str__(self):
        return str(self.order_number)


class OrderDrawing(models.Model):
    """
    A model to represent the drawings a user has submitted to be printed on
    a product
    """

    class Meta:
        # no two drawings in the same order should have the same save_slot
        unique_together = (("order", "save_slot"),)

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="order_drawings",
    )
    image = models.ImageField(null=False, blank=False, upload_to=upload_to)
    save_slot = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return (
            f"Order {str(self.order.order_number)} - Drawing {self.save_slot}"
        )


class OrderItem(models.Model):
    """
    A model to represent each unique pairing of drawing and product variant in
    an order.
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    product_variant = models.ForeignKey(
        ProductVariant, null=False, blank=False, on_delete=models.CASCADE
    )
    order_drawing = models.ForeignKey(
        OrderDrawing, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    order_item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        On save, set the order_item_total by multiplying the product variant's
        price by the selected quantity.
        """
        self.order_item_total = self.product_variant.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Order {str(self.order.order_number)} - "
            f"SKU {self.product_variant.sku} - "
            f"Drawing {self.order_drawing.save_slot}"
        )


class OrderDrawingCache(models.Model):
    """
    A model to store a user's current sketchbook drawing while payment is
    processed
    """

    image = models.ImageField(
        null=False, blank=False, upload_to=upload_to_cache
    )
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    def __str__(self):
        return (
            f"PID {self.stripe_pid}"
        )
