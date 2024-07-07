import datetime
import os
import shutil
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from db.models import Post,User,Offer, Notification, Comment, Report, Conversation
from publicaciones.forms import FormularioRegistrarPublicacion
from ofertas.forms import FormularioRegistrarOferta


# Create your views here.
def Lista_usuarios(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0  # Redirige a la misma página después de procesar la solicitud

    return render(request, 'usuarios/listado.html',{'usuario': request.session.get('usuario'),'user':user,'type_user':tipoo_user}) 

def ver_perfil(request):
    user = User.objects.get(email=request.session.get('usuario')[0])

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(form_type)
        if form_type == 'edit_form':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            phone_number = request.POST.get('phone_number')
            birthdate_str = request.POST.get('birthdate')

            # Check for changes
            has_changes = False

            if name and name != user.name:
                user.name = name
                has_changes = True
       
            if surname and surname != user.surname:
                user.surname = surname
                has_changes = True
        
            telefono_usuario = int(phone_number)
            if phone_number and user.phone_number != telefono_usuario:
                print(phone_number)
                print(user.phone_number)
                user.phone_number = phone_number
                has_changes = True
     
            if birthdate_str:
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
                if birthdate != user.birthdate:
                    user.birthdate = birthdate
                    has_changes = True
       
            if has_changes:
                user.save()
                print("guardo")
                return redirect("/usuarios/perfil") 
        if form_type == 'verificacion_form':
            print("pidio verificaion")
            user.verification_requested= True
            user.verification_canceled= False
            admin = User.objects.filter(type_user=3).first()
            noti = Notification(title='Nueva solicitud de verificación',user=admin,content=f'El usuario {user.name} {user.surname} pidio ser verificado',link=f'/usuarios/listado')
            noti.save()
            user.save()
            
            return redirect("/usuarios/perfil")
        else:   
            return redirect("/usuarios/perfil")
    return render(request, 'usuarios/perfil.html', {'user':user}) 


def ver_listado(request):
    session_usuario = request.session.get('usuario')
    if session_usuario is None or len(session_usuario) == 0:
        return redirect("/")
    
    try:
        user = User.objects.get(email=session_usuario[0])
    except ObjectDoesNotExist:
        return redirect("/")
    
    if user.type_user is None or user.type_user < 3:
        return redirect("/")
    usuarios = User.objects.exclude(type_user=3)
    print("aca abajo!!")
    for usuario in usuarios:
        print(usuario.name)
    if request.method == 'POST':
        action = request.POST.get('action')
        user_email = request.POST.get('user_email')
        user_solicitud = User.objects.get(email=user_email)
        
        if action == 'aceptar':

            user_solicitud.verification_requested = False
            user_solicitud.save()
            user_solicitud.type_user = 1  
            user_solicitud.save()
            messages.success(request, f'La verificación de {user_solicitud.name} ha sido aceptada.')
            noti = Notification(title='Verificación aceptada',user=user_solicitud,content='Has sido verificado con éxito, ya podés realizar publicaciones.',link=f'/usuarios/perfil')
            noti.save()
        elif action == 'rechazar':
            # Lógica para rechazar la solicitud de verificación
            user_solicitud.verification_requested = False
            user_solicitud.save()
            user_solicitud.type_user = 0  
            user_solicitud.save()
            user_solicitud.verification_canceled = True
            user_solicitud.save()
            messages.success(request, f'La verificación de {user_solicitud.name} no ha sido aceptada.')
            noti = Notification(title='Verificación rechazada',user=user_solicitud,content=f'Tu solicitud de verificación ha sido rechazada, revisá tus datos e intentalo nuevamente.',link=f'/usuarios/perfil')
            noti.save()
        elif action == 'eliminar':
            # Lógica para rechazar la solicitud de verificación
            user_solicitud.verification_requested = False
            user_solicitud.save()
            user_solicitud.type_user = 0  
            user_solicitud.save()
            user_solicitud.verification_canceled = True
            user_solicitud.save()
            messages.success(request, f'Se elimino la verificacion de {user_solicitud.name}.')
            noti = Notification(title='Se elimino su verificacion',user=user_solicitud,content=f'Usted deja de estar verificado',link=f'/usuarios/perfil')
            noti.save()
        elif action == 'verificar':
            user_solicitud.verification_requested = False
            user_solicitud.save()
            user_solicitud.type_user = 1  
            user_solicitud.save()
            user_solicitud.verification_canceled = False
            user_solicitud.save()
            messages.success(request, f'La verificación de {user_solicitud.name} ha sido realizada.')
            noti = Notification(title='Verificación aceptada',user=user_solicitud,content='Has sido verificado con éxito, ya podés realizar publicaciones.',link=f'/usuarios/perfil')
            noti.save()
        usuarios = User.objects.exclude(type_user=3)
        return redirect("/usuarios/listado")
        #return render(request, 'usuarios/listado.html', {'usuarios': usuarios})
    else:
        return render(request, 'usuarios/listado.html', {'usuarios': usuarios})

def ver_listado_publicaciones(request):
    session_usuario = request.session.get('usuario')
    if session_usuario is None or len(session_usuario) == 0:
        return redirect("/")
    
    try:
        user = User.objects.get(email=session_usuario[0])
    except ObjectDoesNotExist:
        return redirect("/")
    
    if user.type_user is None or user.type_user < 2:
        return redirect("/")
    ofertas = Offer.objects.filter(answer=2, post__state=1)
        
    if request.method == 'POST':
        action = request.POST.get('action')
        id = request.POST.get('publicacion.id')
        ofertaId = request.POST.get('oferta.id')
        oferta = Offer.objects.get(id=ofertaId)
        post = get_object_or_404(Post, id = id)
        if action == 'aceptar':
            post.state = 2  
            post.save()
            offers = Offer.objects.filter(post=post)
            for offer in offers:
                if (offer.answer == 0):
                    offer.answer = 1
                    offer.save()
            noti = Notification(title='Intercambio finalizado',
                                user=post.user,
                                content=f'El intercambio entre tu publicación "{post.title}" y la oferta "{oferta.title}" ha sido registrado como finalizado y tu publicación fue terminada. Si este no es el caso, por favor contactate con soporte.',
                                link=f'')
            noti.save()
            noti.link = f'/usuarios/notificaciones/ver/{noti.id}/'
            noti.save()
            noti = Notification(title='Intercambio finalizado',
                                user=oferta.user,
                                content=f'El intercambio entre tu oferta "{oferta.title}" y la publicación "{post.title}" ha sido registrado como finalizado. Si este no es el caso, por favor contactate con soporte.',
                                link=f'')
            noti.save()
            noti.link = f'/usuarios/notificaciones/ver/{noti.id}/'
            noti.save()
            print("funciono")
            ofertas = Offer.objects.filter(answer=2)
        elif action == 'rechazar':
            oferta.answer = 1
            oferta.save()
            post.state = 0  
            post.save()
            noti = Notification(title='Intercambio fallido',
                                user=post.user,
                                content=f'El intercambio entre tu publicación "{post.title}" y la oferta "{oferta.title}" ha sido registrado como fallido. Si no sabes la razón, por favor comunicate con soporte.',
                                link=f'')
            noti.save()
            noti.link = f'/usuarios/notificaciones/ver/{noti.id}/'
            noti.save()
            noti = Notification(title='Intercambio fallido',
                                user=oferta.user,
                                content=f'El intercambio de tu oferta "{oferta.title}" y la publicación "{post.title}" ha sido registrado como fallido. Si no sabes la razón, por favor contactate con soporte.',
                                link=f'')
            noti.save()
            noti.link = f'/usuarios/notificaciones/ver/{noti.id}/'
            noti.save()
            ofertas = Offer.objects.filter(answer=2)
        return redirect("/usuarios/listado/publicaciones")
    return render(request,'usuarios/listadoPublicaciones.html',{'ofertas':ofertas,})

def ver_publicaciones(request):

    user_posts = Post.objects.filter(user_id=request.session.get('usuario')[0])

    # Obtener los ids de posts que tienen ofertas sin respuesta
    post_ids_con_ofertas_sin_respuesta = Offer.objects.filter(answer=0).values_list('post_id', flat=True)

    # Filtrar los user_posts para excluir los posts que tienen ofertas sin respuesta o que no tienen ofertas
    posts_sin_ofertas_sin_respuesta = user_posts.exclude(id__in=post_ids_con_ofertas_sin_respuesta).values_list('id', flat=True)
    
    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts, "postOK": posts_sin_ofertas_sin_respuesta})

