from django.urls import path
from . import views

urlpatterns = [
    path('get_prompt/', views.get_prompt, name='get_prompt')
]
