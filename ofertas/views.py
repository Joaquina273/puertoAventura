from django.shortcuts import render
from db.models import Offer,User

# Create your views here.

def ver_oferta(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    return render(request, "ver_oferta.html", {"offer": offer})

def ver_imagen(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    return render(request, "ver_oferta.html", {"image": offer.image})

