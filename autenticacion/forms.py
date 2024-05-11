from django import forms
from db.models import User
class RegistrarUsuario(forms.ModelForm):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ejemplo@ejemplo.com'
    }))
    password1 = forms.CharField(label='Contraseña',max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'label' : 'contraseña'
    }))
    password2 = forms.CharField(label='Repita la contraseña',max_length=20,widget=forms.PasswordInput(attrs={
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