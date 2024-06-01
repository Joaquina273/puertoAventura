import datetime
import os
import shutil
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from db.models import Post,User,Offer, Notification
from publicaciones.forms import FormularioRegistrarPublicacion
from ofertas.forms import FormularioRegistrarOferta


# Create your views here.
def Lista_usuarios(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
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
                messages.success(request, 'Cambios guardados.')
                return render(request, 'usuarios/perfil.html', {'user':user}) 
        if form_type == 'verificacion_form':
            print("pidio verificaion")
            user.verification_requested=True
            user.save()
            
            return render(request, 'usuarios/perfil.html', {'user':user})
        else:   
            return render(request, 'usuarios/perfil.html', {'user':user}) 
    return render(request, 'usuarios/perfil.html', {'user':user}) 


def ver_listado(request):
    usuarios = User.objects.all()
    print("aca abajo!!")
    for usuario in usuarios:
        print(usuario.name)
    return render(request, 'usuarios/listado.html', {'usuarios': usuarios})


def ver_publicaciones(request):
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])

    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts, 'usuario': request.session.get('usuario')})

def ver_notificaciones(request):
    notificaciones = Notification.objects.order_by("-date").filter(user=request.session.get('usuario')[0])
    return render(request, "usuarios/ver_notificaciones.html", {"todas_notificaciones": notificaciones})

def ver_publicaciones_guardadas(request):
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    publicaciones_guardadas = usuario.saved_posts.all

    return render(request, "ver_publicaciones_guardadas.html", {"posts": publicaciones_guardadas, 'usuario': request.session.get('usuario')})

def eliminar_publicacion(request, post_id):

    post = get_object_or_404(Post,id = post_id)
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

    return render(request, "editar_publicacion.html", {'post': form, 'usuario':  request.session.get('usuario')})


def ver_ofertas_recibidas(request):
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])
    ofertas_recibidas = Offer.objects.filter(post__in= user_posts)
    ofertas_recibidas_disponibles = ofertas_recibidas.filter(answer = 0)
    return render(request, "ver_ofertas_recibidas.html", {"offers": ofertas_recibidas_disponibles, 'usuario': request.session.get('usuario')})


def ver_ofertas_realizadas(request):
    user_offers = Offer.objects.filter(user_id= request.session.get('usuario')[0])
    return render(request, "ver_ofertas_realizadas.html", {"offers": user_offers, 'usuario': request.session.get('usuario')})


def eliminar_oferta(request, offer_id):

    offer = get_object_or_404(Offer,id = offer_id)
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

    return render(request, "editar_oferta.html", {'offer': form, 'usuario':  request.session.get('usuario')})
