from django.shortcuts import render, redirect
from .forms import FormularioRegistrarPublicacion
from ofertas.forms import FormularioRegistrarOferta
from django.contrib import messages
from db.models import Post,User

# Create your views here.

def registrar_publicacion(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
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
    return render(request, 'registrar_publicacion.html', {'form': form, 'usuario': request.session.get('usuario'),'type_user':tipoo_user,'mensaje_error': form.errors})

def ver_publicaciones(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    posts = Post.objects.all()
    for post in posts:
        user = User.objects.get(email=post.user_id)
    return render(request, "ver_publicaciones.html", {"posts": posts,'usuario': request.session.get('usuario'), 'type_user':tipoo_user })

def ver_publicacion(request, post_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    post = Post.objects.get(id=post_id)
    user = User.objects.get(email=post.user_id)
    if (None == request.session.get('usuario')):
        saved = None
    else:
        saved = post.saved_by.filter(email=request.session.get('usuario')[0]).exists()
    return render(request, "ver_publicacion.html", {"post": post,'usuario':  request.session.get('usuario'),'saved': saved,'type_user':tipoo_user})

def ver_imagen(request, post_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image,'usuario':  request.session.get('usuario'),'type_user':tipoo_user})

def guardar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if (post.saved_by.filter(email=request.session.get('usuario')[0]).exists()):
        post.saved_by.remove(User.objects.get(email=request.session.get('usuario')[0]))
    else:
        post.saved_by.add(User.objects.get(email=request.session.get('usuario')[0]))
    return redirect ('/publicaciones/'+str(post_id))



def registrar_oferta(request, post_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    errorPatente = None
    if request.method == 'POST':
        form = FormularioRegistrarOferta(data=request.POST, files=request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = User.objects.get(email=request.session.get('usuario') [0]) # Assign the current user to the post
            offer.post = Post.objects.get(id=post_id)
            offer.save()
            messages.success(request, "Oferta registrada exitosamente")
            return redirect("/")
        else:
            messages.error(request, "Ya existe una publicacion registrada en el sistema con esa patente")
    else:
        form = FormularioRegistrarOferta()
    return render(request, 'registrar_oferta.html', {'form': form, 'usuario': request.session.get('usuario'),'type_user':tipoo_user,'mensaje_error': form.errors})