from django.urls import path
from . import views

app_name = "ofertas"
urlpatterns = [
    # ex: /ofertas/4/
    path("<int:offer_id>/", views.ver_oferta, name="ver_oferta"),
    # ex: /ofertas/4/image
    path("<int:offer_id>/image/", views.ver_imagen, name="imagen_oferta"),
]