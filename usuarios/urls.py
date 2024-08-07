from django.urls import path
from . import views


app_name = "usuarios"
urlpatterns = [
    # ex: usuarios/publicaciones
    path("publicaciones", views.ver_publicaciones, name="ver_publicaciones"),
    # ex: usuarios/publicacionesGuardadas
    path("publicacionesGuardadas", views.ver_publicaciones_guardadas, name="ver publicaciones guardadas"),
    # ex: usuarios/publicaciones/eliminarPublicacion/1
    path("publicaciones/eliminarPublicacion/<int:post_id>", views.eliminar_publicacion, name="eliminar_publicacion"),
    # ex: usuarios/publicaciones/editarPublicacion/1
    path("publicaciones/editarPublicacion/<int:post_id>", views.editar_publicacion, name="editar_publicacion"),
    # ex: usuarios/publicaciones/eliminarPublicacion/1
    path("publicaciones/eliminarPublicacion/<int:post_id>", views.eliminar_publicacion, name="eliminar_publicacion"),
    # ex: usuarios/perfil/
    path('perfil/', views.ver_perfil, name='ver perfil'),
    # ex: usuarios/ofertasRecibidas
    path("ofertasRecibidas", views.ver_ofertas_recibidas, name="ver_ofertas_recibidas"),
    # ex: usuarios/ofertarRealizadas
    path("ofertasRealizadas", views.ver_ofertas_realizadas, name="ver_ofertas_realizadas"),
    # ex: usuarios/ofertasRecibidas/eliminarOferta/1
    path("ofertasRecibidas/eliminarOferta/<int:offer_id>", views.eliminar_oferta, name="eliminar_oferta"),
    # ex: usuarios/ofertasRecibidas/editarOferta/1
    path("ofertasRecibidas/editarOferta/<int:offer_id>", views.editar_oferta, name="editar_oferta"),
    # ex: usuarios/ofertasRecibidas/aceptarOferta/1
    path("ofertasRecibidas/aceptarOferta/<int:offer_id>", views.aceptar_oferta, name="aceptar_oferta"),
    # ex: usuarios/ofertasRecibidas/rechazarOferta/1
    path("ofertasRecibidas/rechazarOferta/<int:offer_id>", views.rechazar_oferta, name="rechazar_oferta"),
    # ex: usuarios/notificaciones/
    path('notificaciones/', views.ver_notificaciones, name='ver notificaciones'),
    # ex: usuarios/notificaciones/leer/1
    path('notificaciones/leer/<int:id_notificacion>/', views.leer_notificacion, name='leer notificación'),
    # ex: usuarios/notificaciones/leer/1
    path('notificaciones/ver/<int:id_notificacion>/', views.ver_notificacion, name='ver notificación'),
    # ex: usuarios/listado
    path('listado/',views.ver_listado, name="ver_listado"),
    # ex: usuarios/listado/publicaciones
    path('listado/publicaciones',views.ver_listado_publicaciones,name="ver_listado_publicaciones"),
    
    path('motivoReporte/',views.crear_reporte, name="crear_reporte"),
   
    path('motivoReporte/ultimoPaso',views.motivo_reporte, name="motivo_reporte"),

]