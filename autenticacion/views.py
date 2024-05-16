from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegistrarUsuario
from db.models import User
from django.core.mail import EmailMessage
import random

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

def inicio_de_sesion (request):
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
                    return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : f"La contraseña ingresada es incorrecta. Te quedan {usuario.tries_left} intentos."  
                })
                else:
                    return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : f"Tu cuenta se encuentra bloqueada. Debes recuperar la contraseña para volver a ingresar."  
                })
        else:
            return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : "El email ingresado no se encuentra registrado."  
                })
                    
    return render(request,"autenticacion/inicio_sesion.html")

def cambio_contrasenia (request):
    return render(request,"autenticacion/cambio_contrasenia.html", {'usuario' : se_encuentra_conectado(request)})

def cerrar_sesion (request):
    request.session.clear()
    return redirect("/")

def generar_codigo():
    codigo = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return int(codigo)

def recuperar_contrasenia (request):
    if (request.method == 'POST'):
        mail = request.POST['email']
        if(User.objects.filter(email=mail).exists()):
            usuario = User.objects.get(email=mail)
            usuario.recovery_ID = generar_codigo()
            usuario.save()
            email = EmailMessage(
            subject='Recuperá tu contraseña de Puerto Aventura',
            body=f' ¡Hola {usuario.name}! Este es el codigo para recuperar la contraseña de tu cuenta: {usuario.recovery_ID}. Si vos no pediste este codigo o ya pudiste ingresar a tu cuenta, ignorá este mensaje.',
            from_email='Puerto Aventura',
            to=[usuario.email],
            )
            email.send()
            request.session['recupera'] = usuario.email
            return redirect('/autenticacion/recuperarContrasenia/codigo')
        else:
            return render(request,'autenticacion/recuperar_contrasenia.html',{'mensaje_error':'El email ingresado no se encuentra registrado en el sistema.'})
    return render(request,'autenticacion/recuperar_contrasenia.html')

def ingresar_codigo (request):
    if (request.method == 'POST'):
        usuario = User.objects.get(email=request.session['recupera'])
        if (int(request.POST['code']) == usuario.recovery_ID):
            if (request.POST['password'] == request.POST['password2']):
                usuario.password = request.POST['password']
                usuario.save()
                return render(request,'autenticacion/cambio_exitoso.html')
            else:
                mensaje_error = 'Las contraseñas ingresadas no coinciden, intentalo nuevamente.'
        else:
            mensaje_error = 'El código ingresado es incorrecto, intentalo nuevamente.'
        return render(request, 'autenticacion/ingresar_codigo.html',{'mensaje_error': mensaje_error,'mail':request.session['recupera']})
    return render(request, 'autenticacion/ingresar_codigo.html',{'mail':request.session['recupera']})

def se_encuentra_conectado(request):
    if ('usuario' in request.session):
        return request.session['usuario']
    else:
        return None