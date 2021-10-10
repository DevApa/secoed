from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from eva.models import Categoria, Ciclo
from eva.forms import CategoriaForm
from django.http import JsonResponse


class CategoryListView(ListView):
    model = Categoria
    template_name = 'categoria/list.html'
    success_url = reverse_lazy('eva:list-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Matenimiento Categorias'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        context['object_list'] = Categoria.objects.filter(state=True)
        context['create_url'] = reverse_lazy('eva:create-category')
        context['url_list'] = reverse_lazy('eva:list-category')
        return context


class CategoryCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/create.html"
    success_url = reverse_lazy('eva:list-category')
    
    def post(self, request, *args, **kwargs):
        response = None
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
            message = 'error'
            response = JsonResponse({'message': message, 'error': str(e)})
        return JsonResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Categoria'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('eva:list-category')
        return context
    

class CategoryUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categoria/update.html"
    success_url = reverse_lazy('eva:list-category')

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
        context['title'] = 'Actualizar Categoria'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('eva:list-category')
        return context


class CategoryDeleteView(DeleteView):
    model = Categoria
    success_url = reverse_lazy('eva:list-category')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            category = self.get_object()
            category.state = False
            category.save()
            message = f'{self.model.__name__} eliminada correctamente!'
            errors = 'No se encontraron errores'
            response = JsonResponse({'message': message, 'error': errors})
            response.status_code = 201
            return response
        else:
            return redirect('eva:list-category')
