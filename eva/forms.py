from django.forms import *

from conf.models import Rol, RolMoodle
from eva.models import *


class DocenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Seleccione un usuario '
        self.fields['user'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'identificacion', 'roles', 'rol_moodle', 'moodle_user']

        labels = {
            'user': 'Usuario',
            'title': 'Titulo',
            'type_contract': 'Tipo de Contrato',
            'dedication': 'Dedicación',
            'position': 'Cargo',
            'is_evaluator': 'Es Evaluador'
        }

        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo Profesional'}),
            'type_contract': Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Contrato'}),
            'dedication': Select(attrs={'class': 'form-control', 'placeholder': 'Tiempo de dedicación'}),
            'position': Select(attrs={'class': 'form-control', 'placeholder': 'Cargo del docente'}),
            'is_evaluator': CheckboxInput(attrs={'class': 'form-check-radio'})
        }


class MateriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rol = Rol.objects.filter(descripcion='Docente').first()
        self.fields['teacher'].empty_label = 'Seleccione un docente'
        self.fields['teacher'].queryset = Usuario.objects.filter(roles=rol.id, rol_moodle__codigo__gte=5)
        self.fields['area'].empty_label = 'Seleccione una área de conocimiento'
        self.fields['area'].widget.attrs['autofocus'] = True

    class Meta:
        model = Materia
        fields = ['area', 'teacher', 'name']

        labels = {
            'area': 'Área',
            'teacher': 'Docente',
            'name': 'Nombre Materia',
        }

        widgets = {
            'area': Select(attrs={'class': 'form-select select2-templating'}),
            'teacher': Select(attrs={'class': 'form-select select2-templating'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CicloForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ciclo
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del ciclo ejemplo: C1-2021'}),
            'ciclo_activo': CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoria'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TipoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tipo
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Defina aquí el tipo'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PreguntaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pregunta
        fields = '__all__'

        labels = {
            'category': 'Categoria',
            'title': 'Título',
            'description': 'Descripción',
            'type': 'Tipo'
        }

        widgets = {
            'category': Select(attrs={'class': 'form-select'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Aquí un título para la pregunta'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la pregunta'}),
            'type': Select(attrs={'class': 'form-control select2'})
        }


class AreasConocimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        co_evaluators = []
        super().__init__(*args, **kwargs)
        rol = Rol.objects.filter(descripcion='Coevaluador').first()
        rol_ml = RolMoodle.objects.filter(descripcion='Docentes').first()
        self.fields['docente'].queryset = Usuario.objects.filter(roles=rol.id, rol_moodle__codigo__gte=rol_ml.codigo)
        self.fields['career'].empty_label = 'Seleccione una carrera'
        self.fields['docente'].empty_label = 'Seleccione una docente'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = AreasConocimiento
        fields = '__all__'

        labels = {'name': 'Nombre', 'career': 'Carrera', 'docente': 'Docente', 'materia': 'Materia'}

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Aquí nombre del área de conocimiento'}),
            'career': Select(attrs={'class': 'form-select select2'}),
            'docente': Select(attrs={'class': 'form-select select2'}),
        }

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class ParametroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Parametro
        fields = '__all__'

        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del parámetro'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ParametrosGeneralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parameter'].empty_label = 'Seleccione un parámetro'
        self.fields['parameter'].widget.attrs['autofocus'] = True

    class Meta:
        model = ParametrosGeneral
        fields = '__all__'

        labels = {
            'parameter': 'Parámetro',
            'code': 'Código',
            'value': 'Valor',
        }

        widgets = {
            'parameter': Select(attrs={'class': 'form-select'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del parámetro'}),
            'value': NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RespuestaForm(ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'


class CoevaluacionForm(ModelForm):
    class Meta:
        model = Pregunta
        fields = ['id']


class AutoEvaluacionForm(ModelForm):
    class Meta:
        model = Pregunta
        fields = ['id']


class ResultadoProcesoForm(ModelForm):
    class Meta:
        model = ResultadoProceso
        fields = ['coevaluator', 'coe_result_Tic', 'coe_result_Did', 'coe_result_Ped', 'Total_Proceso_Coe', 'Total_Proceso']