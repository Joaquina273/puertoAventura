from db.models import Notification, Conversation
from db.models import User

def navbar_variables (request):
    if (request.session.get('usuario') != None):
        notificaciones = Notification.objects.order_by("-date").filter(user=request.session.get('usuario')[0])[0:3]
        for noti in notificaciones:
            if (len(noti.content) > 75):
                noti.content = f'{" ".join(noti.content.split()[0:9])}...'
        sin_leer = Notification.objects.filter(user=request.session.get('usuario')[0]).filter(read=False)
        user=User.objects.filter(email=request.session.get('usuario')[0]).first
        chats = None
        #chats = Conversation.objects.order_by("-updated_at").filter(sender=request.session.get('usuario')[0] or recipient=request.session.get('usuario')[0])
    else:
        notificaciones = None
        sin_leer = None
        user = None
        chats = None
    return {
        'usuario' : user,
        'notificaciones' : notificaciones,
        'sin_leer' : sin_leer,
        'chats' : chats
    }