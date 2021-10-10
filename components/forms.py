from django.forms import ModelForm, TextInput, Select, ModelChoiceField
from conf.models import Modulo, Menu, Icono
from django import forms

ICONOS = Icono.objects.order_by('descripcion')
MODULOS = Modulo.objects.order_by('descripcion')


class CriterioForm(forms.Form):
    Nivel_CHOICES = (
         ('1','Nivel 1'),
         ('2','Nivel 2'),
         ('3', 'Nivel 3'),
         ('4', 'Nivel 4')
     )

    semaforo_CHOICES = (
        ('1', 'Rojo'),
        ('2', 'Amarillo'),
        ('3', 'Verde'),
        ('4', 'Azul')
    )

    # id = forms.IntegerField(required = False)
    nivel = forms.ChoiceField(choices=Nivel_CHOICES)
    criterio = forms.CharField(label='Criterio', max_length=200)
    semaforo = forms.ChoiceField(choices=semaforo_CHOICES)
