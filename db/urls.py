from django.urls import path
from . import views

app_name = "db"
urlpatterns = [
    path('rating', views.rating, name='rating')
]