from django.urls import path
from . import views

app_name = "conversaciones"
urlpatterns = [
    path('<str:conversacion>/', views.conversacion, name='conversacion'),
    path('checkview', views.checkview, name='checkview'),
    path('enviar', views.enviar, name='enviar'),
    path('conseguir_mensajes/<str:conversacion>/', views.conseguir_mensajes, name='conseguir_mensajes'),
]