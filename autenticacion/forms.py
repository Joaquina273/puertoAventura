from datetime import datetime
from django import forms
from db.models import User
class RegistrarUsuario(forms.ModelForm):

    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ejemplo@ejemplo.com'
    }))
    password1 = forms.CharField(label='Contraseña',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'label' : 'contraseña'
    }))
    password2 = forms.CharField(label='Repita la contraseña',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control'
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
 
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "name", "surname", "birth_date", "phone_number")
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas ingresadas son distintas")
        return password2
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        age = (datetime.now() - dob).days/365
        if age < 18:
            raise forms.ValidationError('Must be at least 18 years old to register')
        return dob

    def save(self, commit=True):
        user = super(RegistrarUsuario, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.birthdate = self.cleaned_data['birth_date']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user