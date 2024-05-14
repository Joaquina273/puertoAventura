from django import forms
from db.models import Port,Post,User

class FormularioRegistrarPublicacion(forms.ModelForm):
    
    title = forms.CharField(label= "Titulo", max_length=40, widget = forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.IntegerField(label="Valor", widget= forms.NumberInput(attrs= {'class':'form-control'}))
    image = forms.ImageField(label = "Imagen", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    eslora = forms.DecimalField(label="Eslora", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    model = forms.CharField(label= "Modelo", max_length=40, widget = forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.ModelChoiceField(label= "Puerto", queryset= Port.objects.values_list('name', flat=True), widget= forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ["title","value","image","eslora","model","port"]

#forms.ModelChoiceField(queryset= Port.objects.values_list('name', flat=True),widget= 

def save(self, commit=True):
        post = super(FormularioRegistrarPublicacion, self).save(commit=False)
        post.title = self.cleaned_data['title']
        post.value = self.cleaned_data['value']
        post.image = self.cleaned_data['image']
        post.eslora = self.cleaned_data['eslora']
        post.model = self.cleaned_data['model']
        post.ship_type = self.cleaned_data['ship_type']
        post.port = self.cleaned_data['port']
        post.user = None
        if commit:
            post.save()
        return post


