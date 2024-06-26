from django.shortcuts import render
from db.models import Post,User

# Create your views here.

def landing_page(request):
    posts = Post.objects.all().order_by("-post_date")
    return render(request, "home.html", {'available_posts' : posts.filter(state=0)[0:3],'finalized_posts' : posts.filter(state=2)})


def visualizar_publicaciones_finalizadas(request):

    publicaciones = Post.objects.filter(state =2)[:3]  # Filtra los primeros tres elementos con state=2
    return render(request, "home.html", {"posts": publicaciones})

