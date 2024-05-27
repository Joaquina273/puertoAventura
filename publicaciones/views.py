from django.shortcuts import render, redirect
from .forms import FormularioRegistrarPublicacion, CommentForm
from django.contrib import messages
from db.models import Post,User

# Create your views here.

def registrar_publicacion(request):
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(email=request.session.get('usuario') [0]) # Assign the current user to the post
            post.save()
            messages.success(request, "Publicacion registrada exitosamente")
            return redirect("/")
        else:
            messages.error(request, "Ya existe una publicacion registrada en el sistema con esa patente")
    else:
        form = FormularioRegistrarPublicacion()
    return render(request, 'registrar_publicacion.html', {'form': form, 'mensaje_error': form.errors})

def ver_publicaciones(request):
    posts = Post.objects.all()
    return render(request, "ver_publicaciones.html", {"posts": posts })

def ver_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if (None == request.session.get('usuario')):
        saved = None
    else:
        saved = post.saved_by.filter(email=request.session.get('usuario')[0]).exists()
    form = CommentForm()
    return render(request, "ver_publicacion.html", {'form': form, "post": post,'saved': saved})

def crear_comentario(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, post_id=post_id, request=request)
        if form.is_valid():
            form.save()
    form = CommentForm()
    return ver_publicacion(request,post_id)

def ver_imagen(request, post_id):
    usuario=request.session.get('usuario')
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image})

def guardar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if (post.saved_by.filter(email=request.session.get('usuario')[0]).exists()):
        post.saved_by.remove(User.objects.get(email=request.session.get('usuario')[0]))
    else:
        post.saved_by.add(User.objects.get(email=request.session.get('usuario')[0]))
    return redirect ('/publicaciones/'+str(post_id))