from django.shortcuts import render
from autenticacion.views import se_encuentra_conectado

def ver_perfil(request):
    usuario_conectado = se_encuentra_conectado(request)
    return render(request, 'usuarios/perfil.html', {'usuario': usuario_conectado})
