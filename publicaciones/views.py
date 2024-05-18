from django.shortcuts import render, redirect
from .forms import FormularioRegistrarPublicacion
from django.contrib import messages
from db.models import Post,User

# Create your views here.

def registrar_publicacion(request):

    errorPatente = None
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(email=request.session.get('usuario') [0]) # Assign the current user to the post
            post.save()
            messages.success(request, "Publicacion registrada exitosamente")
            return redirect("/")
        else:
            errorPatente = form.errors['patent']
            messages.error(request, "Ya existe una publicacion registrada en el sistema con esa patente")
    else:
        form = FormularioRegistrarPublicacion()
    return render(request, 'registrar_publicacion.html', {'form': form, 'usuario':  request.session.get('usuario'),'mensaje_error': form.errors})

def ver_publicaciones(request):
    posts = Post.objects.all()
    for post in posts:
        user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicaciones.html", {"posts": posts,'usuario':  request.session.get('usuario')})


def ver_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicacion.html", {"post": post,'usuario':  request.session.get('usuario')})

def ver_imagen(request, post_id):
    
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image,'usuario':  request.session.get('usuario')})
