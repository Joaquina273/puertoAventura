from django.shortcuts import render, redirect
from .forms import RegistrarUsuario, cambiar_contrasenia_form
from db.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
import random

# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuario(request.POST)
        if form.is_valid():
            form.save()
            email = EmailMessage(
                subject='¡Bienvenido a Puerto Aventura!',
                body=f' ¡Hola {form.cleaned_data["name"]}! Estamos muy contentos de que te hayas animado a vivir esta aventura juntos. Esperamos que tengas una buena experiencia utilizando nuestra página.'
                + ' Cualquier duda no dudes en contactarte con nuestro equipo. Saludos aventurero.',
                from_email='Puerto Aventura',
                to=[form.cleaned_data['email']],
                )
            email.send(fail_silently=True)
            messages.success(request,"¡Usuario registrado exitosamente!")
            #request.session['mensaje_exito'] = "¡Usuario registrado exitosamente!"
            return redirect('/autenticacion/inicioSesion')
        else: 
            return render(request, 'autenticacion/registro.html', { 'form':form, 'mensaje_error': form.errors })
    form = RegistrarUsuario()
    return render(request, 'autenticacion/registro.html', {'form':form})

def cambio_contraseña(request):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    email = request.session['usuario'][0]
    if (request.method == 'POST'):
        form = cambiar_contrasenia_form(request.POST)
        user = User.objects.get(email=email)
        new_password = request.POST['new_password']
        actual_password = request.POST['actual_password']
        confirm_new_password = request.POST['confirm_new_password']
        db_password = user.password
        if(db_password == actual_password):
            if(new_password == confirm_new_password):
                user.password = new_password
                user.save()
                request.session.clear()
                messages.success(request,"¡Cambio de contraseña realizado exitosamente!")
                return redirect('/autenticacion/inicioSesion') #debería cerrar sesion
            else:
                messages.error(request,"Las contraseñas nuevas no coinciden, vuelve a intentarlo")
                return render(request, 'autenticacion/cambio_contrasenia.html', { 'form':form })
        else:
            return render(request, 'autenticacion/cambio_contrasenia.html', { 'form':form, 'mensaje_error': 'la contraseña actual es incorrecta' })
    form = cambiar_contrasenia_form()
    return render(request, 'autenticacion/cambio_contrasenia.html', {'usuario' : request.session.get('usuario'),'form':form,'type_user':tipoo_user})


def inicio_de_sesion (request):
    if (request.method == 'POST'):
        mail = request.POST['email']
        if(User.objects.filter(email=mail).exists()):
            usuario = User.objects.get(email=mail)
            contrasenia = request.POST['password']
            if ((usuario.password == contrasenia) and (usuario.tries_left > 1)):
                usuario.tries_left = 5
                usuario.save()
                request.session['usuario'] = mail, usuario.name
                return redirect("/")
            else:
                if (usuario.tries_left > 1):
                    usuario.tries_left -= 1
                    usuario.save()
                    messages.error(request, f"La contraseña ingresada es incorrecta. Te quedan {usuario.tries_left} intentos.")
                    return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : f"La contraseña ingresada es incorrecta. Te quedan {usuario.tries_left} intentos."  
                })
                else:
                    messages.error(request, "Tu cuenta se encuentra bloqueada. Debes recuperar la contraseña para volver a ingresar.")
                    return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : "Tu cuenta se encuentra bloqueada. Debes recuperar la contraseña para volver a ingresar."  
                })
        else:
            messages.error(request, "El email ingresado no se encuentra registrado.")
            return render (request, "autenticacion/inicio_sesion.html", {
                    "mensaje_error" : "El email ingresado no se encuentra registrado."  
                })
    return render(request,"autenticacion/inicio_sesion.html",{'mensaje_exito': request.session.get('mensaje_exito')})

def cerrar_sesion (request):
    request.session.clear()
    return render(request,'autenticacion/cierre_exitoso.html')

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
            try:
                email.send()
                request.session['recupera'] = usuario.email
                return redirect('/autenticacion/recuperarContrasenia/codigo')
            except Exception:
                messages.error(request, 'Hubo un problema en la conexión con el servidor. Por favor intentalo nuevamente')
                return render(request,'autenticacion/recuperar_contrasenia.html',{'mensaje_error':'Hubo un problema en la conexión con el servidor. Por favor intentalo nuevamente'})
        else:
            messages.error(request, 'El email ingresado no se encuentra registrado en el sistema')
            return render(request,'autenticacion/recuperar_contrasenia.html',{'mensaje_error':'El email ingresado no se encuentra registrado en el sistema.'})
    return render(request,'autenticacion/recuperar_contrasenia.html')

def ingresar_codigo (request):
    if (request.method == 'POST'):
        usuario = User.objects.get(email=request.session['recupera'])
        if (int(request.POST['code']) == usuario.recovery_ID):
            if (request.POST['password'] == request.POST['password2']):
                usuario.password = request.POST['password']
                usuario.tries_left = 5
                usuario.save()
                return render(request,'autenticacion/cambio_exitoso.html')
            else:
                messages.error(request, 'Las contraseñas ingresadas no coinciden, intentalo nuevamente.')
        else:
            messages.error(request, 'El código ingresado es incorrecto, intentalo nuevamente.')
        return render(request, 'autenticacion/ingresar_codigo.html',{'mail':request.session['recupera']})
    return render(request, 'autenticacion/ingresar_codigo.html',{'mail':request.session['recupera']})
