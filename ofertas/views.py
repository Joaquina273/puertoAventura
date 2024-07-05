from django.shortcuts import render,get_object_or_404
from db.models import Offer,User,Conversation

# Create your views here.

def ver_oferta(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    try:
        chat = Conversation.objects.get(sender=offer.post.user,recipient=offer.user)
    except Conversation.DoesNotExist:
        chat = None
    return render(request, "ver_oferta.html", {"offer": offer, 'chat' : chat})

def ver_imagen(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    return render(request, "ver_oferta.html", {"image": offer.image})

