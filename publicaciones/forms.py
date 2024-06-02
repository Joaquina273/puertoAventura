from django import forms
from db.models import Port,Post, Comment, User

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
    
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
            'class': "form-control", 
            'id': "textAreaExample",
            'style': "background: #fff;",
            'rows': '4'
            }))
    
    class Meta: 
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.pop('post_id', None)
        self.request = kwargs.pop('request', None)
        self.parent_id = kwargs.pop('parent_id', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.content = self.cleaned_data['content']
        if(self.parent_id):
            comment.parent = Comment.objects.get(id=self.parent_id)
        comment.post = Post.objects.get(id=self.post_id)
        comment.user = User.objects.get(email=self.request.session.get('usuario') [0])
        if commit:
            comment.save()
        return comment