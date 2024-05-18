from django import forms
from db.models import Port,Post,User

class FormularioRegistrarPublicacion(forms.ModelForm):
    
    title = forms.CharField(label= "Titulo", max_length=40, widget = forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.IntegerField(label="Valor", widget= forms.NumberInput(attrs= {'class':'form-control'}))
    image = forms.ImageField(label = "Imagen", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    patent = forms.CharField(label= "Patente", max_length=20, widget = forms.TextInput(attrs={'class': 'form-control'}))
    eslora = forms.DecimalField(label="Eslora", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    model = forms.CharField(label= "Modelo", max_length=40, widget = forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.ModelChoiceField(label="Puerto", queryset=Port.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ["title","value","image","patent","eslora","model","ship_type","port"]
        
    def __init__(self, *args, **kwargs):
        exclude_patent = kwargs.pop('exclude_patent', False)  # Obtener el valor de exclude_patent, si no se proporciona, será False
        super().__init__(*args, **kwargs)

        if exclude_patent:
            self.fields.pop('patent')  # Excluir el campo de patente si se establece exclude_patent como True
    
    def clean_patent(self):
        patent = self.cleaned_data.get('patent')
        if Post.objects.filter(patent=patent).exists():
            raise forms.ValidationError("Ya existe una publicación con esa patente registrada en el sistema")
        return patent