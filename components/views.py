from django.http.response import HttpResponse
from .models import Evaluation as EvaluationModel
from components.Evaluation import Evaluation
from components.utils import render_to_pdf
from conf.forms import MenuForm
from conf.models import Menu
from secoed.settings import EMAIL_HOST_USER
from typing import Any, Dict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.db.models import CharField, Value as V, F, Q
from django.db.models.functions import Concat
from components.models import  AprobacionCurso, CursoAsesores
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,FileResponse,HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
import io,json
from datetime import datetime
from django.core.mail import send_mail
from asesor.services import obtener_datos

from django.contrib.auth.decorators import login_required # login

from components.forms import CriterioForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

#Settings

from secoed.settings import TOKEN_MOODLE, API_BASE

# IMPORT
import datetime
from django.forms.models import fields_for_model, model_to_dict
import requests
from asesor.models import Asesor

###########################  Recursos para consumir la api###########################

apiBase = API_BASE

def wsfunction(function):
    return {
        "wstoken":TOKEN_MOODLE,
        "wsfunction":function,
        "moodlewsrestformat":"json",
    }

######################################################################################

##### filtrar asesor
def asesor(request, *args, **kwargs):                                                                                   
    #asesor = AsesorAsesor.objects.filter(Q(nombres__icontains =  kwargs["asesor"])|Q(apellidos__icontains = kwargs["asesor"])).distinct().values('id_asesor',nombre = Concat('nombres', V(' '),'apellidos'))
    ase = Asesor.objects.annotate(names = Concat('Nombres', V(' ') ,'Apellidos'))
    asesor = ase.filter(names__icontains = kwargs["asesor"] ).distinct().values('id_asesor',nombre = Concat('Nombres', V(' '),'Apellidos'))

    print(asesor)
    return JsonResponse({'data':list(asesor)})

#############Guardar asesor curso
@csrf_exempt
def guardarAsesorCurso(request, *args, **kwargs): 
    if(request.method == "POST"): 
        a = json.loads(request.body)
        ase = Asesor.objects.annotate(names = Concat('Nombres', V(' ') ,'Apellidos'))

        for i in ase:
            if (i.names == a['result'][2]):
                palabra = a['result'][2].split()
                # AsesorCursoAsesor.objects.create(relacion = palabra[0]+'_'+a['result'][1],asesor = i, curso = AsesorCursos.objects.get(id_curso = a['result'][0]))
                CursoAsesores.objects.create(id_curso = a['result'][0], id_asesor = i.id_asesor)
                return JsonResponse({"estado":"Se le asignó curso correctamente al asesor"},safe=False)
        return JsonResponse({"estado":"El asesor designado no existe, seleccione bien al asesor que desea asignar"},safe=False)

         
##################################
def buildEmail(course):
    subject = "Welcome to Skote  Membership"
    email_template_name = "components/email/email-notify.txt"
    email_text =  "jorge.penaz@ug.edu.ec" #"jucacero@hotmail.com"
    context = {
        "courseName" : course["fullname"]
    }
    template_email = render_to_string(email_template_name, context)
    # Array de destinatarios
    send_mail(subject, template_email, EMAIL_HOST_USER, [email_text], fail_silently=False)

@csrf_exempt
def getPDF(request):
    eva = Evaluation(request)
    eva.saveEvaluation()
    return render_to_pdf(eva.getLastEvaluationBD(), 'components/templates_pdf/evaluation_final.html')

def sendEmail(request):
    coursesList: Any = obtener_datos({
        "wsfunction": "core_course_get_courses",
    })
    finishCourses = []
    # courseSelected = [course for course in coursesList['courses'] if  course['id'] == courseId ]
    for course in coursesList:
        justNow = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        endDate = datetime.datetime.fromtimestamp(course['enddate'])
        if(justNow == endDate):
            # Send email
            buildEmail(course)
            finishCourses.append(course['fullname'])
    return JsonResponse({
        "finished_courses": finishCourses,
    })

def cursoA(request, *args, **kwargs):
    params = wsfunction("core_course_get_courses")
    response = requests.get(apiBase,params)
    
    curso = []
    for data in response.json():
        dat = CursoAsesores.objects.filter(id_curso = data['id'])
        if dat :
            print("nada")
        else :
            curso.append(data)

    datos = {"datas":curso}

    if kwargs["curso"] != "null":
        context = {"context":[p for p in datos["datas"] if kwargs['curso'].lower() in p['fullname'].lower()]}
    else:
        context = {"context":datos['datas']}
    return JsonResponse({'data':context})


