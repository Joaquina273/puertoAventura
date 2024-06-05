from django.db import models
from django.utils import timezone
import os
# Create your models here.
class User(models.Model):
    
    types_users = {
        0 : "Usuario normal",
        1 : "Usuario con permisos para publicar",   # Creo que es mejor implementarlo de esta manera
        2 : "Personal",
        3 : "Administrador"
    }
    email = models.EmailField("Email", primary_key=True)
    password = models.CharField("Contraseña", max_length=20)
    name = models.CharField("Nombre", max_length=30)
    surname = models.CharField("Apellido", max_length=20)
    avatar = models.ImageField("Avatar", upload_to='avatares/', blank=True, null=True)
    birthdate = models.DateField("Fecha de nacimiento")
    type_user = models.IntegerField("Tipo de usuario", default=0) # 0 es usuario normal
    phone_number = models.PositiveBigIntegerField("Número de teléfono")
    creation_date = models.DateField("Fecha de registro", auto_now_add=timezone.now)
    is_blocked = models.BooleanField("Bloquear", default=False)
    verification_requested = models.BooleanField("Solicita verificacion", default=False)
    recovery_ID = models.IntegerField("Id de recuperacion",blank=True,null=True)
    tries_left = models.IntegerField("Intentos restantes",default=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Port(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    location = models.CharField(max_length=30)

    class Meta:
        db_table = 'ports'
        verbose_name = 'Puerto'
        verbose_name_plural = 'Puertos'

    def __str__(self) :
        return self.name
    
class Post(models.Model):
      
    def get_image_upload_path(instance, filename):
        return os.path.join('publicaciones', instance.patent, filename)
    
    types_ships = {
        "Barco Motor" : "Barco Motor",
        "Velero" : "Velero",
        "Yate" : "Yate",
        "Catamaran" : "Catamaran",
        "Semirigida" : "Semirigida",
        "Gomon" : "Gomon",
        "Pesca paseo" : "Pesca paseo",
        "Lancha" : "Lancha",
        "Goleta" : "Goleta",
        "Bote" : "Bote",
        "Otro" : "Otro",
    }
    patent = models.CharField(max_length=20, unique=True)
    eslora = models.DecimalField(decimal_places=3, max_digits=12)
    patent = models.CharField(max_length=100)
    image = models.ImageField("Imagen", upload_to=get_image_upload_path) # height_field=None, width_field=None,
    title = models.CharField("Titulo", max_length=30)
    value = models.DecimalField("Valor", max_digits=12, decimal_places=2) # Lo debe poner
    ship_type = models.CharField("Tipo de embarcación", choices= types_ships, max_length=11) # quizas va blank = True
    model = models.CharField("Modelo", max_length= 20)
    state = models.IntegerField(default = 0, verbose_name="Estado") # 0 --> disponible
    post_date = models.DateField(auto_now_add=timezone.now, verbose_name="Fecha de publicacion")
    end_date = models.DateField(blank = True, null=True, verbose_name="Fecha de finalizacion")
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    port = models.ForeignKey(Port, on_delete= models.CASCADE, null = False, blank= False,verbose_name="Puerto")
    saved_by = models.ManyToManyField(User, related_name='saved_posts')


    class Meta:
        db_table = 'posts'
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
    
    def __str__(self) :
        return self.title
  
    def get_comments(self):
        return self.comments.filter(parent_id__isnull=True) 

class Offer(models.Model):

    def get_image_upload_path(instance, filename):
        return os.path.join('ofertas', instance.user.email, instance.post.patent, filename)
    
    title = models.CharField("Titulo", max_length=30)
    image = models.ImageField("Imagen", upload_to=get_image_upload_path)  # heig
    description = models.CharField("Descripción", max_length= 300)
    answer = models.IntegerField(blank = True, default= 0) # 0 --> sin respuesta, 1 --> rechazada, 2 --> aceptada ?
    date = models.DateField(auto_now_add=timezone.now, verbose_name="Fecha de publicacion")
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = False, blank= False)

    class Meta:
        db_table = 'offers'
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
    

class Comment(models.Model):  # Un comentario puede tener otro comentario
    content = models.TextField("Ingrese el mensaje", max_length= 300) 
    date = models.DateField(auto_now_add=timezone.now)
    post = models.ForeignKey(Post, related_name="comments", on_delete= models.CASCADE, null = False, blank= False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    parent = models.OneToOneField("self", on_delete= models.CASCADE, related_name='answer', null = True, blank= True) # Como es una relación recursiva se pasa el propio objeto "self" y se pone null en True ya que no es obligatorio que un comentario tenga una respuesta

    def __str__(self):
        return '%s - %s' %(self.post.title, self.user.name)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

class Rating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1) # Porque el puntaje puede ser un numero entero, como por ejemplo 10, o un decimal, tipo 4,5 (No considero más decimales)
    user = models.OneToOneField(User, on_delete= models.CASCADE, null = False, blank= False) # Es de uno a uno, porque un usuario puede calificar una sola vez la página

    class Meta:
        db_table = 'rating'
        verbose_name = 'Calificacion'
        verbose_name_plural = 'Calificaciones'

class Conversation(models.Model): # Analizar y definir bien
    sender = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "sent_conversations")
    recipient = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "received_conversations")
    created_at = models.DateTimeField(auto_now_add= timezone.now, verbose_name="Fecha de creacion")
    updated_at = models.DateTimeField(auto_now= timezone.now, verbose_name= "Fecha de actualizacion")

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversacion'
        verbose_name_plural = 'Conversaciones'

class Message(models.Model):
    content = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add= False)
    sender = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "sent_messages")
    recipient = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "received_messages")
    conversation = models.ForeignKey(Conversation, on_delete= models.CASCADE, null= False, blank= False)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False, related_name='notifications')
    read = models.BooleanField("Leída",default=False)
    link = models.CharField(max_length=50)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'






