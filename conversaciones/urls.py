from django.urls import path
from . import views

app_name = "conversaciones"
urlpatterns = [
    path('<str:conversacion>/', views.conversacion, name='conversacion'),
    path('enviar', views.enviar, name='enviar'),
    path('conseguir_mensajes/<str:conversacion>/', views.conseguir_mensajes, name='conseguir_mensajes'),
    path('crearConversacion/<str:id_oferta>/', views.crear_conversacion, name='crear_conversacion'),
    path('descargar/<int:id_mensaje>/', views.descargar_archivo, name='descargar_archivo'),
]