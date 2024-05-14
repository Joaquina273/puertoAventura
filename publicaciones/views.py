from django.shortcuts import render, redirect
from .forms import FormularioRegistrarPublicacion
from db.models import Post,User

# Create your views here.

def registrar_publicacion(request):
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the current user to the post
            post.save()
            return redirect("/")
    else:
        form = FormularioRegistrarPublicacion()
    return render(request, 'registrar_publicacion.html', {'form': form})

def ver_publicaciones(request):

    posts = Post.objects.all()
    for post in posts:
        user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicaciones.html", {"posts": posts})


def ver_publicacion(request, post_id):
    
    post = Post.objects.get(id=post_id)
    user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicacion.html", {"post": post})

def ver_imagen(request, post_id):
    
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image})

