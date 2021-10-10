from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import AreasConocimiento, Ciclo
from eva.forms import AreasConocimientoForm
from django.http import JsonResponse


class KnowledgeAreasListView(ListView):
    model = AreasConocimiento
    template_name = 'areas/list.html'
    success_url = reverse_lazy('eva:list-area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Áreas de Conocimiento'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['action'] = 'add'
        context['create_url'] = reverse_lazy('eva:create-area')
        context['url_list'] = reverse_lazy('eva:list-area')
        return context


class KnowledgeAreasCreateView(CreateView):
    model = AreasConocimiento
    form_class = AreasConocimientoForm
    template_name = "areas/create.html"
    success_url = reverse_lazy('eva:list-area')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.is_ajax():
                option = request.POST['action']
                form = self.get_form()
                if option == 'add':
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
        context['title'] = 'Creación de Área de conocimiento'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-area')
        return context
    

class KnowledgeAreasUpdateView(UpdateView):
    model = AreasConocimiento
    form_class = AreasConocimientoForm
    template_name = "areas/update.html"
    success_url = reverse_lazy('eva:list-area')

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
        context['title'] = 'Actualizar Área de Conocimiento'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-area')
        return context


class KnowledgeAreasDeleteView(DeleteView):
    model = AreasConocimiento
    success_url = reverse_lazy('eva:list-area')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            knowledge_area = self.get_object()
            knowledge_area.delete()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-area')
