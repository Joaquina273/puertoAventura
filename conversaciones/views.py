from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db.models import Conversation, Message, User

def home(request):
    return render(request, 'home.html')

def conversacion(request, conversacion):
    username = request.session.get('usuario')[0]
    room_details = Conversation.objects.get(id=conversacion)
    return render(request, 'conversacion.html', {
        'username': username,
        'room': conversacion,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Conversation.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Conversation.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def enviar(request):
    message = request.POST['message']
    usuario = User.objects.get(email=request.session.get('usuario')[0])
    id_conversacion = Conversation.objects.get(id=request.POST['room_id'])

    new_message = Message.objects.create(content=message, sender=usuario, conversation=id_conversacion)
    new_message.save()
    return HttpResponse('Message sent successfully')

def conseguir_mensajes(request, conversacion):
    conversacion = Conversation.objects.get(id=conversacion)

    mensajes = Message.objects.filter(conversation=conversacion)
    mensajes = list(mensajes.values())
    for mensaje in mensajes:
        usuario = User.objects.get(email=mensaje['sender_id'])
        mensaje['sender'] = f'{usuario.name} {usuario.surname}'
    return JsonResponse({"messages":mensajes})