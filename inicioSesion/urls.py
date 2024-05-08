from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioDeSesion, name='inicio de sesion')
]