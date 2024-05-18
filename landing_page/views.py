from django.shortcuts import render
from db.models import Post

# Create your views here.

def landing_page(request):

    return render(request, "home.html",{'usuario': request.session.get('usuario')})


def visualizar_publicaciones_finalizadas(request):

    publicaciones = Post.objects.filter(state =2)[:3]  # Filtra los primeros tres elementos con state=2
    return render(request, "home.html", {"posts": publicaciones, 'usuario': request.session.get('usuario')})

