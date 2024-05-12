from django.shortcuts import render
from django.contrib.auth import login


def inicio(request):
    return render(request, 'inicio/inicio.html')