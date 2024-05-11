from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrarUsuario
from db.models import User
from django.contrib.auth import login

# Create your views here.
def registro(request):
    return render(request, 'autenticacion/registro.html',{
        'form': RegistrarUsuario()
    }
    )

def inicioDeSesion (request):
    print("Metodo:", request.method)
    if (request.method == 'POST'):
        mail = request.POST['email']
        if(User.objects.filter(email=mail).exists()):
            usuario = User.objects.get(email=mail)
            contrasenia = request.POST['password']
            if (usuario.password == contrasenia):
                login(request,usuario)
                return HttpResponseRedirect("/")
    return render(request,"autenticacion/inicioSesion.html")

def cambioContrasenia (request):
    return render(request,"autenticacion/cambio_contrasenia.html")
