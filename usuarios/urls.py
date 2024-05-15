from django.urls import path, include
from . import views

urlpatterns = [
    path('perfil/', views.ver_perfil, name='ver perfil'),
]