from django.urls import path
from cursos import views

urlpatterns = [
    path(r'categoria', views.CursoView.categoria, name='categoria'),
    path(r'allCategorias', views.CursoView.allCategorias, name='categoriaAll'),
    path(r'deleteCategoria/<int:idCategoria>', views.CursoView.deleteCategoria, name='deleteCategoria'),
    path(r'createEditCategoria', views.CursoView.createEditCategoria, name='createEditCategoria'),
    path(r'', views.CursoView.as_view(), name='cursos'),
    path(r'crearEditarCurso', views.CursoView.crearEditarCurso, name='crearEditarCurso'),
    path(r'deleteCourse/<int:idCourse>', views.CursoView.deleteCourse, name='deleteCourse'),
]
