from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrarUsuario

# Create your views here.
def registro(request):
    return render(request, 'autenticacion/registro.html',{
        'form': RegistrarUsuario()
    }
    )

def inicioDeSesion (request):
    return render(request,"autenticacion/inicioSesion.html")