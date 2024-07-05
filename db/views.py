from django.shortcuts import render, redirect
from db.models import User, Rating
from django.contrib import messages

def rating(request):
    url = request.POST.get('url')
    if (request.method == 'POST'):
        usuarioEmail = request.session.get('usuario')[0]
        usuario = User.objects.get(email=usuarioEmail)
        rate = request.POST.get('rating')
        rating = Rating(
            user = usuario,
            score = rate
        )
        rating.save()
        messages.success(request, "Gracias por su opinión!")
    return redirect(url)
