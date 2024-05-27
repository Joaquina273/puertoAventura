from django.urls import path
from . import views

app_name = "publicaciones"
urlpatterns = [
    # ex: /publicaciones/
    path("", views.ver_publicaciones, name="ver_publicaciones"),
    # ex: /publicaciones/registrarPublicacion
    path("registrarPublicacion", views.registrar_publicacion, name="registrar_publicacion"),
    # ex: /publicaciones/4
    path("<int:post_id>/", views.ver_publicacion, name="ver_publicacion"),
    path("<int:post_id>/comentario", views.crear_comentario, name="comentario"),
    # ex: /publicaciones/4/image
    path("<int:post_id>/image/", views.ver_imagen, name="imagen_publicacion"),
    path("<int:post_id>/guardar/", views.guardar_publicacion, name="guardar publicacion"),
]