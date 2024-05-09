from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm
from .forms import RegistrarUsuario

# Create your views here.

def user_login(request):
    if request.methos == "POST":
        form = LoginForm(request.post)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                email = cd["email"],
                                password = cd["password"])
            if user is not None:
                if user.is_active():
                    login(request,user)
                    return HttpResponse("Usuario autenticado")
                else:
                    return HttpResponse("El usuario no está activo")
            else:
                return HttpResponse("La información ingresada es incorrecta")
    else:
        form = LoginForm()
        return render(request, "cuenta/login.html", {"form": form})


def registro(request):
    return render(request, 'autenticacion/registro.html',{
        'form': RegistrarUsuario()
    }
    )
