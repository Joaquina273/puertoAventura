from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm

# Create your views here.
def registro(request):
    return render(request, 'registro.html',{
        'form': NameForm
    }
    )
