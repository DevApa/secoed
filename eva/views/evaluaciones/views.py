import json

import requests
from django.core.mail import send_mail
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from authentication.models import Usuario
from conf.models import RolMoodle
from eva.forms import CoevaluacionForm, AutoEvaluacionForm
from eva.models import Respuesta, DetalleRespuesta, ResultadoProceso, ParametrosGeneral, Ciclo, \
    Pregunta, Categoria, Tipo, Parametro, Materia, AreasConocimiento, Courses
from secoed.settings import TOKEN_MOODLE, API_BASE


class TeachersPendingEvaluationList(ListView):
    model = Usuario
    template_name = 'evaluaciones/list.html'
    success_url = reverse_lazy('eva:list-coevaluar')

    def get_pendings_evaluation(self):
        data = []
        by_co_evaluate = []
        type_eva = Tipo.objects.filter(name='Coevaluación').first()
        cycle = Ciclo.objects.filter(is_active=True).first()
        resultado = Respuesta.objects.filter(cycle=cycle.id, type_evaluation=type_eva.id)
        area = AreasConocimiento.objects.filter(docente=self.request.user.id).first()

        if area is not None:
            materia = Materia.objects.filter(area=area.id)
            code = RolMoodle.objects.filter(descripcion='Estudiante').first()
            docentes = Usuario.objects.filter(usuario_activo=True, rol_moodle__codigo__gte=code.codigo)
            for m in materia:
                for d in docentes:
                    if m.teacher_id == d.id:
                        by_co_evaluate.append(d)

            for d in by_co_evaluate:
                coevaluated = resultado.filter(teacher=d.id).first()
                if coevaluated is None:
                    data.append(d)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Docentes pendientes de coevaluar'
        coevaluator = self.request.user.id
        docentes = self.get_pendings_evaluation()
        context['object_list'] = docentes
        context['list_url'] = reverse_lazy('eva:list-coevaluar')
        return context


