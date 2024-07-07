from db.models import Notification, Conversation, User, Message 
from django.db.models import Q

def navbar_variables (request):
    if (request.session.get('usuario') != None):
        notificaciones = Notification.objects.order_by("-date").filter(user=request.session.get('usuario')[0])[0:3]
        for noti in notificaciones:
            if (len(noti.content) > 75):
                noti.content = f'{" ".join(noti.content.split()[0:9])}...'
        sin_leer = Notification.objects.filter(user=request.session.get('usuario')[0]).filter(read=False)
        user=User.objects.get(email=request.session.get('usuario')[0])
        chats = None
        chats = Conversation.objects.order_by("-updated_at").filter(Q(sender=request.session.get('usuario')[0]) | Q(recipient=request.session.get('usuario')[0]))
        mensajes_sin_leer = 0
        chats = list(chats)
        for chat in range(len(chats)):
            no_leido = Message.objects.filter(conversation=chats[chat]).exclude(sender=request.session.get('usuario')[0]).exclude(read=True).exists()
            if (no_leido):
                mensajes_sin_leer = mensajes_sin_leer + 1
                chats[chat] = {'content': chats[chat], 'read' : False}
            else:
                chats[chat] = {'content': chats[chat], 'read' : True}
            
    else:
        notificaciones = None
        sin_leer = None
        user = None
        chats = None
        mensajes_sin_leer = None
    return {
        'usuario' : user,
        'notificaciones' : notificaciones,
        'sin_leer' : sin_leer,
        'chats' : chats,
        'mensajes_sin_leer' : mensajes_sin_leer
    }