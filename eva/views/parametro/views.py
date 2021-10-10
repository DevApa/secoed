from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Parametro, Ciclo
from eva.forms import ParametroForm
from django.http import JsonResponse


class ParameterListView(ListView):
    model = Parametro
    template_name = 'parametro/list.html'
    success_url = reverse_lazy('eva:list-parameter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Cabecera Parámetros'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['create_url'] = reverse_lazy('eva:create-parameter')
        context['url_list'] = reverse_lazy('eva:list-parameter')
        return context


class ParameterCreateView(CreateView):
    model = Parametro
    form_class = ParametroForm
    template_name = "parametro/create.html"
    success_url = reverse_lazy('eva:list-parameter')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()
                    message = f'{self.model.__name__} registrado correctamente'
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
        context['title'] = 'Creación de Parámetro'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-parameter')
        return context
    

class ParameterUpdateView(UpdateView):
    model = Parametro
    form_class = ParametroForm
    template_name = "parametro/update.html"
    success_url = reverse_lazy('eva:list-parameter')

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
        context['title'] = 'Actualizar Parámetro'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-parameter')
        return context


class ParameterDeleteView(DeleteView):
    model = Parametro
    success_url = reverse_lazy('eva:list-parameter')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            parameter = self.get_object()
            parameter.delete()
            message = f'{self.model.__name__} eliminado correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-parameter')
