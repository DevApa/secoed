import psycopg2
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from secoed import settings


class DashboardView(View):
    def get(self, request):
        greeting = {'heading': "Inicio", 'pageview': "Inicio"}
        if 'username' in request.session:
            return render(request, 'dashboard/dashboard.html', greeting)
        else:
            return redirect('pages-login')


class AjaxEvent(View):
    def jsnCountLogin(request):
        sql = "SELECT string_agg(CAST(valor AS text),',') FROM(SELECT EXTRACT(dow FROM datetime), COUNT(id) as valor " \
              "FROM easyaudit_loginevent WHERE username = '" \
              + str(request.session['username']) + "' AND login_type=0  GROUP BY 1 ORDER BY 1 ASC ) aux"
        conexion = psycopg2.connect(database=settings.CONEXION_NAME, user=settings.CONEXION_USER,
                                    password=settings.CONEXION_PASSWORD, host=settings.CONEXION_HOST,
                                    port=settings.CONEXION_PORT)
        query = conexion.cursor()
        query.execute(sql)
        array = []
        for fila in query:
            items = fila[0].split(',')
            for item in items:
                array.append(int(item))
        json_object = {
            'key': array
        }
        return JsonResponse(json_object)


class Error404View(TemplateView):
    template_name = "utility/utility-404error.html"


def error_500(solicitud):
    datos = {}
    return render(solicitud, 'utility/utility-500error.html', datos)
