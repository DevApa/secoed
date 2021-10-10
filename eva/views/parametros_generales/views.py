from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import ParametrosGeneral, Ciclo
from eva.forms import ParametrosGeneralForm
from django.http import JsonResponse


class ParameterGrlListView(ListView):
    model = ParametrosGeneral
    template_name = 'parametro/values/list.html'
    success_url = reverse_lazy('eva:list-parameter-grl')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Parámetros Generales'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        parameters = ParametrosGeneral.objects.select_related('parameter')
        print(parameters)
        context['object_list'] = parameters
        context['create_url'] = reverse_lazy('eva:create-parameter-grl')
        context['url_list'] = reverse_lazy('eva:list-parameter-grl')
        return context


class ParameterGrlCreateView(CreateView):
    model = ParametrosGeneral
    form_class = ParametrosGeneralForm
    template_name = "parametro/values/create.html"
    success_url = reverse_lazy('eva:list-parameter-grl')
    
    def post(self, request, *args, **kwargs):
        data = None
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
        context['title'] = 'Creación de Tipo'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-parameter-grl')
        return context
    

class ParameterGrlUpdateView(UpdateView):
    model = ParametrosGeneral
    form_class = ParametrosGeneralForm
    template_name = "parametro/values/update.html"
    success_url = reverse_lazy('eva:list-parameter-grl')

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
        context['title'] = 'Actualizar Tipo'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-parameter-grl')
        return context


class ParameterGrlDeleteView(DeleteView):
    model = ParametrosGeneral
    success_url = reverse_lazy('eva:list-parameter-grl')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            parameter_grl = self.get_object()
            parameter_grl.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-parameter-grl')
