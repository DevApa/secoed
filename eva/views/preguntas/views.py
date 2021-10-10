from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from eva.models import Pregunta, Categoria, Ciclo
from eva.forms import PreguntaForm
from django.http import JsonResponse


class QuestionsListView(ListView):
    model = Pregunta
    template_name = 'preguntas/list.html'
    success_url = reverse_lazy('eva:list-questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Mantenimiento Pregunta'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['create_url'] = reverse_lazy('eva:create-questions')
        context['url_list'] = reverse_lazy('eva:list-questions')
        return context


class QuestionsCreateView(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "preguntas/create.html"
    success_url = reverse_lazy('eva:list-questions')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()
                    message = f'{self.model.__name__} registrada correctamente'
                    error = 'No han ocurrido errores'
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 201
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo registrar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Pregunta'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-questions')
        return context


class QuestionsUpdateView(UpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = "preguntas/update.html"
    success_url = reverse_lazy('eva:list-questions')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST, instance=self.get_object())
                if form.is_valid():
                    form.save()
                    message = f'{self.model.__name__} actualizado correctamente'
                    error = 'No hay error'
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 201
                    return response
                else:
                    message = f'{self.model.__name__} no se pudo actualizar!'
                    error = form.errors
                    response = JsonResponse({'message': message, 'error': error})
                    response.status_code = 400
                    return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Pregunta'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-questions')
        return context


class QuestionsDeleteView(DeleteView):
    model = Pregunta
    success_url = reverse_lazy('eva:list-questions')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            questions = self.get_object()
            questions.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-questions')


class PreguntasAutoView(TemplateView):
    model = Pregunta
    template_name = 'preguntas/auto-preguntas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Preguntas de Autoevaluación'
        context['questions'] = Pregunta.objects.filter(type=1)
        context['categories'] = Categoria.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class PreguntasCoeView(TemplateView):
    model = Pregunta
    template_name = 'preguntas/coe-preguntas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Preguntas de Coevaluación'
        context['questions'] = Pregunta.objects.filter(type=2)
        context['categories'] = Categoria.objects.all()
        return context
