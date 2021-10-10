
from django import forms
from .models import Nivel_Académico, Cursos, Asesor, Docentes, Periodo, Recursos, Curso_Asesor, Cabecera_Crono, Titulos, Event, Observaciones, registro_historicos
from django.forms import ModelForm, DateInput


#5
class Nivel_AcadémicoForm(forms.ModelForm):

    class Meta:
        model = Nivel_Académico
        fields = '__all__'   
#6
class curso_FechaForm(ModelForm):
  class Meta:
    model = Cursos
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'Fecha_de_Apertura': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'Fecha_fin': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = []

  def __init__(self, *args, **kwargs):
    super(curso_FechaForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['Fecha_de_Apertura'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['Fecha_fin'].input_formats = ('%Y-%m-%dT%H:%M',)

#8
class CursosForm(forms.ModelForm):

    class Meta:
        model = Cursos
        fields = 'Tipo','Estado','Fecha_de_Apertura','Fecha_fin','Carrera',
        
#9
class AsesorForm(forms.ModelForm):

    class Meta:
        model = Asesor
        fields = '__all__'   
#10
class DocentesForm(forms.ModelForm):

    class Meta:
        model = Docentes
        fields = '__all__'   
#11
class PeriodoForm(forms.ModelForm):

    class Meta:
        model = Periodo
        fields = '__all__'   
#12
class RecursosForm(forms.ModelForm):

    class Meta:
        model = Recursos
        fields = '__all__'  
#13
class Curso_AsesorForm(forms.ModelForm):

    class Meta:
        model = Curso_Asesor
        fields = '__all__'   

#14
class TitulosForm(forms.ModelForm):

    class Meta:
        model = Titulos
        fields = '__all__'


#Cronograma
#15
class Cabecera_CronoForm(forms.ModelForm):

    class Meta:
        model = Cabecera_Crono
        fields = '__all__'
#16
class EventForm(ModelForm):
  class Meta:    
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = []

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


#17
class Cabecera_Crono_ObForm(forms.ModelForm):

    class Meta:
        model = Observaciones
        fields = '__all__'

#18
class historiasForm(ModelForm):
  class Meta:
    model = registro_historicos
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = []

  def __init__(self, *args, **kwargs):
    super(historiasForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)