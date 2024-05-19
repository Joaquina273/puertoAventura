import datetime
import os
import shutil
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from db.models import Post,User
from publicaciones.forms import FormularioRegistrarPublicacion
from django.http import JsonResponse

# Create your views here.
def ver_perfil(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone_number = request.POST.get('phone_number')
        birthdate_str = request.POST.get('birthdate')

        # Check for changes
        has_changes = False

        if name and name != user.name:
            user.name = name
            has_changes = True
        print(has_changes)
        if surname and surname != user.surname:
            user.surname = surname
            has_changes = True
        print(has_changes)
        telefono_usuario = int(phone_number)
        if phone_number and user.phone_number != telefono_usuario:
            print(phone_number)
            print(user.phone_number)
            user.phone_number = phone_number
            has_changes = True
        print(has_changes)
        if birthdate_str:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            if birthdate != user.birthdate:
                user.birthdate = birthdate
                has_changes = True
        print(has_changes)
        if has_changes:
            user.save()
            print("guardo")
            mensaje = "Cambios guardados"
            return render(request, 'usuarios/perfil.html', {'usuario': request.session.get('usuario'),'user':user,'type_user':tipoo_user}) 
        else:
            print("hola")   
            return render(request, 'usuarios/perfil.html', {'usuario': request.session.get('usuario'),'user':user,'type_user':tipoo_user}) 
    return render(request, 'usuarios/perfil.html', {'usuario': request.session.get('usuario'),'user':user,'type_user':tipoo_user}) 


def ver_publicaciones(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])
    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts, 'usuario': request.session.get('usuario'),'type_user':tipoo_user})

def ver_publicaciones_guardadas(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    usuario_publicaciones_guardadas = usuario.saved_posts.all
    return render(request, "ver_publicaciones_guardadas.html", {"posts": usuario_publicaciones_guardadas, 'usuario': request.session.get('usuario'),'type_user':tipoo_user})

def eliminar_publicacion(request, post_id):

    post = get_object_or_404(Post,id = post_id)
    post.delete()

    folder_path = os.path.join("C:\\Users\\x1\\Desktop\\Facultad\\Tercer Año\\Ingenieria de Software 2\\Puerto Aventura\\puertoAventura\\media\\publicaciones", str(post.patent))

    shutil.rmtree(folder_path)

    messages.success(request, "Publicacion eliminada exitosamente")

    return redirect("/usuarios/publicaciones")


def editar_publicacion(request, post_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    print(tipoo_user)
    post = get_object_or_404(Post, id = post_id)
    
    old_image_url = post.image.url.lstrip('/')  # Remove leading slash
    
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(data=request.POST, instance=post, files=request.FILES, exclude_patent = True)
        if form.is_valid():
            old_image_path = os.path.join(settings.MEDIA_ROOT, old_image_url.replace('/', os.sep))

            # Ensure the 'media' is not duplicated in the path
            old_image_path = old_image_path.replace(os.sep + 'media', '', 1)

            # Verificar si el archivo existe y eliminarlo
            if (form.cleaned_data["image"] == old_image_path):
                default_storage.delete(old_image_path)
            form.save()
            messages.success(request, "Publicacion modificada exitosamente")
            return redirect('/usuarios/publicaciones')
        else:
            print(form.errors)
    else:
        form = FormularioRegistrarPublicacion(instance=post, exclude_patent = True), 

    return render(request, "editar_publicacion.html", {'post': form, 'usuario':  request.session.get('usuario'),'type_user':tipoo_user})