class AutoEvaluacionCreateView(CreateView):
    model = Usuario
    form_class = AutoEvaluacionForm
    template_name = 'evaluaciones/auto-evaluation.html'
    success_url = reverse_lazy('eva:result-evaluation')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        n3 = 0.00
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Usuario.objects.filter(rol_moodle__codigo__gte=5, id=self.request.user.id).first()
                    if docente is None:
                        usuario = Usuario.objects.filter(id=request.user.id).first()
                        data['message'] = usuario.nombres + ' Usuario no habilitado para el actual proceso'
                        data['error'] = 'No se pudo realizar el proceso!'
                        return JsonResponse(data)
                    else:
                        answer = Respuesta()
                        answer.teacher = docente.id
                        answer.cycle = int(question['cycle'])
                        answer.type_evaluation = int(question['type'])
                        answer.save()

                        for i in question['questions']:
                            resp = DetalleRespuesta()
                            resp.answer_id = answer.id
                            resp.category = int(i['category'])
                            resp.question = int(i['question'])
                            resp.parameter = int(i['parameter'])
                            resp.save()

                        details = DetalleRespuesta.objects.filter(answer=answer.id).values('category',
                                                                                           'question',
                                                                                           'parameter') \
                            .order_by('category')

                        ac_tics = 0.00
                        ac_ped = 0.00
                        ac_did = 0.00
                        c_tic = 0
                        c_ped = 0
                        c_did = 0

                        for item in details:
                            if item['category'] == 1:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_tics += float(value['value'])
                                c_tic += 1
                            elif item['category'] == 2:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_ped += float(value['value'])
                                c_ped += 1
                            elif item['category'] == 3:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                ac_did += float(value['value'])
                                c_did += 1

                        aux_tic = round((float(ac_tics) / c_tic) * 100, 2)
                        aux_ped = round((float(ac_ped) / c_ped) * 100, 2)
                        aux_did = round((float(ac_did) / c_did) * 100, 2)
                        total_auto = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        result = ResultadoProceso.objects.filter(cycle=answer.cycle,
                                                                 user=answer.teacher,
                                                                 coevaluator__isnull=False).first()
                        if result is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.user = answer.teacher
                            result.cycle = answer.cycle

                            result.auto_result_Tic = aux_tic
                            result.auto_result_Ped = aux_ped
                            result.auto_result_Did = aux_did

                            result.Total_Proceso_Auto = total_auto

                            result.save()

                            message = 'Autoevaluación concluida correctamente'
                            error = ''
                            response = JsonResponse({'message': message, 'error': error})
                            response.status_code = 201
                            return response
                        else:
                            result = ResultadoProceso.objects. \
                                filter(cycle=answer.cycle,
                                       user=answer.teacher,
                                       coevaluator__isnull=False).update(auto_result_Tic=aux_tic,
                                                                         auto_result_Ped=aux_ped,
                                                                         auto_result_Did=aux_did,
                                                                         Total_Proceso_Auto=total_auto)
                            if result:
                                obj = ResultadoProceso.objects.filter(cycle=answer.cycle, user=answer.teacher,
                                                                      coevaluator__isnull=False).first()
                                coevaluator = Usuario.objects.filter(identificacion=obj.coevaluator).first()

                                if obj.Total_Proceso_Coe > 0:
                                    auto_subtotal = float(obj.Total_Proceso_Coe) + float(obj.Total_Proceso_Auto)
                                    obj.Total_Proceso = round(auto_subtotal / 2, 2)

                                    obj.save()

                                    result_ped = (float(obj.auto_result_Ped) + float(obj.coe_result_Ped)) / 2
                                    result_did = (float(obj.auto_result_Did) + float(obj.coe_result_Did)) / 2
                                    result_tic = (float(obj.auto_result_Tic) + float(obj.coe_result_Tic)) / 2

                                    parameter = Parametro.objects.filter(name='Indicadores').first()
                                    kpi = ParametrosGeneral.objects.filter(parameter=parameter.id)

                                    c_tics = Courses.objects.filter(sortName='TICs').first()
                                    c_ped = Courses.objects.filter(sortName='Pedagogía').first()
                                    c_did = Courses.objects.filter(sortName='Didáctica').first()

                                    for ind in kpi:
                                        if ind.code == 'RCA':
                                            n3 = float(ind.value)

                                    if result_ped > n3:
                                        data[
                                            'message'] = 'Felicidades ha concluido en proceso' \
                                                         ' de auto y co evaluaciòn de manera èxitosa '
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(self.request.user, c_ped.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_ped.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_ped.fullName)
                                    if result_did > n3:
                                        data['message'] = 'Felicidades ha concluido en proceso ' \
                                                          'de auto y co evaluaciòn de manera èxitosa '
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(self.request.user, c_did.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_did.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_did.fullName)
                                    if result_tic >= n3:
                                        data['message'] = 'Felicidades ha concluido en proceso' \
                                                          ' de auto y co evaluaciòn de manera èxitosa '
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(self.request.user, c_tics.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_tics.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_tics.fullName)

                                    message = 'Proceso de Coevaluación concluido correctamente'
                                    error = ''

                                    response = JsonResponse({'message': message, 'error': error})
                                    response.status_code = 201
                                    return response
        except Exception as e:
            message = 'Exception'
            response['error'] = {'message': message, 'error': str(e)}
            transaction.rollback()
            return JsonResponse(response)
        except IntegrityError:
            transaction.rollback()
            return JsonResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'AutoEvaluación'
        tipo = Tipo.objects.filter(name='Autoevaluación').first()
        parametro = Parametro.objects.filter(name='Autoevaluación').first()
        context['object_list'] = Pregunta.objects.filter(type=tipo.id, state=True)
        context['categories'] = Categoria.objects.filter(state=True)
        context['parameters'] = ParametrosGeneral.objects.filter(parameter=parametro.id)
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['cycle'] = cycle
        teacher = Usuario.objects.filter(id=self.request.user.id).first()
        flag = False
        if teacher is not None:
            evaluate = Respuesta.objects.filter(teacher=teacher.id,
                                                cycle=cycle.id,
                                                type_evaluation=tipo.id).first()
            if evaluate is None:
                flag = True
        context['verification'] = flag
        context['type'] = tipo.id
        context['type_evaluation'] = 'AUTO EVALUACIÓN DOCENTE'
        return context


