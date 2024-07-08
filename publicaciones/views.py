from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioRegistrarPublicacion, CommentForm
from ofertas.forms import FormularioRegistrarOferta
from django.contrib import messages
from db.models import Post,User,Comment, Notification,Port
from django.db.models import Q


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
def search(request):
    if request.method == 'GET':
        estado = None 
        palabra = request.GET.get('q')
        posts=Post.objects.all()
        posts = posts.filter(title__icontains=palabra).order_by("-post_date")
        posts = posts.filter(~Q(state=1)).order_by("-post_date")
        return render(request, "ver_publicaciones.html", {"posts": posts, "puertos": Port.objects.all(), "tipos": list(Post.types_ships.values()), 'palabra': palabra, 'state': estado})

def ver_publicaciones(request):
    estado = request.GET.get('state', None)  # Por defecto, mostrar publicaciones disponibles (state=0)
    print(estado)
    posts = Post.objects.filter(~Q(state=1)).order_by("-post_date")
    if request.method == 'GET':
        tipo = request.GET.get('tipo-embarcacion')
        valor = request.GET.get('valor')
        puerto = request.GET.get('puerto')
        eslora = request.GET.get('tamano-eslora')
        palabra = request.GET.get('palabra')
            
        if estado == '0' or estado == '2':
            print(estado)
            print("aca abajos")
            posts = posts.filter(state=estado)
        if palabra:
             posts = posts.filter(title__icontains=palabra)
        if tipo:
            posts = posts.filter(ship_type=tipo)
        if valor:
            if valor == "99":
                posts = posts.filter(value__lt=1000000)  
            elif valor == "1000001":
                posts = posts.filter(value__gte=1000000, value__lte=10000000)  
            elif valor == "10000001":
                posts = posts.filter(value__gt=10000000)
        if puerto:
            puerto_obj = Port.objects.get(name=puerto)
            posts = posts.filter(port=puerto_obj)
        if eslora:
            if eslora == "4":
                posts = posts.filter(eslora__lt=5)  
            elif eslora == "10":
                posts = posts.filter(eslora__gte=5, eslora__lte=15) 
            elif eslora == "15":
                posts = posts.filter(eslora__gt=15)
            
        return render(request, "ver_publicaciones.html", {"posts": posts, "puertos": Port.objects.all(), "tipos": list(Post.types_ships.values()), 'palabra': palabra, 'state': estado,'tipo':tipo,'eslora':eslora,'valor':valor,'puerto':puerto})
    
    return render(request, "ver_publicaciones.html", {"posts": posts, "puertos": Port.objects.all(), "tipos": list(Post.types_ships.values()), 'palabra': palabra, 'state': estado,'tipo':tipo,'eslora':eslora,'valor':valor,'puerto':puerto_obj})

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
