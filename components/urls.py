from django.urls import path
from components import views
# app_name = "components"
urlpatterns = [    

                    # Requisito

    #menu de requisito (tabla de criterios vista)
    path(r'requisito', views.menu, name='requisito'),

    #formulario de nuevo requisito
    path(r'newRequisito', views.requisito, name='newRequisito'),

    #carga los requisitos
    path(r'ajax/loadRequisito', views.loadRequisito, name='loadRequisito'),

    #formulario requisitos con botones delete, update
    path(r'formrequisito',views.menu, name='forms-requisito'),

    # eliminar requisito
    path(r'deleteRequisito/<int:pk>',views.deleteRequisito, name='deleteRequisito'),

    # actualizar requisito
    path('updateRequisito/<int:pk>',views.UpdateRequisito.as_view(), name = 'updateRequisito'),






                                # Asesor
    # Listar asesor curso
    path('formasesor',views.FormAsesor.as_view(), name="forms-asesor"),

    #Obtiene los asesores filtrados y devuelve en formato JSON
    path('asesor/<str:asesor>',views.asesor, name="obtenerAsesor"),

    #Obtiene los curso ha asignar
    path('cursoAsignado/<str:curso>',views.cursoA, name="obtenerCursoA"),

    # Listar curso y filtro
    path('formeducativo',views.FormEducacion.as_view(), name='forms-educativo'),

    #Guarda asesor Curso
    path('guardarAsesorCurso', views.guardarAsesorCurso, name = 'guardarAsesor'),

    # eliminar Asignacion
    path(r'deleteAsignacion/<int:pk>',views.deleteAsignacion, name='deleteAsignacion'),


    #Cursos 
    path('cursos/', views.cursosTodos, name = 'cursos'),


    # Vista de asesores cursos asignados

    path('formeducativo1',views.FormEducaciona.as_view(), name='forms-educativo1'),

                            # Evaluacion
    #Vista evaluacion
    path('formevaluation',views.FormEvaluation.as_view(), name='forms-evaluation'),
    #Notificar email
    path('notify/email',views.sendEmail, name='sendEmail'),
    #Pdf 
    path('notify/pdf',views.getPDF, name='getPDF'),

    #Listado de asesor
    path('listado-Asesor', views.listadoAsesores.as_view(), name = 'listadoAsesores'),

    path('actividades', views.actividades.as_view(), name = 'actividades'),
    path('historial/evaluation', views.historialEvaluations, name = 'historialEvaluations'),
    path('historial/evaluation/<int:id>', views.historialEvaluation, name = 'historialEvaluation'),
]