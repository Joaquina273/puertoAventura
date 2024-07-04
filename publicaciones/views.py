from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioRegistrarPublicacion, CommentForm
from ofertas.forms import FormularioRegistrarOferta
from django.contrib import messages
from db.models import Post,User,Comment, Notification,Port

# Create your views here.

def registrar_publicacion(request):
    usuarioConectado=User.objects.get(email=request.session.get('usuario') [0])
    if(request.session.get('usuario') != None and usuarioConectado.type_user > 0):
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
        messages.error(request, "Necesitas que tu perfil esté verificado para poder publicar")
        return redirect("/usuarios/perfil")
    return render(request, 'registrar_publicacion.html', {'form': form, 'mensaje_error': form.errors})

def ver_publicaciones(request):
    query = request.GET.get('q')
    print(query)
    puertos = Port.objects.all()
    ship_types = Post.types_ships
    ship_types_list = list(ship_types.values())
    if query:
       posts = Post.objects.filter(title__icontains=query, state=0).order_by("-post_date")
    else:
        posts = Post.objects.all().order_by("-post_date").filter(state=0)
    return render(request, "ver_publicaciones.html", {"posts": posts,"puertos":puertos,"tipos":ship_types_list})

def ver_publicaciones_finalizadas(request):
    posts = Post.objects.all().order_by("-post_date").filter(state=2)
    return render(request, "ver_publicaciones.html", {"posts": posts})

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
                noti = Notification(title='Nuevo comentario',user=post.user,content=f'Has recibido un nuevo comentario en la publicación "{post.title}"',link=f'/publicaciones/{post_id}#comentario{comentario.id}')
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
            padre = Comment.objects.get(id= request.POST["parent_id"])
            noti = Notification(title='Nueva respuesta a tu comentario',
                                user=padre.user,
                                content=f'Tu comentario de la publicación "{Post.objects.get(id=post_id).title}" ha sido respondido',
                                link=f'/publicaciones/{post_id}#comentario{request.POST["parent_id"]}')
            noti.save()
    else:
        form = CommentForm()
    return redirect ('/publicaciones/'+str(post_id))

def ver_imagen(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "ver_publicacion.html", {"image": post.image})

def guardar_publicacion(request, post_id):
    if (request.session.get('usuario') != None):
        post = Post.objects.get(id=post_id)
        if (post.saved_by.filter(email=request.session.get('usuario')[0]).exists()):
            post.saved_by.remove(User.objects.get(email=request.session.get('usuario')[0]))
        else:
            post.saved_by.add(User.objects.get(email=request.session.get('usuario')[0]))
        return redirect ('/publicaciones/'+str(post_id))
    else:
        messages.error(request, "Debes iniciar sesion para guardarte una publicación")
        return redirect("/autenticacion/inicioSesion")

def registrar_oferta(request, post_id):
    if(request.session.get('usuario') != None):
        if request.method == 'POST':
            form = FormularioRegistrarOferta(data=request.POST, files=request.FILES)
            if form.is_valid():
                offer = form.save(commit=False)
                offer.user = User.objects.get(email=request.session.get('usuario') [0]) # Assign the current user to the post
                offer.post = Post.objects.get(id=post_id)
                offer.save()
                post = Post.objects.get(id=post_id)
                noti = Notification(title='Nueva oferta recibida',
                                user=post.user,
                                content=f'Has recibido una oferta en tu publicación "{post.title}"',
                                link=f'/ofertas/{offer.id}')
                noti.save()
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
    notis = Notification.objects.filter(user=Post.objects.get(id=post_id).user.email,link=f'/publicaciones/{post_id}#comentario{comment_id}')
    for noti in notis:
        noti.link = '/usuarios/notificaciones/ver/0/'
        noti.save()
    if comment.parent:
        notis = Notification.objects.filter(user=comment.parent.user.email,link=f'/publicaciones/{post_id}#comentario{comment.parent.id}')
        for noti in notis:
            noti.link = '/usuarios/notificaciones/ver/0/'
            noti.save()
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
            if post.user.email == request.session.get('usuario')[0]:
                noti = Notification(title='Comentario editado',
                                    user=comment.parent.user,
                                    content=f'Una respuesta en tu comentario de {post.title} ha sido editada.',
                                    link=f'/publicaciones/{post_id}#comentario{comment.parent.id}')
            else:
                noti = Notification(title='Comentario editado',
                                    user=post.user,
                                    content=f'Un comentario realizado en tu publicación {post.title} ha sido editado',
                                    link=f'/publicaciones/{post_id}#comentario{comentario.id}')
            noti.save()
    form = CommentForm()
    return redirect ('/publicaciones/'+str(post_id))