def send_mail_notification(docente: Usuario, coevaluator:Usuario=None, course=None):
    subject = 'Matriculación Automática'

    if coevaluator is None:
        email_template_name = "evaluaciones/enroll-email.txt"
        content = {'nombres': docente.nombres, 'apellidos': docente.apellidos, 'course': course, }
    else:
        email_template_name = "evaluaciones/coevaluator-email.txt"
        content = {'nombres': docente.nombres, 'apellidos': docente.apellidos, 'course': course,
                   'c_name': coevaluator.nombres, 'c_last_name': coevaluator.apellidos,}
    c = content
    email_1 = render_to_string(email_template_name, c)
    if coevaluator is None:
        send_mail(subject, email_1, 'secoed.web@gmail.com', [docente.email], fail_silently=False)
    else:
        send_mail(subject, email_1, 'secoed.web@gmail.com', [coevaluator.email], fail_silently=False)


def enroll_course_evaluation(user: Usuario, course):
    params = {
        "wstoken": TOKEN_MOODLE,
        "wsfunction": "enrol_manual_enrol_users",
        "moodlewsrestformat": "json",
        "enrolments[0][userid]": user.moodle_user,
        "enrolments[0][courseid]": course,
        "enrolments[0][roleid]": user.rol_moodle.codigo
    }
    response = requests.post(API_BASE, params)

    if response.ok:
        data = 'OK'
    else:
        data = 'error'
    return data


