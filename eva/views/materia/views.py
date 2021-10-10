from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Materia, Ciclo
from eva.forms import MateriaForm
from django.http import JsonResponse


class MatterListView(ListView):
    model = Materia
    template_name = 'materia/list.html'
    success_url = reverse_lazy('eva:list-matter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Materia'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['create_url'] = reverse_lazy('eva:create-matter')
        context['url_list'] = reverse_lazy('eva:list-matter')
        return context


class MatterCreateView(CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = "materia/create.html"
    success_url = reverse_lazy('eva:list-matter')
    
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
        context['title'] = 'Creación de Materia'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-matter')
        return context
    

class MatterUpdateView(UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = "materia/update.html"
    success_url = reverse_lazy('eva:list-matter')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
           if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                message = f'{self.model.__name__} actualizada correctamente'
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
        context['title'] = 'Actualizar Materia'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-matter')
        return context


class MatterDeleteView(DeleteView):
    model = Materia
    success_url = reverse_lazy('eva:list-matter')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            matter = self.get_object()
            matter.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-matter')