def ver_notificaciones(request):
    notificaciones = Notification.objects.order_by("-date").filter(user=request.session.get('usuario')[0])
    return render(request, "usuarios/ver_notificaciones.html", {"todas_notificaciones": notificaciones})

def leer_notificacion(request,id_notificacion):
    notificacion = Notification.objects.get(id=id_notificacion)
    notificacion.read = True
    notificacion.save()
    return redirect(notificacion.link)

def ver_notificacion(request,id_notificacion):
    if id_notificacion != 0:
        notificacion = Notification.objects.get(id=id_notificacion)
    else:
        notificacion = None
    return render(request, "usuarios/ver_notificacion.html", {'notificacion' : notificacion})

def ver_publicaciones_guardadas(request):
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    publicaciones_guardadas = usuario.saved_posts.all

    return render(request, "ver_publicaciones_guardadas.html", {"posts": publicaciones_guardadas })

def eliminar_publicacion(request, post_id):

    post = get_object_or_404(Post,id = post_id)
    offers = Offer.objects.filter(post=post)
    for offer in offers:
        notificaciones = Notification.objects.filter(link=f'/ofertas/{offer.id}')
        for noti in notificaciones:
            noti.link = '/usuarios/notificaciones/ver/0/'
            noti.save()
    comentarios = Comment.objects.filter(post=post)
    for comment in comentarios:
        notificaciones = Notification.objects.filter(link=f'/publicaciones/{post_id}#comentario{comment.id}')
        for noti in notificaciones:
            noti.link = '/usuarios/notificaciones/ver/0/'
            noti.save()
    post.delete()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Construye la ruta relativa desde el directorio base del proyecto
    relative_path = os.path.join(base_dir, 'media', 'publicaciones', str(post.patent))
    # Normaliza la ruta
    relative_path = os.path.normpath(relative_path)
    print(relative_path)
    shutil.rmtree(relative_path)
    messages.success(request, "Publicacion eliminada exitosamente")
    return redirect("/usuarios/publicaciones")

