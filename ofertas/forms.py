from django import forms
from db.models import Offer,User

class FormularioRegistrarOferta(forms.ModelForm):
    
    title = forms.CharField(label= "Titulo", max_length=30, widget = forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label= "Descripción", max_length=500, widget = forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label = "Imagen", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Offer
        fields = ["title", "description","image"]
        
    
    """def clean_patent(self):
        patent = self.cleaned_data.get('patent')
        if Post.objects.filter(patent=patent).exists():
            raise forms.ValidationError("Ya existe una publicación con esa patente registrada en el sistema")
        return patent"""