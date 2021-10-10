from django.urls import path
from asesor import views
urlpatterns = [
    #Tablas Módulos Asesor           
    
    #4Tabla Nivel Academico
    path('tablas_N_Ac/', views.Tablas_N_Ac, name='T-Nivel-Aca'),
    path('buscar_N_Ac/', views.buscar_N_Ac,name='buscar_N_Ac'),
    path('agregar-producto_N_Ac/', views.agregar_producto_N_Ac, name="agregar_producto_N_Ac"),
    path('modificar-producto_N_Ac/<id>/', views.modificar_producto_N_Ac, name="modificar_producto_N_Ac"), 
    path('eliminar-producto_N_Ac/<id>/', views.eliminar_producto_N_Ac, name="eliminar_producto_N_Ac"),
    #5Tabla Curso
    path('tablas_Cu/', views.Tablas_Cu, name='T-cur'),
    path('buscar_Cu/', views.buscar_Cu, name='buscar_Cu'),
    path('agregar-producto_Cu/', views.agregar_producto_Cu, name="agregar_producto_Cu"),
    path('modificar-producto_Cu/<id>/', views.modificar_producto_Cu, name="modificar_producto_Cu"),
    path('eliminar-producto_Cu/<id>/', views.eliminar_producto_Cu, name="eliminar_producto_Cu"),
    #6Tabla Asesor
    path('tablas_As/', views.Tablas_As, name='T-As'),
    path('buscar_As/', views.buscar_As,name='buscar_As'),
    path('agregar-producto_As/', views.agregar_producto_As, name="agregar_producto_As"),
    path('modificar-producto_As/<id>/', views.modificar_producto_As, name="modificar_producto_As"),
    path('eliminar-producto_As/<id>/', views.eliminar_producto_As, name="eliminar_producto_As"),
    #7Tabla Docente
    path('tablas_Do/', views.Tablas_Do, name='T-Doc'),
    path('buscar_Do/', views.buscar_Do,name='buscar_Do'),
    path('agregar-producto_Do/', views.agregar_producto_Do, name="agregar_producto_Do"),
    path('modificar-producto_Do/<id>/', views.modificar_producto_Do, name="modificar_producto_Do"),
    path('eliminar-producto_Do/<id>/', views.eliminar_producto_Do, name="eliminar_producto_Do"),
    #8Tablas Periodo
    path('tablas_Pe/', views.Tablas_Pe, name='T-Per'),
    path('buscar_Pe/', views.buscar_Pe, name='buscar_Pe'),
    path('agregar-producto_Pe/', views.agregar_producto_Pe, name="agregar_producto_Pe"),
    path('modificar-producto_Pe/<id>/', views.modificar_producto_Pe, name="modificar_producto_Pe"),
    path('eliminar-producto_Pe/<id>/', views.eliminar_producto_Pe, name="eliminar_producto_Pe"),
    #9Tabla Recursos
    path('tablas_Re/', views.Tablas_Re, name='T-Rec'),
    path('buscar_Re/', views.buscar_Re, name='buscar_Re'),
    path('agregar-producto_Re/', views.agregar_producto_Re, name="agregar_producto_Re"),
    path('modificar-producto_Re/<id>/', views.modificar_producto_Re, name="modificar_producto_Re"),
    path('eliminar-producto_Re/<id>/', views.eliminar_producto_Re, name="eliminar_producto_Re"),
    #10Tabla Cursos Asesor
    path('tablas_Cu_As/', views.Tablas_Cu_As, name='T-Cur-As'),
    path('buscar_Cu_As/', views.buscar_Cu_As, name='buscar_Cu_As'),
    path('agregar-producto_Cu_As/', views.agregar_producto_Cu_As, name="agregar_producto_Cu_As"),
    path('modificar-producto_Cu_As/<id>/', views.modificar_producto_Cu_As, name="modificar_producto_Cu_As"),
    path('eliminar-producto_Cu_As/<id>/', views.eliminar_producto_Cu_As, name="eliminar_producto_Cu_As"),     
    #11Tabla Titulos
    path('tablas_Ti/', views.Tablas_Ti, name='T-Ti'),
    path('buscar_Ti/', views.buscar_Ti, name='buscar_Ti'),    
    path('agregar_producto_Ti/', views.agregar_producto_Ti, name="agregar_producto_Ti"),
    path('modificar-producto_Ti/<id>/', views.modificar_producto_Ti, name="modificar_producto_Ti"),
    path('eliminar-producto_Ti/<id>/', views.eliminar_producto_Ti, name="eliminar_producto_Ti"),    

    #Cronograma
    #12Tabla Cabecera Crono
    path('tablas_Cab_Cro/', views.Tablas_Cab_Cro, name='t-cab_crono'),
    path('buscar_Cab_Cro/', views.buscar_Cab_Cro,name='buscar_Cab_Cro'),
    path('agregar-producto_Cab_Cro/', views.agregar_producto_Cab_Cro, name="agregar_producto_Cab_Cro"),
    path('modificar-producto_Cab_Cro/<id>/', views.modificar_producto_Cab_Cro, name="modificar_producto_Cab_Cro"),
    path('eliminar-producto_Cab_Cro/<id>/', views.eliminar_producto_Cab_Cro, name="eliminar_producto_Cab_Cro"),    
    #13 Observaciones_Cabecera
    path('t-cab_crono_observaciones/', views.Cab_crono_observaciones, name='t-cab_crono_observaciones'),
    path('buscar_Cab_Cro_ob/', views.buscar_Cab_Cro_ob,name='buscar_Cab_Cro_ob'),
    path('agregar_Cab_Cro_ob/', views.agregar_Cro_ob, name='agregar_Cro_ob'),
    path('modificar_Cab_Cro_ob/<id>/', views.modificar_Cro_ob, name='modificar_Cro_ob'),
    path('eliminar_Cab_Cro_ob/<id>/', views.eliminar_Cro_ob, name='eliminar_Cro_ob'),
    path('SolicitarObserva', views.SolicitarObserva, name="SolicitarObserva"),
    #14Tabla Evento Crono
    path('tablas_Event_Cro/', views.Tablas_Event_Crono, name='t-evento_cro'),
    path('buscar_Event_Crono/', views.buscar_Event_Crono, name='buscar_Event_Crono'),
    path('agregar_producto_Event_Crono/', views.agregar_producto_Event_Crono, name="agregar_producto_Event_Crono"),
    path('modificar_producto_Event_Crono/<id>/<user>/', views.modificar_producto_Event_Crono, name="modi_Event"),
    path('eliminar_producto_Event_Crono/<id>/', views.eliminar_producto_Event_Crono, name="eliminar_producto_Event_Crono"),    
    #15Crono_Reporte
    path('tablas_Reporte_Crono/', views.Tablas_Reporte_Crono, name='Tablas_Reporte_Crono'), 
    path('buscar_Reporte_Crono/', views.buscar_Reporte_Crono, name='buscar_Reporte_Crono'),         
    path('SolicitarDatos/<id>', views.SolicitarDatos, name="SolicitarDatos"),                      
    #16Crono            
    path('llamar_crono/<id>/', views.llamar_crono, name="llamar_crono"),   
    path('event/<int:event_id>/details/', views.event_details, name="event-detail"),
    path('nextM/<id>/<p>', views.nextM, name="nextM"),                      
               
    #17Reporte Estadistico
    path('Reporte_estadistico',views.estadistico,name='Reporte_estadistico'),
    
    #18Historias
    path('Tabla_Historias/', views.Tabla_Historias, name='T-Historias'), 
    path('B_Tabla_Historias/', views.B_Tabla_Historias, name='B_Tabla_Historias'),
    path('eliminar_Historias/<id>/', views.eliminar_Historias, name="eliminar_Historias"),    
    path('CompararDatos/<id>/<user>/', views.CompararDatos, name="CompararDatos"),

    #19api
    path('cursos_api', views.api_curso, name='cursos_api'),
    path('listado_estudiante/<id>/<nombre>/', views.listado_estudiante, name='listado_estudiante'),
    path('actividades_user/<id>/<nombre>/<idest>/', views.actividades_user, name='actividades_user')
]   