def editar_publicacion(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    old_image_url = post.image.url.lstrip('/')  # Remove leading slash
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(data=request.POST, instance=post, files=request.FILES, exclude_patent = True)
        if form.is_valid():
            old_image_path = os.path.join(settings.MEDIA_ROOT, old_image_url.replace('/', os.sep))

            # Ensure the 'media' is not duplicated in the path
            old_image_path = old_image_path.replace(os.sep + 'media', '', 1)

            # Verificar si el archivo existe y eliminarlo
            if (form.cleaned_data["image"] != old_image_path):
                default_storage.delete(old_image_path)
            form.save()
            messages.success(request, "Publicacion modificada exitosamente")
            return redirect('/usuarios/publicaciones')
    else:
        form = FormularioRegistrarPublicacion(instance=post, exclude_patent = True), 

    return render(request, "editar_publicacion.html", {'post': form})


def ver_ofertas_recibidas(request):
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])
    ofertas_recibidas = Offer.objects.filter(post__in= user_posts)
    return render(request, "ver_ofertas_recibidas.html", {"offers": ofertas_recibidas})


def ver_ofertas_realizadas(request):
    user_offers = Offer.objects.filter(user_id= request.session.get('usuario')[0])
    return render(request, "ver_ofertas_realizadas.html", {"offers": user_offers})


def eliminar_oferta(request, offer_id):

    offer = get_object_or_404(Offer,id = offer_id)
    noti = Notification.objects.get(link=f'/ofertas/{offer.id}')
    noti.link = '/usuarios/notificaciones/ver/0/'
    noti.save()
    offer.delete()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Construye la ruta relativa desde el directorio base del proyecto
    relative_path = os.path.join(base_dir, 'media', 'ofertas', str(offer.user.email), str(offer.post.patent))
    # Normaliza la ruta
    relative_path = os.path.normpath(relative_path)
    print(relative_path)
    shutil.rmtree(relative_path)
    messages.success(request, "Oferta eliminada exitosamente")
    return redirect("/usuarios/ofertasRealizadas")

