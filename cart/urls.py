from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('remove_cart_item/', views.remove_cart_item, name='remove_cart_item'),
]
