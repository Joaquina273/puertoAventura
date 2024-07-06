from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db.models import Conversation, Message, User, Offer
from django.utils import timezone
from django.core.files import File

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
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    conversacion = Conversation.objects.get(id=request.POST['room_id'])
    conversacion.updated_at = timezone.now()
    conversacion.save()
    print('llegue')
    imagen = request.FILES.get('imagen')
    if imagen:
        new_message = Message.objects.create(content=message, sender=usuario, conversation=conversacion,image=imagen)
    else:
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

def crear_conversacion(request, id_oferta):
    oferta = Offer.objects.get(id=id_oferta)
    conversacion = Conversation(sender=oferta.post.user,recipient=oferta.user)
    conversacion.save()
    return redirect(f'/conversaciones/{conversacion.id}/')