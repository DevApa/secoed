
from django.db import models

class AprobacionCurso(models.Model):
    Nivel_CHOICES = (
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
        ('4', 'Nivel 4'),
    )

    semaforo_CHOICES = (
        ('1', 'Rojo'),
        ('2', 'Amarillo'),
        ('3', 'Verde'),
        ('4', 'Azul')
    )

    nivel = models.IntegerField(choices = Nivel_CHOICES)
    criterio = models.CharField(max_length = 200)
    semaforo = models.IntegerField(choices = semaforo_CHOICES)
    estado = models.BooleanField(default = True)

class Evaluation(models.Model):
    course = models.CharField(max_length=100)
    question = models.JSONField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
class CursoAsesores(models.Model):
    id_curso = models.IntegerField()
    id_asesor = models.IntegerField()
    estado = models.BooleanField(default = True)