class CoevaluacionCreateView(CreateView):
    model = Usuario
    form_class = CoevaluacionForm
    template_name = 'evaluaciones/co-evaluation.html'
    success_url = reverse_lazy('eva:list-coevaluation')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {}
        n3 = 0.00
        try:
            action = self.request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    question = json.loads(request.POST['answers'])
                    docente = Usuario.objects.filter(id=int(request.session['docente'])).first()
                    coevaluator = Usuario.objects.filter(id=self.request.user.id).first()
                    if docente is None:
                        data['message'] = 'usuario no habilitado para está evaluación'
                        return JsonResponse(data)
                    else:
                        answer = Respuesta()
                        answer.teacher = docente.id
                        answer.cycle = int(question['cycle'])
                        answer.type_evaluation = int(question['type'])
                        answer.save()
                        for i in question['questions']:
                            resp = DetalleRespuesta()
                            resp.answer_id = answer.id
                            resp.category = int(i['category'])
                            resp.question = int(i['question'])
                            resp.parameter = int(i['parameter'])
                            resp.save()

                        detalle = DetalleRespuesta.objects.filter(answer=answer.id) \
                            .values('category', 'question', 'parameter').order_by('category')

                        coe_tics = 0.00
                        coe_peda = 0.00
                        coe_dida = 0.00
                        c_tic = 0
                        c_ped = 0
                        c_did = 0

                        for item in detalle:
                            if item['category'] == 1:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_tics += float(value['value'])
                                c_tic += 1
                            elif item['category'] == 2:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_peda += float(value['value'])
                                c_ped += 1
                            elif item['category'] == 3:
                                value = ParametrosGeneral.objects.values('value').filter(
                                    id=int(item['parameter'])).first()
                                coe_dida += float(value['value'])
                                c_did += 1

                        aux_tic = round((float(coe_tics) / c_tic) * 100, 2)
                        aux_ped = round((float(coe_peda) / c_ped) * 100, 2)
                        aux_did = round((float(coe_dida) / c_did) * 100, 2)
                        total_coe = round((aux_tic + aux_ped + aux_did) / 3, 2)

                        evaluated = ResultadoProceso.objects.filter(user=docente.id, cycle=answer.cycle).first()
                        if evaluated is None:
                            result = ResultadoProceso()
                            result.answer_id = answer.id
                            result.cycle = answer.cycle
                            result.user = docente.id
                            result.coevaluator = coevaluator.identificacion

                            result.coe_result_Tic = aux_tic
                            result.coe_result_Ped = aux_ped
                            result.coe_result_Did = aux_did

                            result.Total_Proceso_Coe = total_coe

                            result.save()
                            message = 'Coevaluación concluida correctamente'
                            error = ''
                            response = JsonResponse({'message': message, 'error': error})
                            response.status_code = 201
                            return response
                        else:
                            result = ResultadoProceso.objects. \
                                filter(cycle=answer.cycle, user=answer.teacher)\
                                .update(coevaluator=coevaluator.identificacion,
                                        coe_result_Tic=aux_tic,
                                        coe_result_Ped=aux_ped,
                                        coe_result_Did=aux_did,
                                        Total_Proceso_Coe=total_coe)

                            if result:

                                obj = ResultadoProceso.objects.filter(cycle=answer.cycle, user=answer.teacher,
                                                                      coevaluator__isnull=False).first()
                                if obj.Total_Proceso_Auto > 0:
                                    subtotal = float(obj.Total_Proceso_Auto) + float(obj.Total_Proceso_Coe)
                                    obj.Total_Proceso = round(subtotal / 2, 2)
                                    obj.save()

                                    result_ped = (float(obj.auto_result_Ped) + float(obj.coe_result_Ped)) / 2
                                    result_did = (float(obj.auto_result_Did) + float(obj.coe_result_Did)) / 2
                                    result_tic = (float(obj.auto_result_Tic) + float(obj.coe_result_Tic)) / 2
                                    kpi = ParametrosGeneral.objects.filter(parameter=3)

                                    c_tics = Courses.objects.filter(sortName='TICs').first()
                                    c_ped = Courses.objects.filter(sortName='Pedagogía').first()
                                    c_did = Courses.objects.filter(sortName='Didáctica').first()

                                    for ind in kpi:
                                        if ind.code == 'RCA':
                                            n3 = float(ind.value)

                                    if result_ped > n3:
                                        message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                  'èxitosa en Pedagogía'
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(docente, c_ped.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_ped.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_ped.fullName)
                                    if result_did > n3:
                                        message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                  'èxitosa en '
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(docente, c_did.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_did.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_did.fullName)
                                    if result_tic > n3:
                                        message = 'Felicidades ha concluido en proceso de auto y co evaluaciòn de manera ' \
                                                  'èxitosa en '
                                    else:
                                        # Matriculación en moodle
                                        response_enroll = enroll_course_evaluation(docente, c_tics.idMoodle)
                                        if response_enroll == 'OK':
                                            # Envio de correo al docente
                                            send_mail_notification(docente, None, c_tics.fullName)
                                            # Envio de Correo al Coevaluador
                                            send_mail_notification(docente, coevaluator, c_tics.fullName)

                                message = 'Coevaluación concluida correctamente'
                                del request.session['docente']

                                error = ''
                                response = JsonResponse({'message': message, 'error': error})
                                response.status_code = 201
                                return response
        except Exception as e:
            response['error'] = str(e)
            transaction.rollback()
            return JsonResponse(response)
        except IntegrityError:
            transaction.rollback()
            return JsonResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['docente'] = self.request.GET.get('docente')
        context['heading'] = 'Coevaluacion'
        url = reverse_lazy('eva:list-coevaluar')
        context['list_url'] = url
        docente = Usuario.objects.filter(id=self.request.user.id).first()
        if docente is not None:
            if docente.rol_moodle.codigo != 4:
                context['retorno'] = url
                return context
        tipo = Tipo.objects.filter(name='Coevaluación').first()
        parametro = Parametro.objects.filter(name='Coevaluación').first()
        context['object_list'] = Pregunta.objects.filter(type=tipo.id)
        context['categories'] = Categoria.objects.filter(state=True)
        context['parameters'] = ParametrosGeneral.objects.filter(parameter=parametro.id)
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['cycle'] = cycle
        teacher = int(self.request.GET.get('docente'))
        evaluate = Respuesta.objects.filter(teacher=teacher, cycle=cycle.id, type_evaluation=tipo.id).first()
        flag = False
        if evaluate is None:
            flag = True
        context['verification'] = flag
        context['type'] = tipo.id
        context['type_evaluation'] = 'COE EVALUACION DOCENTE'
        return context
