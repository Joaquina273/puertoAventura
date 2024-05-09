from django import forms

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)

class RegistrarUsuario(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ejemplo@ejemplo.com'
    }))
    contraseña = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    apellido = forms.CharField(max_length=20,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    fecha_nacimiento = forms.DateField(widget=forms.SelectDateWidget(years=range(1924,2024),attrs={
        'class':'form-control'
    }))