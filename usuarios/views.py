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


# Create your views here.
def ver_perfil(request):
    user = User.objects.get(email=request.session.get('usuario')[0])
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
            return render(request, 'usuarios/perfil.html', {'user':user}) 
        else:
            print("hola")   
            return render(request, 'usuarios/perfil.html', {'user':user}) 
    return render(request, 'usuarios/perfil.html', {'user':user}) 


def ver_publicaciones(request):
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])
    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts})

def ver_notificaciones(request):
    user_posts = Post.objects.filter(user_id= request.session.get('usuario')[0])
    return render(request, "usuarios/ver_notificaciones.html", {"posts": user_posts})

def ver_publicaciones_guardadas(request):
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    usuario_publicaciones_guardadas = usuario.saved_posts.all
    return render(request, "ver_publicaciones_guardadas.html", {"posts": usuario_publicaciones_guardadas})

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

    return render(request, "editar_publicacion.html", {'post': form})
