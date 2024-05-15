from django.urls import path
from . import views

app_name = "usuarios"
urlpatterns = [
    # ex: usuarios/email/publicaciones
    path("<str:user_email>/publicaciones", views.ver_publicaciones, name="ver_publicaciones"),
    # ex: usuarios/email/publicaciones/eliminarPublicacion/1
    path("<str:user_email>/publicaciones/eliminarPublicacion/<int:post_id", views.eliminar_publicacion, name="eliminar_publicacion")
]