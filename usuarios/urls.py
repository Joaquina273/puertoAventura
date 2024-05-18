from django.urls import path
from . import views


app_name = "usuarios"
urlpatterns = [
    # ex: usuarios/publicaciones
    path("publicaciones", views.ver_publicaciones, name="ver_publicaciones"),
     path("publicacionesGuardadas", views.ver_publicaciones_guardadas, name="ver publicaciones guardadas"),
    # ex: usuarios/publicaciones/eliminarPublicacion/1
    path("publicaciones/eliminarPublicacion/<int:post_id>", views.eliminar_publicacion, name="eliminar_publicacion"),
    # ex: usuarios/email/publicaciones/editarPublicacion/1
    path("publicaciones/editarPublicacion/<int:post_id>", views.editar_publicacion, name="editar_publicacion"),
    path('perfil/', views.ver_perfil, name='ver perfil'),
]