def editar_oferta(request, offer_id):
    offer = get_object_or_404(Offer,id = offer_id)
    old_image_url = offer.image.url.lstrip('/')  # Remove leading slash
    if request.method == 'POST':
        form = FormularioRegistrarOferta(data=request.POST, instance=offer, files=request.FILES)
        if form.is_valid():
            old_image_path = os.path.join(settings.MEDIA_ROOT, old_image_url.replace('/', os.sep))

            # Ensure the 'media' is not duplicated in the path
            old_image_path = old_image_path.replace(os.sep + 'media', '', 1)

            # Verificar si el archivo existe y eliminarlo
            if (form.cleaned_data["image"] != old_image_path):
                default_storage.delete(old_image_path)
            form.save()
            messages.success(request, "Oferta modificada exitosamente")
            return redirect('/usuarios/ofertasRealizadas')
    else:
        form = FormularioRegistrarOferta(instance=offer), 

    return render(request, "editar_oferta.html", {'offer': form})

def aceptar_oferta(request, offer_id):

    offer = get_object_or_404(Offer,id = offer_id)
    offer.answer = 2
    offer.post.state = 1
    offer.save()
    offer.post.save()
    noti = Notification(title='Oferta aceptada',
                        user=offer.user,
                        content=f'Tu oferta "{offer.title}" de la publicación "{offer.post.title}" ha sido aceptada. Ahora deberás esperar la comunicación del personal del puerto para llevar el intercambio adelante.',
                        link=f'')
    noti.save()
    noti.link = f'/usuarios/notificaciones/ver/{noti.id}/'
    noti.save()
    personal = User.objects.filter(type_user=2)
    for persona in personal:
        noti = Notification(title='Oferta aceptada',
                        user=persona,
                        content=f'Se ha aceptado la oferta "{offer.title}" de la publicación "{offer.post.title}".',
                        link=f'/usuarios/listado/publicaciones')
        noti.save()
    messages.success(request, "Oferta aceptada exitosamente")
    return redirect("/usuarios/ofertasRecibidas")

def rechazar_oferta(request, offer_id):

    offer = get_object_or_404(Offer,id = offer_id)
    offer.answer = 1
    offer.save()
    noti = Notification(title='Oferta rechazada',
                        user=offer.user,
                        content=f'Tu oferta "{offer.title}" de la publicación "{offer.post.title}" ha sido rechazada.',
                        link=f'/ofertas/{offer.id}')
    noti.save()
    messages.success(request, "Oferta rechazada exitosamente")
    return redirect("/usuarios/ofertasRecibidas")

def crear_reporte(request):
    if (request.session.get('usuario') != None):
        content_type = request.POST["content_type"]
        id = request.POST["id"]
        id_url = request.POST["url"]
        reportado = request.POST['reportado']
    else: 
        messages.error(request, "¡Debe iniciar sesión para poder reportar!")
        return redirect ('/autenticacion/inicioSesion')
    return render(request, "usuarios/motivoReporte.html", {'id': id, 'content_type': content_type, 'id_url': id_url, 'reportado': reportado})

def motivo_reporte(request):
    if request.method == 'POST':
        content_type = request.POST["content_type"]
        id = request.POST["id"]
        elemento = get_object_or_404(eval(content_type), id=id)
        id_url = request.POST["id_url"]
        if(content_type == "Conversation"):
            reportado = request.POST["reportado"]
            if(reportado == 'sender'):
                usuario = elemento.sender
            else: 
                usuario = elemento.recipient
            reported_user = usuario
        else:
            reported_user = elemento.user
        report_reason = request.POST["motivoReporte"]
        reported_user.is_reported = True;
        reported_user.save()
        reporte = Report(
            user=reported_user,
            reason=report_reason,
            content_type=ContentType.objects.get_for_model(elemento),
            object_id=elemento.id,
            url = id_url
        )
        reporte.save()
        messages.success(request, "Reporte realizado exitosamente")
    return redirect("/")