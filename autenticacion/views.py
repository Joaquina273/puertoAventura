from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegistrarUsuario
from db.models import User

# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuario(request.POST)
        if form.is_valid():
            form.save() 
        else: 
            print(form.errors)#Saving form user data in the model
    form = RegistrarUsuario()
    return render(request, 'autenticacion/registro.html', { 'form':form })

def inicioDeSesion (request):
    if (request.method == 'POST'):
        mail = request.POST['email']
        if(User.objects.filter(email=mail).exists()):
            usuario = User.objects.get(email=mail)
            contrasenia = request.POST['password']
            if (usuario.password == contrasenia):
                usuario.tries_left = 5
                usuario.save()
                request.session['usuario'] = mail, usuario.name
                return redirect("/autenticacion/cambioContrasenia")
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
    return render(request,"autenticacion/cambio_contrasenia.html", {'usuario' : seEncuentraConectado(request)})

def cerrarSesion (request):
    request.session.clear()
    return redirect("/autenticacion/registro")

def seEncuentraConectado(request):
    if ('usuario' in request.session):
        return request.session['usuario']
    else:
        return None