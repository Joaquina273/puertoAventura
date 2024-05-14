from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrarUsuario
from db.models import User

# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuario(request.POST)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect("/")
        else: 
            return render(request, 'autenticacion/registro.html', { 'form':form,'mensaje_error': form.errors })
    form = RegistrarUsuario()
    return render(request, 'autenticacion/registro.html', {'form':form})

def inicioDeSesion (request):
    if (request.method == 'POST'):
        mail = request.POST['email']
        if(User.objects.filter(email=mail).exists()):
            usuario = User.objects.get(email=mail)
            contrasenia = request.POST['password']
            if (usuario.password == contrasenia):
                usuario.tries_left = 5
                usuario.save()
                return HttpResponseRedirect("/")
            else:
                if (usuario.tries_left > 1):
                    usuario.tries_left -= 1
                    usuario.save()
                    return render (request, "autenticacion/inicioSesion.html", {
                    "mensaje_error" : f"La contraseña ingresada es incorrecta. Te quedan {usuario.tries_left} intentos."  
                })
                else:
                    return render (request, "autenticacion/inicioSesion.html", {
                    "mensaje_error" : f"Tu cuenta se encuentra bloqueada. Debes recuperar la contraseña para volver a ingresar."  
                })
        else:
            return render (request, "autenticacion/inicioSesion.html", {
                    "mensaje_error" : "El email ingresado no se encuentra registrado."  
                })
                    
    return render(request,"autenticacion/inicioSesion.html")

def cambioContrasenia (request):
    return render(request,"autenticacion/cambio_contrasenia.html")
