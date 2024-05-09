from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField("Email", primary_key=True)
    password = models.CharField("Contraseña", max_length=20)
    name = models.CharField("Nombre", max_length=30)
    surname = models.CharField("Apellido", max_length=20)
    birthdate = models.DateField("Fecha de nacimiento")
    type_user = models.IntegerField("Tipo de usuario", default=0) # 0 es usuario normal
    phone_number = models.PositiveBigIntegerField("Número de teléfono")
    creation_date = models.DateField("Fecha de registro", auto_now_add=False)
    is_bloqued = models.BooleanField("Bloquear", default=False)
    request_verification = models.BooleanField("Solicita verificacion", default=False)
    ID_recuperation = models.IntegerField("Id de recuperacion")

class Port(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    location = models.CharField(max_length=30)

class Post(models.Model):
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
    #types_ships = models.TextChoices("Barco Motor", "Velero", "Yate", "Catamaran", "Semirigida", "Gomon", "Pesca paseo", "Lancha", "Goleta", "Bote", "Otros")
    image = models.ImageField()  # height_field=None, width_field=None,
    title = models.CharField("Titulo", max_length=30)
    value = models.DecimalField("Valor", max_digits=12, decimal_places=2) # Lo debe poner
    type_ship = models.CharField("Tipo de embarcación", choices= types_ships, max_length=11) # quizas va blank = True
    model = models.CharField("Modelo", max_length= 20)
    state = models.IntegerField(default = 0) # 0 --> disponible
    post_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(blank = True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    port = models.ForeignKey(Port, on_delete= models.CASCADE, null = False, blank= False)

class Offer(models.Model):
    image = models.ImageField()
    description = models.CharField("Descripción", max_length= 300)
    answer = models.IntegerField(blank = True, default= 0) # 0 --> sin respuesta, 1 --> rechazada, 2 --> aceptada ?
    date = models.DateField(auto_now_add= False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = False, blank= False)

class Comment(models.Model):  # Un comentario puede tener otro comentario
    content = models.CharField("Ingrese el mensaje", max_length= 300)
    date = models.DateField(auto_now_add= False)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null = False, blank= False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    answer = models.OneToOneField("self", on_delete= models.CASCADE, null = True, blank= True) # Como es una relación recursiva se pasa el propio objeto "self" y se pone null en True ya que no es obligatorio que un comentario tenga una respuesta

class Rating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1) # Porque el puntaje puede ser un numero entero, como por ejemplo 10, o un decimal, tipo 4,5 (No considero más decimales)
    user = models.OneToOneField(User, on_delete= models.CASCADE, null = False, blank= False) # Es de uno a uno, porque un usuario puede calificar una sola vez la página

class Conversation(models.Model): # Analizar y definir bien
    sender = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "sent_conversations")
    recipient = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "received_conversations")
    created_at = models.DateTimeField(auto_now_add= False)
    updated_at = models.DateTimeField(auto_now= False)

class Message(models.Model):
    content = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add= False)
    sender = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "sent_messages")
    recipient = models.ForeignKey(User, on_delete= models.CASCADE, null= False, blank= False, related_name= "received_messages")
    conversation = models.ForeignKey(Conversation, on_delete= models.CASCADE, null= False, blank= False)

class Notification(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = False, blank= False)
    offer = models.ForeignKey(Offer, on_delete= models.CASCADE, null= True, blank= True) # Es opcional esta relación
    post = models.ForeignKey(Post, on_delete= models.CASCADE, null= True, blank= True) # Es opcional esta relación
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, null= True, blank= True) # En el diagrama esta como que un comentario puede tener muchas notificaciones, pero para mi un comentario va a recibir solo una notificacion
    conversation = models.ForeignKey(Conversation, on_delete= models.CASCADE, null= True, blank= True) # Depende como lo implementemos puede ser muchos a uno o uno a uno







