from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("webhook/", webhook, name="webhook"),
    path("cache_order_data/", views.cache_order_data, name="cache_order_data"),
    path(
        "cache_order_drawing/",
        views.cache_order_drawing,
        name="cache_order_drawing",
    ),
    path(
        "order_confirmed/<order_number>",
        views.order_confirmed,
        name="order_confirmed",
    ),
    path(
        "order_details/<order_number>",
        views.order_details,
        name="order_details",
    ),
]
