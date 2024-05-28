from db.models import Notification

def navbar_variables (request):
    if (request.session.get('usuario') != None):
        notificaciones = Notification.objects.filter(user=request.session.get('usuario')[0])
    else:
        notificaciones = None
    return {
        'usuario' : request.session.get('usuario'),
        'notificaciones' : notificaciones 
    }