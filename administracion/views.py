from django.shortcuts import render
from db.models import User

def ver_reportes(request):
     user = User.objects.all()
     return render(request, 'administracion/reportes.html', {"usuarios": user})

