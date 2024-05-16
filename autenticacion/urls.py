from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('inicioSesion/', views.inicio_de_sesion, name='inicio de sesion'),
    path('cambioContrasenia/', views.cambio_contrasenia, name='cambio contraseña'),
    path('cerrarSesion/', views.cerrar_sesion, name='cerrar sesion'),
    path('recuperarContrasenia/', views.recuperar_contrasenia, name='recuperar contraseña'),
    path('recuperarContrasenia/codigo', views.ingresar_codigo, name='ingresar zcodigo'),
]
