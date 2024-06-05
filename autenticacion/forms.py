from datetime import date
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
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('Debe tener al menos 18 años para registrarse')
        return birth_date

    def save(self, commit=True, avatar= None):
        user = super(RegistrarUsuario, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.birthdate = self.cleaned_data['birth_date']
        user.phone_number = self.cleaned_data['phone_number']
        if avatar:
            user.avatar = avatar
        if commit:
            user.save()
        return user
    

class cambiar_contrasenia_form (forms.ModelForm):
      
    actual_password = forms.CharField(label='Contraseña actual',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
    }))
    new_password = forms.CharField(label='Nueva contraseña',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
    }))
    confirm_new_password = forms.CharField(label='Repita la nueva contraseña',min_length=8,max_length=20,widget=forms.PasswordInput(attrs={
        'class':'form-control',
    }))

    class Meta:
        model = User
        fields = ("actual_password", "new_password", "confirm_new_password")
       