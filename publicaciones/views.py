from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioRegistrarPublicacion, CommentForm
from ofertas.forms import FormularioRegistrarOferta
from django.contrib import messages
from db.models import Post,User,Comment, Notification

# Create your views here.

def registrar_publicacion(request):
    if(request.session.get('usuario') != None and request.session.get('usuario') [2] > 0):
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
    else:
        messages.error(request, "Debes tener permisos para poder publicar")
        return redirect("/")
    return render(request, 'registrar_publicacion.html', {'form': form, 'mensaje_error': form.errors})

def ver_publicaciones(request):
    posts = Post.objects.all()
    if (None == request.session.get('usuario')):
        user_email = None
    else:
        user_email = request.session.get('usuario')[0]
    print(user_email)
    return render(request, "ver_publicaciones.html", {"posts": posts, 'user_email': user_email})

def ver_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if (None == request.session.get('usuario')):
        saved = None
    else:
        saved = post.saved_by.filter(email=request.session.get('usuario')[0]).exists()
    form = CommentForm()
    return render(request, "ver_publicacion.html", {'form': form, "post": post,'saved': saved})

def crear_comentario(request, post_id):
    if (request.session.get('usuario') != None):
        if request.method == 'POST':
            form = CommentForm(request.POST, post_id=post_id, request=request)
            if form.is_valid():
                comentario = form.save()
                post = Post.objects.get(id=post_id)
                noti = Notification(title='Nuevo comentario',user=post.user,content=f'Has recibido un nuevo comentario en la publicación {post.title}',link=f'/publicaciones/{post_id}#comentario{comentario.id}')
                noti.save()
        form = CommentForm()
    else: 
        messages.error(request, "¡Debe iniciar sesión para poder comentar!")
        return redirect ('/autenticacion/inicioSesion')
    return redirect ('/publicaciones/'+str(post_id))

def crear_respuesta(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, post_id=post_id, request=request, parent_id = request.POST["parent_id"])
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
    return redirect ('/publicaciones/'+str(post_id))

def ver_imagen(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image})

def guardar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if (post.saved_by.filter(email=request.session.get('usuario')[0]).exists()):
        post.saved_by.remove(User.objects.get(email=request.session.get('usuario')[0]))
    else:
        post.saved_by.add(User.objects.get(email=request.session.get('usuario')[0]))
    return redirect ('/publicaciones/'+str(post_id))

def registrar_oferta(request, post_id):
    if(request.session.get('usuario') != None):
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
            form = FormularioRegistrarOferta()
    else:
        messages.error(request, "Debes iniciar sesion para poder ofertar")
        return redirect("/autenticacion/inicioSesion")
    return render(request, 'registrar_oferta.html', {'form': form})

def eliminar_comentario(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    comment.delete()
    messages.success(request, "Comentario eliminado exitosamente")
    return redirect ('/publicaciones/'+str(post_id))

def editar_comentario(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST, post_id=post_id, instance=comment, request=request)
        if form.is_valid():
            comentario = form.save()
            post = Post.objects.get(id=post_id)
            noti = Notification(title='Nuevo comentario',user=post.user,content=f'Has recibido un nuevo comentario en la publicación {post.title}',link=f'/publicaciones/{post_id}#comentario{comentario.id}')
            noti.save()
    form = CommentForm()
    return redirect ('/publicaciones/'+str(post_id))
