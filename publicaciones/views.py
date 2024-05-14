from django.shortcuts import render, redirect
from .forms import FormularioRegistrarPublicacion
from db.models import Post,User
from autenticacion.views import se_encuentra_conectado

# Create your views here.

def registrar_publicacion(request):
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = se_encuentra_conectado(request)[0]  # Assign the current user to the post
            post.save()
            return redirect("")
        else:
            print(form.errors)
    else:
        form = FormularioRegistrarPublicacion()
    return render(request, 'registrar_publicacion.html', {'form': form, 'usuario': se_encuentra_conectado(request)})

def ver_publicaciones(request):
    posts = Post.objects.all()
    for post in posts:
        user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicaciones.html", {"posts": posts,'usuario': se_encuentra_conectado(request)})


def ver_publicacion(request, post_id):
    
    post = Post.objects.get(id=post_id)
    user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicacion.html", {"post": post,'usuario': se_encuentra_conectado(request)})

def ver_imagen(request, post_id):
    
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image,'usuario': se_encuentra_conectado(request)})

