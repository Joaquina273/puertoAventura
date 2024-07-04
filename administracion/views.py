from django.shortcuts import render
from db.models import User, Report

def ver_reportes(request):
     reports = Report.objects.all();
     return render(request, 'administracion/reportes.html', { "reportes": reports})

def bloqueo(request):
     reports = Report.objects.all();
     action = request.POST.get('action')
     reporteId = request.POST.get('reporte')
     reporte = Report.objects.get(id=reporteId)
     usuario = reporte.user
     if action == 'rechazar':
          reporte.is_resolved = True;
          reporte.save()
     elif action == 'bloquear':
          reporte.is_resolved = True;
          reporte.save()
          usuario.is_blocked = True;
          usuario.save()
     return render(request,'administracion/reportes.html', {"reportes": reports})

     