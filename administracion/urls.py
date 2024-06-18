from django.urls import path
from . import views


app_name = "administracion"
urlpatterns = [ 

path('reportes/',views.ver_reportes, name="ver_reportes")

]