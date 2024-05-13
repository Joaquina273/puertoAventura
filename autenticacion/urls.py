from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('inicioSesion/', views.inicioDeSesion, name='inicio de sesion'),
    path('cambioContrasenia/', views.cambioContrasenia, name='cambio contraseña'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar sesion')
]
