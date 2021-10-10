from django.db import models
from conf.models import Carrera
from django.urls import reverse


# 4
class Nivel_Académico(models.Model):
    id_academico=models.AutoField(primary_key=True)
    Nivel=models.CharField(max_length=60)
    Detalle=models.CharField(max_length=60)

    def __str__(self):
        return self.Nivel

# 5
class Cursos(models.Model):
    Id_curso=models.AutoField(primary_key=True)
    Tipo=models.CharField(max_length=200)
    Estado=models.CharField(max_length=200)
    Fecha_de_Apertura=models.DateTimeField()
    Fecha_fin=models.DateTimeField()
    Carrera=models.ForeignKey(Carrera, on_delete=models.CASCADE,max_length=200,db_column='id')

    def __str__(self):
        return self.Tipo
# 6
class Asesor(models.Model):
    id_asesor=models.AutoField(primary_key=True)
    Nombres=models.CharField(max_length=200)
    Apellidos=models.CharField(max_length=200)
    Titulo=models.ForeignKey('titulos', on_delete=models.CASCADE, max_length=10)
    Nivel_Académico=models.ForeignKey('nivel_académico', on_delete=models.CASCADE, max_length=10)
    Correo=models.EmailField(max_length=25)    
    Carrera=models.ForeignKey(Carrera, on_delete=models.CASCADE,max_length=200,db_column='id')

    def __str__(self):
        return self.Nombres
    
# 7
class Docentes(models.Model):
    id_docentes=models.AutoField(primary_key=True)
    Nombres=models.CharField(max_length=200)
    Apellidos=models.CharField(max_length=200)
    Titulo=models.ForeignKey('titulos', on_delete=models.CASCADE, max_length=10)
    Nivel_Académico=models.ForeignKey('nivel_académico', on_delete=models.CASCADE, max_length=10)
    Correo=models.EmailField(max_length=30)
    Curso=models.ForeignKey('Cursos', on_delete=models.CASCADE)   
    Carrera=models.ForeignKey(Carrera, on_delete=models.CASCADE,max_length=200,db_column='id')

    def __str__(self):
        return self.Nombres
    
# 8
class Periodo(models.Model):
    id_periodo=models.AutoField(primary_key=True)
    Tipo=models.CharField(max_length=25)

    def __str__(self):
        return self.Tipo
    
# 9
class Recursos(models.Model):
    id_recursos=models.AutoField(primary_key=True)
    Tiempo=models.CharField(max_length=200)    

    def __str__(self):
        return self.Tiempo

#parametrización.

# 10
class Curso_Asesor(models.Model):
    id_curso_asesor=models.AutoField(primary_key=True)
    Asesor=models.ForeignKey('asesor', on_delete=models.CASCADE,max_length=200)
    Curso=models.ForeignKey('Cursos', on_delete=models.CASCADE,max_length=200)
    Relacion=models.CharField(max_length=200)
    Estudiante=models.ManyToManyField('Docentes',blank=True, help_text="Ctrl para elegir varios Servicios")

    def __str__(self):
        return self.Relacion



# 11
class Cabecera_Crono(models.Model):
    estado_cabecera = [
    (1, 'Pendiente'),
    (2, 'Aprobado')
    ]
    Id_Cabecera_Crono=models.AutoField(primary_key=True)
    Periodo=models.ForeignKey('Periodo', on_delete=models.CASCADE,max_length=200)
    Tiempo=models.ForeignKey('Recursos', on_delete=models.CASCADE,max_length=200)
    Relación=models.ForeignKey('Curso_Asesor', on_delete=models.CASCADE,max_length=20, null=True)
    Nombre=models.CharField(max_length=200)   
    Dia_Creación=models.DateTimeField(auto_now_add=True) 
    Estado=models.IntegerField(null=True, blank=False, choices=estado_cabecera, default=1)

    def __str__(self):
        return self.Nombre



# 12
class Titulos(models.Model):
    id_titulo=models.AutoField(primary_key=True)
    Nombramiento=models.CharField(max_length=25)    
    Carrera=models.ForeignKey(Carrera, on_delete=models.CASCADE,max_length=200)
    
    def __str__(self):
        return self.Nombramiento


#13
class Event(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey('Cabecera_Crono', on_delete=models.CASCADE, max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
           
    def get_absolute_url(self):
        return reverse('event-detail', args=(self.id,))
    
    @property
    def get_html_url(self):        
        url = reverse('event-detail', args=(self.id,))                
        p="'"+url+"'"        
        return f'<button type="button" class="btn btn-link btn-sm" onclick="abrir_Uni_edi({p})"> {self.title} </button>'  
#14
class Observaciones(models.Model):
    id_ob=models.AutoField(primary_key=True)
    Nombre_Cabecera = models.ForeignKey('Cabecera_Crono', on_delete=models.CASCADE,max_length=200)    
    Observaciones=models.TextField()            
    
    def __str__(self):
        return str(self.Nombre_Cabecera)

#15
class registro_historicos(models.Model):    
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey('Cabecera_Crono', on_delete=models.CASCADE, max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title