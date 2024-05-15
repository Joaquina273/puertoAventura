from django.shortcuts import render, redirect
from django.http import JsonResponse
from db.models import Post,User
from autenticacion.views import se_encuentra_conectado

# Create your views here.


def ver_publicaciones(request, user_email):

    user_posts = Post.objects.filter(user_id=user_email)
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