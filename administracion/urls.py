from django.urls import path
from . import views


app_name = "administracion"
urlpatterns = [ 
    path('reportes/bloqueo/',views.bloqueo, name="bloqueo usuario"),
    path('reportes/',views.ver_reportes, name="ver_reportes"),
    # ex: administracion/estadisticas/
    path('estadisticas/', views.ver_estadisticas, name = 'ver_estadisticas'),
    # ex: administracion/estadisticas/publicaciones/
    path('estadisticas/publicaciones', views.ver_estadisticas_publicaciones, name = 'ver_estadisticas_publicaciones'),
    # ex: administracion/estadisticas/usuarios/
    path('estadisticas/usuarios', views.ver_estadisticas_usuarios, name = 'ver_estadisticas_usuarios'),
    # ex: administracion/estadisticas/intercambios/
    path('estadisticas/intercambios', views.ver_estadisticas_intercambios, name = 'ver_estadisticas_intercambios'),
    # ex: administracion/estadisticas/ofertas/
    path('estadisticas/ofertas', views.ver_estadisticas_ofertas, name = 'ver_estadisticas_ofertas'),
]