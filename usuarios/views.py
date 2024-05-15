from django.shortcuts import render
from db.models import User

def ver_perfil(request):
    return render(request, 'usuarios/perfil.html')
