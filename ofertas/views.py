from django.shortcuts import render
from db.models import Offer,User

# Create your views here.

def ver_oferta(request, offer_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    offer = Offer.objects.get(id=offer_id)
    user = User.objects.get(email=offer.user_id)
    return render(request, "ver_oferta.html", {"offer": offer,'usuario':  request.session.get('usuario'),'type_user':tipoo_user})

def ver_imagen(request, offer_id):
    usuario=request.session.get('usuario')
    if usuario: 
        user = User.objects.get(email=usuario[0])
        tipoo_user=user.type_user
    else:
        tipoo_user=0
    offer = Offer.objects.get(id=offer_id)
    return render(request, "ver_oferta.html", {"image": offer.image,'usuario':  request.session.get('usuario'),'type_user':tipoo_user})

