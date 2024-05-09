from django.shortcuts import render

# Create your views here.
def inicioDeSesion (request):
    return render(request,"inicioSesion.html")