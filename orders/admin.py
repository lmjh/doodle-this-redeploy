from django.contrib import admin
from .models import Order, OrderDrawing, OrderItem, OrderDrawingCache


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("order_item_total",)


class OrderDrawingAdminInline(admin.TabularInline):
    model = OrderDrawing


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline, OrderDrawingAdminInline)

    readonly_fields = (
        "order_number",
        "date",
        "delivery_cost",
        "order_cost",
        "grand_total",
        "shopping_cart",
        "stripe_pid",
    )

    fields = (
        "order_number",
        "user_account",
        "first_name",
        "last_name",
        "address_1",
        "address_2",
        "town",
        "county",
        "postcode",
        "country",
        "email_address",
        "phone_number",
        "order_cost",
        "delivery_cost",
        "grand_total",
        "shopping_cart",
        "stripe_pid",
        "date",
    )

    list_display = (
        "order_number",
        "date",
        "first_name",
        "last_name",
        "order_cost",
        "delivery_cost",
        "grand_total",
    )

    ordering = ("-date",)


class OrderDrawingCacheAdmin(admin.ModelAdmin):
    fields = (
        "image",
        "stripe_pid",
    )
    list_display = (
        "image",
        "stripe_pid",
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDrawingCache, OrderDrawingCacheAdmin)
