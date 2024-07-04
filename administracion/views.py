from django.shortcuts import render
from db.models import User, Report

def ver_reportes(request):
     reports = Report.objects.all();
     return render(request, 'administracion/reportes.html', { "reportes": reports})

