from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("save_drawing/", views.save_drawing, name="save_drawing"),
    path("get_drawing/", views.get_drawing, name="get_drawing"),
    path(
        "delete_drawing/<int:drawing_id>/",
        views.delete_drawing,
        name="delete_drawing",
    ),
]
