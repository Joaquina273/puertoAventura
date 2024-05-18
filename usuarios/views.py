import os
import shutil
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from db.models import Post,User
from publicaciones.forms import FormularioRegistrarPublicacion
from autenticacion.views import se_encuentra_conectado

# Create your views here.
def ver_perfil(request):
    usuario_conectado = se_encuentra_conectado(request)
    return render(request, 'usuarios/perfil.html', {'usuario': usuario_conectado})

def ver_publicaciones(request):

    user_posts = Post.objects.filter(user_id=se_encuentra_conectado(request)[0])
    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts, 'usuario': se_encuentra_conectado(request)})

def eliminar_publicacion(request, post_id):

    post = get_object_or_404(Post,id = post_id)
    post.delete()

    folder_path = os.path.join("C:\\Users\\x1\\Desktop\\Facultad\\Tercer Año\\Ingenieria de Software 2\\Puerto Aventura\\puertoAventura\\media\\publicaciones", str(post.patent))

    shutil.rmtree(folder_path)

    messages.success(request, "Publicacion eliminada exitosamente")

    return redirect("/usuarios/publicaciones")


def editar_publicacion(request, post_id):

    post = get_object_or_404(Post, id = post_id)
    
    old_image_url = post.image.url.lstrip('/')  # Remove leading slash
    
    if request.method == 'POST':
        form = FormularioRegistrarPublicacion(data=request.POST, instance=post, files=request.FILES, exclude_patent = True)
        if form.is_valid():
            old_image_path = os.path.join(settings.MEDIA_ROOT, old_image_url.replace('/', os.sep))
            print(old_image_path)
            # Ensure the 'media' is not duplicated in the path
            old_image_path = old_image_path.replace(os.sep + 'media', '', 1)
            print(old_image_path)
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

    return render(request, "editar_publicacion.html", {'post': form, 'usuario': se_encuentra_conectado(request)})
