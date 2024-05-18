from datetime import date
from django import forms
from db.models import User

class editarPerfil(forms.ModelForm):
     
    password = forms.CharField(label='Contraseña',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'label' : 'contraseña'
    }))
    name = forms.CharField(label='Nombre',max_length=30,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    surname = forms.CharField(label='Apellido',max_length=20,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    birth_date = forms.DateField(label='Fecha de nacimiento',widget=forms.SelectDateWidget(years=range(1924,2024),attrs={
        'class':'form-control'
    }))
    phone_number = forms.IntegerField(label='Numero de telefono',widget=forms.TextInput(attrs={
        'class':'form-control'
    }))