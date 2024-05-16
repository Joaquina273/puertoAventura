from django.shortcuts import render
from db.models import Post
from autenticacion.views import se_encuentra_conectado

# Create your views here.

def landing_page(request):

    return render(request, "home.html",{'usuario':se_encuentra_conectado(request)})


def visualizar_publicaciones_finalizadas(request):

    publicaciones = Post.objects.filter(state =2)[:3]  # Filtra los primeros tres elementos con state=2
    return render(request, "home.html", {"posts": publicaciones, 'usuario':se_encuentra_conectado(request)})

