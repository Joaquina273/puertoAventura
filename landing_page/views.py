from django.shortcuts import render
from db.models import Post,User

# Create your views here.

def landing_page(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    usuario=request.session.get('usuario')
    return render(request, "home.html",{'usuario': request.session.get('usuario'),'type_user':tipoo_user})


def visualizar_publicaciones_finalizadas(request):

    publicaciones = Post.objects.filter(state =2)[:3]  # Filtra los primeros tres elementos con state=2
    return render(request, "home.html", {"posts": publicaciones, 'usuario': request.session.get('usuario')})

