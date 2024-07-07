import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from db.models import Conversation, Message, User, Offer
from django.utils import timezone
from django.db.models import Q

def conversacion(request, conversacion):
    username = request.session.get('usuario')[0]
    room_details = Conversation.objects.get(id=conversacion)
    conseguir_mensajes(request,conversacion)
    return render(request, 'conversacion.html', {
        'username': username,
        'conversacion': room_details
    })

def enviar(request):
    message = request.POST['message']
    imagen = request.FILES.get('imagen')
    archivo = request.FILES.get('archivo')
    if (message or imagen or archivo):
        usuario = User.objects.get(email=request.session.get('usuario')[0])
        conversacion = Conversation.objects.get(id=request.POST['room_id'])
        conversacion.updated_at = timezone.now()
        conversacion.save()
        if imagen:
            new_message = Message.objects.create(content=message, sender=usuario, conversation=conversacion)
            new_message.save()
            new_message.image = imagen
        elif archivo:
            new_message = Message.objects.create(content=message, sender=usuario, conversation=conversacion)
            new_message.save()
            new_message.file = archivo
        else:
            new_message = Message.objects.create(content=message, sender=usuario, conversation=conversacion)
        new_message.save()
        return HttpResponse('Message sent successfully')
    else:
        return HttpResponse('Empty message')

def conseguir_mensajes(request, conversacion):
    conversacion = Conversation.objects.get(id=conversacion)

    mensajes = Message.objects.filter(conversation=conversacion)
    sin_leer = mensajes.exclude(sender=request.session.get('usuario')[0]).exclude(read=True)
    for mensaje in sin_leer:
        mensaje.read = True
        mensaje.save()
    mensajes = list(mensajes.values())
    for mensaje in mensajes:
        usuario = User.objects.get(email=mensaje['sender_id'])
        mensaje['sender'] = f'{usuario.name} {usuario.surname}'
        mensaje['avatar'] = usuario.avatar.url
        if mensaje.get('file'):
            mensaje['nombre_archivo'] = mensaje.get('file').split("/")[3]
    return JsonResponse({"messages":mensajes})

def crear_conversacion(request, id_oferta):
    oferta = Offer.objects.get(id=id_oferta)
    conversacion = Conversation(sender=oferta.post.user,recipient=oferta.user)
    conversacion.save()
    return redirect(f'/conversaciones/{conversacion.id}/')

def descargar_archivo(request, id_mensaje):
    message = Message.objects.get(id=id_mensaje)
    
    if message.file:
        file_path = message.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            raise Http404("File does not exist")
    else:
        raise Http404("No file associated with this message")

def ver_conversaciones(request):
    chats = Conversation.objects.order_by("-updated_at").filter(Q(sender=request.session.get('usuario')[0]) | Q(recipient=request.session.get('usuario')[0]))
    chats = list(chats)
    for chat in range(len(chats)):
        no_leido = Message.objects.filter(conversation=chats[chat]).exclude(sender=request.session.get('usuario')[0]).exclude(read=True).exists()
        if (no_leido):
            chats[chat] = {'content': chats[chat], 'read' : False}
        else:
            chats[chat] = {'content': chats[chat], 'read' : True}
    return render(request, 'ver_conversaciones.html', {'todas_conversaciones' : chats})