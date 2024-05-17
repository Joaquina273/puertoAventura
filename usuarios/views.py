import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from db.models import Post,User
from publicaciones.forms import FormularioRegistrarPublicacion
from autenticacion.views import se_encuentra_conectado

# Create your views here.


def ver_publicaciones(request):

    user_posts = Post.objects.filter(user_id=se_encuentra_conectado(request)[0])
    return render(request, "ver_publicaciones_usuario.html", {"posts": user_posts, 'usuario': se_encuentra_conectado(request)})

def eliminar_publicacion(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': 'Post eliminado exitosamente'}, status=204)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

    """post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect(' ')  
    return render(request, 'confirm_delete.html', {'post': post})"""

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
            default_storage.delete(old_image_path)
            form.save()
            return redirect('/usuarios/publicaciones')
        else:
            print(form.errors)
    else:
        form = FormularioRegistrarPublicacion(instance=post, exclude_patent = True), 

    return render(request, "editar_publicacion.html", {'post': form, 'usuario': se_encuentra_conectado(request)})
