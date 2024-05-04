from django.db import models

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    tipo_usuario = models.IntegerField(default=0) # 0 es usuario normal
    telefono = models.PositiveBigIntegerField()
    fecha_creacion = models.DateField(auto_now_add=False)
    esta_bloqueado = models.BooleanField(default=False)
    solicita_verificacion = models.BooleanField(default=False)
    ID_recuperacion = models.IntegerField()

class Publicacion(models.Model):
    tipos_de_embarcaciones = models.TextChoices("Barco Motor", "Velero", "Yate", "Catamaran", "Semirigida", "Gomon", "Pesca paseo", "Lancha", "Goleta", "Bote", "Otros")
    puertos = models.TextChoices("Puerto 1", "Puerto 2", "Puerto 3", "Puerto 4")
    imagen = models.ImageField()  # height_field=None, width_field=None,
    titulo = models.CharField(max_length=30)
    valor = models.DecimalField(max_digits=12, decimal_places=2) # Lo debe poner
    tipo = models.CharField(choices= tipos_de_embarcaciones) # quizas va blank = True
    puerto = models.CharField(choices= puertos)
    modelo = models.CharField(max_length= 20)
    estado = models.IntegerField(default = 0) # 0 --> disponible
    fecha_publicacion = models.DateField(auto_now_add=False)
    fecha_finalizacion = models.DateField(blank = True, auto_now_add=False)
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, null = False, blank= False)

class Oferta(models.Model):
    imagen = models.ImageField()
    descripcion = models.CharField(max_length= 300)
    respuesta = models.IntegerField(blank = True, default= 0) # 0 --> sin respuesta, 1 --> rechazada, 2 --> aceptada ?
    fecha = models.DateField(auto_now_add= False)
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, null = False, blank= False)
    publicacion = models.ForeignKey(Publicacion, on_delete= models.CASCADE, null = False, blank= False)

class Comentario(models.Model):  # Un comentario puede tener otro comentario
    contenido = models.CharField(max_length= 300)
    fecha = models.DateField(auto_now_add= False)
    publicacion = models.ForeignKey(Publicacion, on_delete= models.CASCADE, null = False, blank= False)
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, null = False, blank= False)
    respuesta = models.OneToOneField("self", on_delete= models.CASCADE, null = True, blank= True) # Como es una relación recursiva se pasa el propio objeto "self" y se pone null en True ya que no es obligatorio que un comentario tenga una respuesta


class Calificacion(models.Model):
    puntaje = models.DecimalField(max_digits=2, decimal_places=1) # Porque el puntaje puede ser un numero entero, como por ejemplo 10, o un decimal, tipo 4,5 (No considero más decimales)
    usuario = models.OneToOneField(Usuario, null = False, blank= False) # Es de uno a uno, porque un usuario puede calificar una sola vez la página

class Conversacion(models.Model): # Analizar y definir bien
    contenido = models.CharField(max_length= 500) # Hay que definir si vamos a guardar cada comentario con su respesctivos usuarios, o vamos a agregar toda la conversación en contenido


class Notificacion(models.Model):
    contenido = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=False)
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, null = False, blank= False)
    oferta = models.ForeignKey(Oferta, on_delete= models.CASCADE, null= True, blank= True) # Es opcional esta relación
    publicacion = models.ForeignKey(Publicacion, on_delete= models.CASCADE, null= True, blank= True) # Es opcional esta relación
    comentario = models.ForeignKey(Comentario, on_delete= models.CASCADE, null= True, blank= True) # En el diagrama esta como que un comentario puede tener muchas notificaciones, pero para mi un comentario va a recibir solo una notificacion
    conversacion = models.ForeignKey(Conversacion, on_delete= models.CASCADE, null= True, blank= True) # Depende como lo implementemos puede ser muchos a uno o uno a uno







