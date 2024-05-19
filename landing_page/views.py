from django.shortcuts import render
from db.models import Post,User

# Create your views here.

def landing_page(request):
    usuario=request.session.get('usuario')
    if usuario:
        user = User.objects.get(email=usuario[0])
    else: 
        user = usuario
    return render(request, "home.html",{'usuario': user})


def visualizar_publicaciones_finalizadas(request):

    publicaciones = Post.objects.filter(state =2)[:3]  # Filtra los primeros tres elementos con state=2
    return render(request, "home.html", {"posts": publicaciones, 'usuario': request.session.get('usuario')})

