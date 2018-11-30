from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
#
class Noticia (models.Model) :
    emcabezado = models.CharField(max_length=50)
    cuerpo = models.CharField(max_length=100)
    id_user = models.ForeignKey( User , models.SET_NULL,
    blank=True,
    null=True,)
    fecha = models.DateField(auto_now=True)
    imagen = models.CharField(max_length=250, blank=True)
    imagenUrl = models.TextField(blank=True)

    def __str__(self):
        return str(self.emcabezado)


class Image(models.Model):
    img = models.ImageField(upload_to='uploads/{0}'.format("%d-%m-%y/%H_%M_%S"), default='static/f1.png')

    def __str__(self):
        return str(self.img)


class Aspirante (models.Model) :
    id_aspirante = models.AutoField(primary_key=True)
    nombreuser_aspirante = models.CharField(max_length=10, unique=True, blank=True, null=True)
    nombre_aspirante = models.CharField(max_length=20)
    apellido_aspirante = models.CharField(max_length=20)
    contrasena_aspirante = models.CharField(max_length=256)
    dui = models.CharField(max_length=9)
    genero = models.CharField(max_length=9)
    fechas_nac = models.DateField()
    t_fijo = models.CharField(max_length=10)
    t_movil = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    titulo_pre = models.CharField(max_length=30)
    institucion = models.CharField(max_length=30)
    f_expedicion = models.DateField()
    municipio = models.CharField(max_length=50)
    lugar_trab = models.CharField(max_length=50)
    programa = models.CharField(max_length=50)
    aceptado = models.BooleanField(blank=True, default=False)
    id_user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, )
    id_val = models.ForeignKey('validacion', models.SET_NULL, blank=True, null=True, )

    def __str__(self):
                return str(self.nombre_aspirante)

class Docente(models.Model) :
    id_docente = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=15,unique=True, blank=True, null=True,)
    password = models.CharField(max_length=10)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dui = models.CharField(max_length=10)
    genero = models.CharField(max_length=15)
    fecha_naci = models.DateField()
    telefono = models.CharField(max_length=15, blank=True, null=True,)
    movil = models.CharField(max_length=15, blank=True, null=True,)
    email = models.CharField(max_length=35)
    formacion = models.CharField(max_length=200, blank=True)
    titulo =models.CharField(max_length=200, blank=True, null=True,)

    def __str__(self):
        return (self.nombre,self.apellido)

class Validacion (models.Model):
    id_codigo=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=250)
    vigencia= models.DateField()
    activo= models.BooleanField(default=True)
    impreso= models.BooleanField(default=False)

    def __str__(self):
                return str(self.codigo)

class Procedimiento(models.Model):
    id_procedimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return(self.nombre)

class Pasos(models.Model):
    id_paso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    id_proceimiento = models.ForeignKey('Procedimiento', models.SET_NULL, blank=True, null=True,)
    orden = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return(self.nombre)

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True)
    id_user_para = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, )
    id_user_con = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='user2')
    titulo=models.CharField(max_length=150)
    descripcion=models.CharField(max_length=1024)
    fecha_hora_inicio=models.DateTimeField()
    fecha_hora_fin=models.DateTimeField()
    lugar=models.CharField(max_length=150,blank=True,)
    nombre_para=models.CharField(max_length=150,blank=True,)
    nombre_con=models.CharField(max_length=150,blank=True,)
    cancelado=models.BooleanField()
    dia_completo=models.BooleanField()

    def __str__(self):
        return self.titulo

class Programa(models.Model):
    id_programa=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=10)
    nombre=models.CharField(max_length=150)
    descripcion=models.CharField(max_length=1024, blank=True, null=True)
    totalUV=models.IntegerField()
    plan_estudio=models.IntegerField()
    duracion_ciclo=models.IntegerField()
    duracion_anio=models.IntegerField()
    titulo=models.CharField(max_length=100)
    total_asignaturas=models.IntegerField()
    nota_minima=models.DecimalField(max_digits=4,decimal_places=2)
    cum_minimo=models.DecimalField(max_digits=4,decimal_places=2)
    caracteristicas=models.CharField(max_length=1024, blank=True, null=True)
    activo=models.BooleanField(blank=True)
    
    def __str__(self):
        return self.codigo

class ciclo (models.Model):
    id_ciclo=models.AutoField(primary_key=True)
    numero=models.IntegerField()
    anio=models.IntegerField()
    activo=models.BooleanField(blank=True)

    def __str__(self):
        return (str(self.id_ciclo))

class Materia(models.Model):
    id_materia=models.AutoField(primary_key=True)
    id_materia_pre= models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    id_ciclo= models.ForeignKey(ciclo, models.SET_NULL, blank=True, null=True)
    codigo=models.CharField(max_length=10)
    nombre=models.CharField(max_length=150)
    correlativo=models.IntegerField()
    unidad_valorativa=models.IntegerField()
    activo=models.BooleanField(blank=True)

    def __str__(self):
        return (self.codigo)

class aula(models.Model):
    id_aula=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=10)
    ubicacion=models.CharField(max_length=100, blank=True, null=True)
    activo=models.BooleanField(blank=True)

    def __str__(self):
        return(self.codigo)    

class horario(models.Model):
    id_horario=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=10, blank=True, null=True)
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()
    activo=models.BooleanField(blank=True)