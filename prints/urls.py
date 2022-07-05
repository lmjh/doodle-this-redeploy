from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_all_prints, name="show_all_prints"),
    path("add_product/", views.add_product, name="add_product"),
    path(
        "edit_product/<int:product_id>/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "delete_product/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
    path(
        "add_product_image/", views.add_product_image, name="add_product_image"
    ),
    path(
        "edit_product_image/<int:product_image_id>/",
        views.edit_product_image,
        name="edit_product_image",
    ),
    path(
        "delete_product_image/<int:product_image_id>/",
        views.delete_product_image,
        name="delete_product_image",
    ),
    path(
        "add_product_variant/",
        views.add_product_variant,
        name="add_product_variant",
    ),
    path(
        "edit_product_variant/<int:product_variant_id>/",
        views.edit_product_variant,
        name="edit_product_variant",
    ),
    path(
        "delete_product_variant/<int:product_variant_id>/",
        views.delete_product_variant,
        name="delete_product_variant",
    ),
    path(
        "product_management/",
        views.product_management,
        name="product_management",
    ),
    path("<product_name>/", views.product_details, name="product_details"),
]
