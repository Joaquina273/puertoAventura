from db.models import Notification

def navbar_variables (request):
    if (request.session.get('usuario') != None):
        notificaciones = Notification.objects.order_by("-date").filter(user=request.session.get('usuario')[0])[0:3]
        sin_leer = Notification.objects.filter(user=request.session.get('usuario')[0]).filter(read=False)
    else:
        notificaciones = None
        sin_leer = None
    return {
        'usuario' : request.session.get('usuario'),
        'notificaciones' : notificaciones,
        'sin_leer' : sin_leer
    }