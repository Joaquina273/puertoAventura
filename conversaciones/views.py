from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db.models import Conversation, Message, User
from django.utils import timezone

def conversacion(request, conversacion):
    username = request.session.get('usuario')[0]
    room_details = Conversation.objects.get(id=conversacion)
    return render(request, 'conversacion.html', {
        'username': username,
        'conversacion': room_details
    })

def enviar(request):
    message = request.POST['message']
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    conversacion = Conversation.objects.get(id=request.POST['room_id'])
    conversacion.updated_at = timezone.now()
    conversacion.save()

    new_message = Message.objects.create(content=message, sender=usuario, conversation=conversacion)
    new_message.save()
    return HttpResponse('Message sent successfully')

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
    return JsonResponse({"messages":mensajes})