#todos los cursos

def cursosTodos(request, *args, **kwargs):
    params = wsfunction("core_course_get_courses")
    response = requests.get(apiBase,params)
    
    curso = []
    for data in response.json():
        dat = CursoAsesores.objects.filter(id_curso = data['id'])
        if dat :
            print("nada")
        else :
            curso.append(data)

    datos = {"datas":curso}
    context = {"context":datos['datas']}
    return JsonResponse({'data':context})



##########################################################################################################################################
##########################################################################################################################################

def menu(request):
    menusview =  AprobacionCurso.objects.filter(estado =True).order_by('nivel')
    greeting = {'heading': "REQUISITO DEL CURSO", 'pageview': "Gestor", "menusview": menusview}
    return render(request, 'components/proyecto/components-formrequisito.html', greeting)

def requisito(request):
    if request.method == 'POST':
        ##editarField
        request.POST._mutable = True
        criterioForm = CriterioForm(request.POST)
        if criterioForm.is_valid():
            # criterioForm.save()
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.create(nivel = criterio_data.get("nivel"), criterio = criterio_data.get("criterio"), semaforo = criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se registro correctamente", "success")
        else:
            messages.error(request, "No se puedo registrar", "error")
        return redirect('requisito')
    else:
        menuFormView =CriterioForm()
        menu = AprobacionCurso()
        view = False
        context = {'menuFormView': menuFormView, 'requisito': menu, 'view': view}
    return render(request, 'components/proyecto/formrequisito.html', context)



# Editar los datos de un modulo por su pk
class UpdateRequisito(View):
    requisito = lambda self, id : get_object_or_404(AprobacionCurso, pk = id) 
    def post(self, request, *args,  **kwargs):
        criterioForm = CriterioForm(request.POST, model_to_dict(self.requisito(kwargs["pk"])))
        if criterioForm.is_valid():
            criterio_data = criterioForm.cleaned_data
            AprobacionCurso.objects.filter(id = kwargs["pk"]).update(nivel = criterio_data.get("nivel"), criterio = criterio_data.get("criterio"), semaforo = criterio_data.get("semaforo"))
            criterio = criterio_data.get("criterio")
            messages.success(request, "Se edito correctamente", "success")
            return redirect('requisito')
    def get(self, request, *args,  **kwargs):      
        menuFormView = CriterioForm(model_to_dict(self.requisito(kwargs["pk"])))
        view = False
        context = {'menuFormView': menuFormView, 'menu': self.requisito(kwargs["pk"]), 'view': view}
        return render(request, 'components/proyecto/formrequisito.html', context)

def deleteRequisito(request, pk):
    requisito = get_object_or_404(AprobacionCurso, pk=pk)
    if requisito:
        requisito.delete()
        messages.success(request, "Se ha eliminado correctamente", "success")
    return redirect('requisito')


def deleteAsignacion(request, pk):
    deleteA = get_object_or_404(CursoAsesores, pk=pk)
    if deleteA:
        deleteA.delete()
        messages.success(request, "Se ha eliminado correctamente", "success")
    return redirect('forms-asesor')



# AJAX
@login_required
def loadRequisito(request):
    #modulo_id = request.GET.get('modulo_id')
    modulo_id = request.GET.get('id')
    menus = Menu.objects.filter(Q(modulo_id=modulo_id) & Q(href='')).order_by('descripcion')
    return render(request, 'components/proyecto/requisitoList.html', {'menus': menus})


################################################################



class FormEducacion(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Designar asesor curso"
        greeting['pageview'] = "Forms"

        queryset = request.GET.get("buscar")
        
        if queryset:
            greeting['asesor'] = AsesorAsesor.objects.filter(Q(nombres__icontains = queryset)|Q(apellidos__icontains = queryset)).distinct()
            greeting['curso'] = AsesorCursoAsesor.objects.filter
    
        return render (request,'components/proyecto/components-formeducation.html',greeting)

####################Vista de asesores que ya se encuentran asignados

class FormAsesor(View):
    def get(self, request):        
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase,params)
        datos = []
        if response.json():
            for data in response.json():
                curs = CursoAsesores.objects.filter(id_curso = data['id']).values('id','id_asesor')
                if curs:                    
                    a = Asesor.objects.filter(id_asesor = curs[0]['id_asesor']) .values(names = Concat('Nombres', V(' ') ,'Apellidos'))
                    context = {"id":curs[0]['id'],"curso":data["fullname"], "asesor":a[0]["names"]}
                    datos.append(context)
        greeting = {}
        greeting['heading'] = "Curso Designado a Asesor"
        greeting['pageview'] = "Forms"
        if datos:
            greeting['cursos'] = datos        

        return render (request,'components/proyecto/components-formasesor.html',greeting)


class FormEducaciona(View):
    @csrf_exempt
    def get(self, request):        
        params = wsfunction("core_course_get_courses")
        response = requests.get(apiBase,params)
        greeting = {}
        greeting['heading'] = "Avance del curso"
        greeting['pageview'] = "Forms"
        if response:
            greeting['cursos'] = response.json()
        
        return render (request,'components/proyecto/components-formeducation1.html',greeting)

  


class listadoAsesores(View):        
    def get(self, request):
        params = wsfunction("core_enrol_get_enrolled_users")
        params.update(courseid = request.GET.get('id'))
        response = requests.get(apiBase,params)

        greeting = {"heading":"Listado de Docentes","pageview":"Forms", "curso": request.GET.get('id')}
        if response:
            datos = [rol for rol in response.json() if rol.get('roles') and rol['roles'][0]['roleid'] == 5]

            if datos: 
                greeting.update(context = datos)
                if greeting.get("context"):
                    for fecha in greeting["context"]:
                        fecha.update(lastaccess = datetime.datetime.fromtimestamp(fecha['lastaccess']))   

        return render (request,'components/proyecto/components-listadoAsesores.html', greeting)




class actividades(View):        
    def get(self, request):
        params = wsfunction("gradereport_user_get_grade_items")
        params.update(courseid = request.GET.get('curso'))
        response = requests.get(apiBase,params)
        

        if response.json().get("usergrades"):
            actividad = [actividades for actividades in response.json()["usergrades"] if actividades["userid"] == int(request.GET.get('id'))]
            print(actividad)
        else:
            actividad = None


 
        greeting = {"heading":"Listado de Actividades", "pageview":"Forms"}

        if actividad:
            actividades = [dato for dato in actividad[0]["gradeitems"]]
        
            cont = 0
            suma = 0
            nota = 0
            if actividades:
                greeting.update(context = actividades)
                for i in actividades:
                    if i["graderaw"]:
                        nota = (i["graderaw"]*100)/i["grademax"]
                        suma = nota + suma
                        cont = cont + 1                

                if suma == 0:
                    semaforo = 0
                else:
                    semaforo = suma / cont

                    greeting.update(semaforo = self.semaforo(semaforo))       

        return render (request,'components/proyecto/modalActividades.html', greeting)
    
        
    def semaforo(self, semaforo):
        # metodo lambda sirver para obtener los criterios de acuerdo a los niveles
        criterio = lambda level : AprobacionCurso.objects.filter(nivel = level) if AprobacionCurso.objects.filter(nivel = level) else None
        #condiciones de acuerdo a los niveles de semàforo
        criterios = criterio(1) if semaforo < 30 else criterio(2) if semaforo < 70  else criterio(3) if semaforo < 90  else criterio(4)
        return criterios




class FormRequisito(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Requisito del curso"
        greeting['pageview'] = "Forms"
        coursesList: Any = obtener_datos({
            "wsfunction": "core_course_get_courses",
        })
        return render (request,'components/proyecto/components-formrequisito.html',greeting)



class FormEvaluation(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Evaluation Docente"
        greeting['pageview'] = "Evaluación"
        coursesList: Any = obtener_datos({
            "wsfunction": "core_course_get_courses",
        })
        #greeting['curso'] = AsesorCursoAsesor.objects.filter(~Q(curso = AsesorCursos.objects.all() )).values('curso__id_curso','curso__tipo')
    
        return render (request,'components/proyecto/components-formevaluation.html',{
            "greeting": greeting,
            "courses": [course['shortname'] for course in coursesList]
            })

def historialEvaluations(request):
    evaluations = EvaluationModel.objects.all()
        
    return render(request, 'components/proyecto/components-historial_eva.html', {
        "heading": "HIstorial de Evaluaciones",
        'pageview': "Evaluación",
        'evaluations': evaluations,
    })
def historialEvaluation(request, id):
    evaluation = EvaluationModel.objects.get(pk=id)
    return render_to_pdf({"course": evaluation.course, "questions": evaluation.question}, 'components/templates_pdf/evaluation_final.html')





