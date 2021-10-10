from builtins import print

import delorean
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from django.utils.datetime_safe import datetime
# Create your views here.
from django.views import View

from secoed.settings import TOKEN_MOODLE, API_BASE


class CursoView(View):

    def categoria(request):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        try:
            response = requests.post(API_BASE, params)
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCategorias.html', context={"context": "Bad request"})
            if response:
                r = response.json()
                context = {"context": r}
        except Exception as e:
            print(e)
        return render(request, 'cursos/mantenimientoCategorias.html', context)

    def createEditCategoria(request):
        texto = ""
        if (request.POST['id'] == ""):
            print(" wntro al insertar 1")
            wsfunction = "core_course_create_categories";
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "categories[0][name]": request.POST["name"],
                      "categories[0][parent]": request.POST["depth"],
                      "categories[0][description]": request.POST['description'],
                      "categories[0][descriptionformat]": 1,
                      "categories[0][idnumber]": texto
                      }
        else:
            wsfunction = "core_course_update_categories"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "categories[0][id]": request.POST['id'],
                      "categories[0][name]": request.POST["name"],
                      "categories[0][parent]": request.POST["depth"],
                      "categories[0][description]": request.POST['description'],
                      "categories[0][descriptionformat]": 1,
                      "categories[0][idnumber]": texto
                      }
        try:
            response = requests.post(API_BASE, params)
            if response:
                r = response.json()
                if response == 400:
                    print(r.message)
                if response == 500:
                    print(r.message)
                if response == 200:
                    print(r.message)
        except Exception as e:
            print(e)
        return redirect('categoria')

    def deleteCategoria(request, idCategoria):
        params = {
            "wstoken": TOKEN_MOODLE,
            "wsfunction": "core_course_delete_categories",
            "moodlewsrestformat": "json",
            "categories[0][id]": idCategoria,
            "categories[0][recursive]": 1
        }
        try:
            respuesta = requests.post(API_BASE, params)
            if respuesta:
                r = respuesta.json()
                if respuesta.status_code == 400:
                    print(r.message)
                else:
                    print("si se borro")
        except Exception as e:
            print(e)
        return redirect('categoria')

    def get(self, request):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_courses_by_field ",
                  "moodlewsrestformat": "json",
                  }
        cursos = {}
        try:
            response = requests.post(API_BASE, params)
            if response.status_code == 400:
                return render(request, 'cursos/mantenimientoCursos.html', context={"context": "Bad request"})
            if response:
                cursos = {"cursos": response.json()}
        except Exception as e:
            print(e)
        return render(request, 'cursos/mantenimientoCursos.html', cursos)

    def allCategorias(request):
        params = {"wstoken": TOKEN_MOODLE,
                  "wsfunction": "core_course_get_categories",
                  "moodlewsrestformat": "json",
                  }
        context = {}
        try:
            response = requests.post(API_BASE, params)
            if response.status_code == 400:
                return response.status_code
            if response:
                r = response.json()
                context = {"context": r}
        except Exception as e:
            print(e)
        return JsonResponse(context)

    def crearEditarCurso(request):
        calificacion = 0
        actividad = 0
        visibilidad = 0
        sesiones = 0
        notificacion = 0
        if ('calificaciones' in request.POST):
            calificacion = 1
        if ('informeActividad' in request.POST):
            actividad = 1
        if ('visibleAlumno' in request.POST):
            visibilidad = 1
        if ('secciones' in request.POST):
            sesiones = 1
        if ('notificacion' in request.POST):
            notificacion = 1
        if (request.POST['id'] == ""):
            fecha_inicio = datetime.strptime(request.POST['fechaInicio'], '%m/%d/%Y')
            fecha_fin = datetime.strptime(request.POST['fechaFin'], '%m/%d/%Y')
            tiempo = delorean.Delorean(fecha_inicio, timezone='UTC').epoch * 1
            tiempo2 = delorean.Delorean(fecha_fin, timezone='UTC').epoch * 1
            wsfunction = "core_course_create_courses"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "courses[0][fullname]": request.POST["fullName"],
                      "courses[0][shortname]": request.POST["nameShort"],
                      "courses[0][categoryid]": request.POST['categoria'],
                      "courses[0][summary]": request.POST['resumen'],
                      "courses[0][showgrades]": calificacion,
                      "courses[0][newsitems]": 5,
                      "courses[0][startdate]": int(tiempo),
                      "courses[0][enddate]": int(tiempo2),
                      "courses[0][numsections]": 1,
                      "courses[0][maxbytes]": 0,
                      "courses[0][showreports]": actividad,
                      "courses[0][visible]": visibilidad,
                      "courses[0][hiddensections]": sesiones,
                      "courses[0][groupmode]": 0,
                      "courses[0][groupmodeforce]": 0,
                      "courses[0][defaultgroupingid]": 0,
                      "courses[0][enablecompletion]": 0,
                      "courses[0][completionnotify]": notificacion,
                      "courses[0][lang]": "es",
                      }
        else:
            fecha_inicio_edit = datetime.strptime(request.POST['fechaInicio'], '%m/%d/%Y')
            fecha_fin_edit = datetime.strptime(request.POST['fechaFin'], '%m/%d/%Y')
            tiempo1_edit = delorean.Delorean(fecha_inicio_edit, timezone='UTC').epoch * 1
            tiempo2_edit = delorean.Delorean(fecha_fin_edit, timezone='UTC').epoch * 1
            wsfunction = "core_course_update_courses"
            params = {"wstoken": TOKEN_MOODLE,
                      "wsfunction": wsfunction,
                      "moodlewsrestformat": "json",
                      "courses[0][id]": request.POST["id"],
                      "courses[0][fullname]": request.POST["fullName"],
                      "courses[0][shortname]": request.POST["nameShort"],
                      "courses[0][categoryid]": request.POST['categoria'],
                      "courses[0][summary]": request.POST['resumen'],
                      "courses[0][showgrades]": calificacion,
                      "courses[0][newsitems]": 5,
                      "courses[0][startdate]": int(tiempo1_edit),
                      "courses[0][enddate]": int(tiempo2_edit),
                      "courses[0][numsections]": 1,
                      "courses[0][maxbytes]": 0,
                      "courses[0][showreports]": actividad,
                      "courses[0][visible]": visibilidad,
                      "courses[0][hiddensections]": sesiones,
                      "courses[0][groupmode]": 0,
                      "courses[0][groupmodeforce]": 0,
                      "courses[0][defaultgroupingid]": 0,
                      "courses[0][enablecompletion]": 0,
                      "courses[0][completionnotify]": notificacion,
                      "courses[0][lang]": "es",
                      }

        try:
            response = requests.post(API_BASE, params)
            if response:
                r = response.json()
                if response.status_code == 400:
                    print("ENTRA AL IF 400 " + str(response))
                    print("400")
                if response.status_code == 500:
                    print("ENTRA AL IF 500 " + str(response))
                    print("500")
                if response.status_code == 200:
                    print(r)
                    print("ENTRA AL IF 200 " + str(response))
            else:
                print("NO ENTRA al if")
        except Exception as e:
            print("error " + str(e))
        return redirect('cursos')

    def deleteCourse(request, idCourse):
        params = {
            "wstoken": TOKEN_MOODLE,
            "wsfunction": "core_course_delete_courses",
            "moodlewsrestformat": "json",
            "courseids[0]": idCourse,
        }
        try:
            respuesta = requests.post(API_BASE, params)
            if respuesta:
                r = respuesta.json()
            if respuesta.status_code == 400:
                print(r.message)
            else:
                print("si se borro")
        except Exception as e:
            print(e)
        return redirect('cursos')
