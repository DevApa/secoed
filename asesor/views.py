from django.shortcuts import render, redirect, get_object_or_404
import json
import requests
from secoed.settings import TOKEN_MOODLE
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  Nivel_Académico, Cursos, Asesor, Docentes, Periodo, Recursos, Curso_Asesor, Cabecera_Crono, Titulos, Event, Observaciones, registro_historicos
from .forms import  Nivel_AcadémicoForm, CursosForm, AsesorForm, DocentesForm, PeriodoForm, RecursosForm, Curso_AsesorForm, Cabecera_CronoForm, TitulosForm, Cabecera_Crono_ObForm, EventForm, historiasForm, curso_FechaForm
from django.http import HttpResponse

#Calendario
from .utils import Calendar
from datetime import datetime, date
import calendar, locale
# locale.setlocale(locale.LC_ALL, 'es-ES')
from django.utils.safestring import mark_safe
from datetime import timedelta

# Create your views here.

#4Tabla Nivel Academico
@login_required
def Tablas_N_Ac(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Nivel_Académico.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }   
    return render(request, "asesor/base/t-Nivel-Aca.html", data)
@login_required
def buscar_N_Ac(request):

        a='Id'
        b='Nivel'        
        c='Detalle'  

        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>20:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Nivel_Académico.objects.filter(id_academico__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   
                    return render(request, "asesor/base/t-Nivel-Aca.html", data)

                elif b_ava==b:
                                            
                    uni=Nivel_Académico.objects.filter(Nivel__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   
                    return render(request, "asesor/base/t-Nivel-Aca.html", data)
                                            
                elif b_ava==c:

                    uni=Nivel_Académico.objects.filter(Detalle__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   
                    return render(request, "asesor/base/t-Nivel-Aca.html", data)

                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Nivel_Académico.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            }   
            return render(request, "asesor/base/t-Nivel-Aca.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_N_Ac(request):

    data = {
        'form': Nivel_AcadémicoForm(),
        'N':"Tabla Nivel Académico",
        'P':"agregar_producto_N_Ac" 
                   
    }

    if request.method == 'POST':

        formulario = Nivel_AcadémicoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Nivel-Aca')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Nivel-Aca')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_N_Ac(request, id):

    producto = get_object_or_404(Nivel_Académico, id_academico=id)

    data = {
        'form': Nivel_AcadémicoForm(instance=producto),
        'N':"Tabla Nivel Académico",
        'id':id,
        'h':producto, 
        't':"modificar_producto_N_Ac"
    }
        
    if request.method == 'POST':
        formulario = Nivel_AcadémicoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Nivel-Aca')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Nivel-Aca')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_N_Ac(request, id):

    producto = get_object_or_404(Nivel_Académico, id_academico=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_N_Ac"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Nivel-Aca')
    return render(request, 'asesor/crud/delete.html', data)

#5Tabla Curso
@login_required
def Tablas_Cu(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Cursos.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }   
    return render(request, "asesor/base/t-cur.html", data)
@login_required
def buscar_Cu(request):

        a='Id'
        b='Tipo'        
        c='Estado'
        d='Fecha de Apertura'
        e='Fecha fin'
        f='Carrera'

        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Cursos.objects.filter(Id_curso__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html",data)

                elif b_ava==b:
                                            
                    uni=Cursos.objects.filter(Tipo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html",data)
                                            
                elif b_ava==c:

                    uni=Cursos.objects.filter(Estado__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html",data)
                
                elif b_ava==d:

                    uni=Cursos.objects.filter(Fecha_de_Apertura__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html", data)

                elif b_ava==e:

                    uni=Cursos.objects.filter(Fecha_fin__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html", data)
            
                elif b_ava==f:

                    uni=Cursos.objects.filter(Carrera__descripcion__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-cur.html", data)

                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Cursos.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            }   
            return render(request, "asesor/base/t-cur.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Cu(request):

    data = {
        'form': curso_FechaForm(),
        'N':"Tabla Cursos",                    
    }

    if request.method == 'POST':

        formulario = curso_FechaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-cur')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-cur')

    return render(request, 'asesor/crud/agregar_editar_curso/agregar.html', data)
@login_required
def modificar_producto_Cu(request, id):

    producto = get_object_or_404(Cursos, Id_curso=id)

    data = {
        'form': curso_FechaForm(instance=producto),
        'N':"Tabla Cursos",
        'id':id,
        'h':producto,                     
    }
        
    if request.method == 'POST':
        formulario = curso_FechaForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-cur')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-cur')

    return render(request, 'asesor/crud/agregar_editar_curso/editar.html', data)
@login_required
def eliminar_producto_Cu(request, id):

    producto = get_object_or_404(Cursos, Id_curso=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Cu"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-cur')
    return render(request, 'asesor/crud/delete.html', data)
#6Tabla Asesor
@login_required
def Tablas_As(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Asesor.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }  
    return render(request, "asesor/base/t-As.html", data)
@login_required
def buscar_As(request):

        a='id'
        b='Nombres'        
        c='Apellidos'
        d='Titulo'
        e='Nivel_Académico'
        f='Correo'
        g='Carrera'

        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Asesor.objects.filter(id_asesor__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)

                elif b_ava==b:
                                            
                    uni=Asesor.objects.filter(Nombres__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)
                                            
                elif b_ava==c:

                    uni=Asesor.objects.filter(Apellidos__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)
                
                elif b_ava==d:

                    uni=Asesor.objects.filter(Titulo__Nombramiento__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)

                elif b_ava==e:

                    uni=Asesor.objects.filter(Nivel_Académico__Nivel__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)

                elif b_ava==f:

                    uni=Asesor.objects.filter(Correo__icontains=producto)       
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }                                                                          
                    return render(request, "asesor/base/t-As.html", data)

                elif b_ava==g:

                    uni=Asesor.objects.filter(Carrera__descripcion__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-As.html", data)

                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Asesor.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            } 
            return render(request, "asesor/base/t-As.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_As(request):

    data = {
        'form': AsesorForm(),
        'N':"Tabla Asesor",
        'P':"agregar_producto_As" 
      
    }

    if request.method == 'POST':

        formulario = AsesorForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-As')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-As')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_As(request, id):

    producto = get_object_or_404(Asesor, id_asesor=id)

    data = {
        'form': AsesorForm(instance=producto),
        'N':"Tabla Asesor",
        'id':id,
        'h':producto,
        't':"modificar_producto_As"      
    }
        
    if request.method == 'POST':
        formulario = AsesorForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-As')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-As')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_As(request, id):

    producto = get_object_or_404(Asesor, id_asesor=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_As"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-As')
    return render(request, 'asesor/crud/delete.html', data)

#7Tabla Docente
@login_required
def Tablas_Do(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Docentes.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }   
    return render(request, "asesor/base/t-Doc.html",data)
@login_required
def buscar_Do(request):

        a='id'
        b='Nombres'        
        c='Apellidos'
        d='Titulo'
        e='Nivel Académico'
        f='Correo'
        g='Curso'        
        h='Carrera'

        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Docentes.objects.filter(id_docentes__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }   

                    return render(request, "asesor/base/t-Doc.html", data)

                elif b_ava==b:
                                            
                    uni=Docentes.objects.filter(Nombres__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Doc.html", data)
                                            
                elif b_ava==c:

                    uni=Docentes.objects.filter(Apellidos__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Doc.html", data)
                
                elif b_ava==d:

                    uni=Docentes.objects.filter(Titulo__Nombramiento__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Doc.html", data)

                elif b_ava==e:

                    uni=Docentes.objects.filter(Nivel_Académico__Nivel__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Doc.html", data)

                elif b_ava==f:

                    uni=Docentes.objects.filter(Correo__icontains=producto)   
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }                                                                               
                    return render(request, "asesor/base/t-Doc.html", data)

                elif b_ava==g:

                    uni=Docentes.objects.filter(Curso__Tipo__icontains=producto)           
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }                                                                       
                    return render(request, "asesor/base/t-Doc.html", data)             

                elif b_ava==h:

                    uni=Docentes.objects.filter(Carrera__descripcion__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Doc.html", data)

                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Docentes.objects.all()
            data = {  
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            }  
            return render(request, "asesor/base/t-Doc.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Do(request):

    data = {
        'form': DocentesForm(),
        'N':"Tabla Docente",
        'P':"agregar_producto_Do" 

    }

    if request.method == 'POST':

        formulario = DocentesForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Doc')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Doc')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Do(request, id):

    producto = get_object_or_404(Docentes, id_docentes=id)

    data = {
        'form': DocentesForm(instance=producto),
        'N':"Tabla Docente",
        'id':id,
        'h':producto,
        't':"modificar_producto_Do" 
       
    }
        
    if request.method == 'POST':
        formulario = DocentesForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Doc')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Doc')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Do(request, id):

    producto = get_object_or_404(Docentes, id_docentes=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Do"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Doc')
    return render(request, 'asesor/crud/delete.html', data)
#8Tablas Periodo
@login_required
def Tablas_Pe(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Periodo.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    } 
    return render(request, "asesor/base/t-Per.html",data)
@login_required
def buscar_Pe(request):

        a='Id'
        b='Tipo'            
        
        u="Mantenimiento de Código"
        t="Tabla"    
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Periodo.objects.filter(id_periodo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Per.html", data)

                elif b_ava==b:
                                            
                    uni=Periodo.objects.filter(Tipo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Per.html", data)
                                                           
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Periodo.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            } 
            return render(request, "asesor/base/t-Per.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Pe(request):

    data = {
        'form': PeriodoForm(),
        'N':"Tabla Recursos",
        'P':"agregar_producto_Pe" 

    }

    if request.method == 'POST':

        formulario = PeriodoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Per')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Per')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Pe(request, id):

    producto = get_object_or_404(Periodo, id_periodo=id)

    data = {
        'form': PeriodoForm(instance=producto),
        'N':"Tabla Periodo",
        'id':id,
        'h':producto,
        't':"modificar_producto_Pe"     
    }
        
    if request.method == 'POST':
        formulario = PeriodoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Per')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Per')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Pe(request, id):

    producto = get_object_or_404(Periodo, id_periodo=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Pe"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Per')
    return render(request, 'asesor/crud/delete.html', data)
#9Tabla Recursos
@login_required
def Tablas_Re(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Recursos.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    } 
    return render(request, "asesor/base/t-Rec.html",data)
@login_required
def buscar_Re(request):

        a='Id'
        b='Tiempo'        
        c='Humanos'
        d='Materiales'
        
        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Recursos.objects.filter(id_recursos__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Rec.html",data)

                elif b_ava==b:
                                            
                    uni=Recursos.objects.filter(Tiempo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Rec.html", data)
                                            
                elif b_ava==c:

                    uni=Recursos.objects.filter(Humanos__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Rec.html", data)
                
                elif b_ava==d:

                    uni=Recursos.objects.filter(Materiales__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    } 
                    return render(request, "asesor/base/t-Rec.html", data)
                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Recursos.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            } 
            return render(request, "asesor/base/t-Rec.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Re(request):

    data = {
        'form': RecursosForm(),
        'N':"Tabla Recursos",
        'P':"agregar_producto_Re" 

    }

    if request.method == 'POST':

        formulario = RecursosForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Rec')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Rec')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Re(request, id):

    producto = get_object_or_404(Recursos, id_recursos=id)

    data = {
        'form': RecursosForm(instance=producto),
        'N':"Tabla Recursos",
        'id':id,
        'h':producto,
        't':"modificar_producto_Re"         
    }
        
    if request.method == 'POST':
        formulario = RecursosForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Rec')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Rec')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Re(request, id):
    producto = get_object_or_404(Recursos, id_recursos=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Re"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Rec')
    return render(request, 'asesor/crud/delete.html', data)
#10Tabla Cursos Asesor
@login_required
def Tablas_Cu_As(request): 
    u="Parametrización"
    t="Tabla"
    uni=Curso_Asesor.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }
    return render(request, "asesor/base/t-Cur-As.html", data)
@login_required
def buscar_Cu_As(request):

        a='Id'
        b='Asesor'        
        c='Curso'
        d='Relación'
        e='Estudiante'

        u="Parametrización"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Curso_Asesor.objects.filter(id_curso_asesor__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }
                    return render(request, "asesor/base/t-Cur-As.html", {"uni_nombre":uni, "query":producto})

                elif b_ava==b:
                                            
                    uni=Curso_Asesor.objects.filter(Asesor__Nombres__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }
                    return render(request, "asesor/base/t-Cur-As.html", data)
                                            
                elif b_ava==c:

                    uni=Curso_Asesor.objects.filter(Curso__Tipo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }
                    return render(request, "asesor/base/t-Cur-As.html", data)
                
                elif b_ava==d:

                    uni=Curso_Asesor.objects.filter(Relacion__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }
                    return render(request, "asesor/base/t-Cur-As.html", data)
                
                elif b_ava==e:

                    uni=Curso_Asesor.objects.filter(Estudiante__Nombres__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }
                    return render(request, "asesor/base/t-Cur-As.html", data)
                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Curso_Asesor.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            }
            return render(request, "asesor/base/t-Cur-As.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Cu_As(request):

    data = {
        'form': Curso_AsesorForm(),
        'N':"Tabla Relación Curso-Asesor",
        'P':"agregar_producto_Cu_As"    
    }

    if request.method == 'POST':

        formulario = Curso_AsesorForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Cur-As')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Cur-As')   

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Cu_As(request, id):

    producto = get_object_or_404(Curso_Asesor, id_curso_asesor=id)

    data = {
        'form': Curso_AsesorForm(instance=producto),
        'N':"Tabla Relación Curso-Asesor",
        'id':id,
        'h':producto,
        't':"modificar_producto_Cu_As"     
    }
        
    if request.method == 'POST':
        formulario = Curso_AsesorForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Cur-As')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Cur-As')   


    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Cu_As(request, id):

    producto = get_object_or_404(Curso_Asesor, id_curso_asesor=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Cu_As"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Cur-As')
    return render(request, 'asesor/crud/delete.html', data)
#11Tabla Titulos
@login_required
def Tablas_Ti(request): 
    u="Mantenimiento de Código"
    t="Tabla"
    uni=Titulos.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    }  
    return render(request, "asesor/base/t-Ti.html", data)    
@login_required
def buscar_Ti(request):

        a='Id'
        b='Nombramiento'                
        c='Carrera'      
        
        u="Mantenimiento de Código"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Titulos.objects.filter(id_titulo__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Ti.html",data)

                elif b_ava==b:
                                            
                    uni=Titulos.objects.filter(Nombramiento__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Ti.html",data)
                                                                          

                elif b_ava==c:

                    uni=Titulos.objects.filter(Carrera__descripcion__icontains=producto)
                    data = {   
                        'uni_nombre':uni,
                        'heading': u,
                        'pageview': t 
                    }  
                    return render(request, "asesor/base/t-Ti.html", data)
                                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Titulos.objects.all()
            data = {   
                'uni_nombre':uni,
                'heading': u,
                'pageview': t 
            }  
            return render(request, "asesor/base/t-Ti.html", data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Ti(request):

    data = {
        'form': TitulosForm(),
        'N':"Tabla Titulos",
        'P':"agregar_producto_Ti" 
    }

    if request.method == 'POST':

        formulario = TitulosForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Ti')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Ti')   


    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Ti(request, id):

    producto = get_object_or_404(Titulos, id_titulo=id)

    data = {
        'form': TitulosForm(instance=producto),
        'N': "Tabla Titulos",
        'id':id,
        'h':producto,
        't':"modificar_producto_Ti"
    }
        
    if request.method == 'POST':
        formulario = TitulosForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('T-Ti')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('T-Ti')                     

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Ti(request, id):

    producto = get_object_or_404(Titulos, id_titulo=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Ti"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Ti')
    return render(request, 'asesor/crud/delete.html', data)
#Cronograma ---------------------------------------------------------------------

#12Tabla Cabecera Crono
@login_required
def Tablas_Cab_Cro(request): 
    u="Procesos"
    t="Tabla"
    uni=Cabecera_Crono.objects.all()
    data = {   
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    } 
    return render(request, "asesor/cronograma/cabecera_crono.html", data)
@login_required
def buscar_Cab_Cro(request):

        a='Id'
        b='Periodo'        
        c='Tiempo'
        d='Nombre relación Curso y Asesor'        
        e='Nombre'
        f='Dia de creación'
        g='Estado'

        u="Procesos"
        t="Tabla"        
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Cabecera_Crono.objects.filter(Id_Cabecera_Crono__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t } 
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)

                elif b_ava==b:
                                            
                    uni=Cabecera_Crono.objects.filter(Periodo__Tipo__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t } 
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)
                                            
                elif b_ava==c:

                    uni=Cabecera_Crono.objects.filter(Tiempo__Tiempo__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)
                
                elif b_ava==d:

                    uni=Cabecera_Crono.objects.filter(Relación__Relacion__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)
                
                elif b_ava==e:

                    uni=Cabecera_Crono.objects.filter(Nombre__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)

                elif b_ava==f:

                    uni=Cabecera_Crono.objects.filter(Dia_Creación__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/cabecera_crono.html", data)
                elif b_ava==g:
                    if producto=='Pendiente':                        
                        uni=Cabecera_Crono.objects.filter(Estado__icontains=1)
                        data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                        return render(request, "asesor/cronograma/cabecera_crono.html", data)
                    elif producto=='Aprobado':
                        uni=Cabecera_Crono.objects.filter(Estado__icontains=2)
                        data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                        return render(request, "asesor/cronograma/cabecera_crono.html", data)                    
                    else:
                        uni=Cabecera_Crono.objects.all()
                        data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                        return render(request, "asesor/cronograma/cabecera_crono.html",data)                
                else:
                    
                    mensaje="Fallo al realizar la búsqueda"
        else:

            uni=Cabecera_Crono.objects.all()
            data = {  'uni_nombre':uni,'heading': u,'pageview': t }
            return render(request, "asesor/cronograma/cabecera_crono.html",data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Cab_Cro(request):

    data = {
        'form': Cabecera_CronoForm(),
        'N':"Tabla Cabecera Cronograma",
        'P':"agregar_producto_Cab_Cro" 

    }

    if request.method == 'POST':

        formulario = Cabecera_CronoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('t-cab_crono')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('t-cab_crono')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_producto_Cab_Cro(request, id):

    producto = get_object_or_404(Cabecera_Crono, Id_Cabecera_Crono=id)

    data = {
        'form': Cabecera_CronoForm(instance=producto),
        'N':"Tabla Cronograma",
        'id':id,
        'h':producto, 
        't':"modificar_producto_Cab_Cro"
    }
        
    if request.method == 'POST':
        formulario = Cabecera_CronoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('t-cab_crono')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('t-cab_crono')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_producto_Cab_Cro(request, id):

    producto = get_object_or_404(Cabecera_Crono, Id_Cabecera_Crono=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Cab_Cro"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('t-cab_crono')
    return render(request, 'asesor/crud/delete.html', data)

#13Tabla Evento Crono
@login_required
def Tablas_Event_Crono(request): 

    u="Procesos"
    t="Tabla"      
    uni=Event.objects.all()
    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
    return render(request, "asesor/cronograma/evento_crono.html", data)
@login_required
def buscar_Event_Crono(request):

        a='Id'
        b='Nombre De la Cabecera del Cronograma'        
        c='Nombre del Evento'
        d='Descripción'
        e='Tiempo de Inicio'        
        f='Tiempo Fin'
        g='Dia de creación'

        u="Procesos"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>50:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Event.objects.filter(id__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)

                elif b_ava==b:
                                            
                    uni=Event.objects.filter(user__Nombre__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)
                                            
                elif b_ava==c:

                    uni=Event.objects.filter(title__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)
                
                elif b_ava==d:

                    uni=Event.objects.filter(description__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)
                
                elif b_ava==e:

                    uni=Event.objects.filter(start_time__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)

                elif b_ava==f:

                    uni=Event.objects.filter(end_time__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)
                
                elif b_ava==g:

                    uni=Event.objects.filter(created_date__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/evento_crono.html", data)
                

                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Event.objects.all()
            data = {  'uni_nombre':uni,'heading': u,'pageview': t }
            return render(request, "asesor/cronograma/evento_crono.html",data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_producto_Event_Crono(request):

    data = {
        'form': EventForm(),
        'N':"Tabla de Eventos",
        'P':"tablas_Event_Cro"        
    }

    if request.method == 'POST':

        formulario = EventForm(data=request.POST, files=request.FILES)
        
        if formulario.is_valid():
            formulario.save()            
            return redirect('t-evento_cro')
        else:
            messages.error(request, 'Error, evite repetir el nombre de las actividades')
            return redirect('t-evento_cro') 
                                  

    return render(request, 'asesor/crud/agregar_editar_evento_crono/agregar_Event_pop.html', data)
@login_required
def modificar_producto_Event_Crono(request, id, user):       
    producto = get_object_or_404(Event, id=id)      
    data = {
        'form': EventForm(instance=producto),   
        'N':"Tabla de Eventos",
        'id':id,
        'user':user,        
        'h':producto,
        'P':"tablas_Event_Cro" 
    }
        
    if request.method == 'POST':        
        formulario = EventForm(data=request.POST, instance=producto, files=request.FILES)              
        formulario2 = historiasForm(data=request.POST, files=request.FILES)              
        if formulario.is_valid():                               
            formulario.save()
            name = get_object_or_404(Cabecera_Crono, Nombre__icontains=user)                         
            if(name.Estado == 2):
                formulario2.save()
                return redirect('t-evento_cro')
            else:
                return redirect('t-evento_cro')            
        else:            
            messages.error(request, 'Error, evite repetir el nombre de las actividades')
            return redirect('t-evento_cro')             

    return render(request, 'asesor/crud/agregar_editar_evento_crono/editar_Event_pop.html', data)
@login_required
def eliminar_producto_Event_Crono(request, id):

    producto = get_object_or_404(Event, id=id)
    data = { 
        'a':id,
        'r':"eliminar_producto_Event_Crono"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('t-evento_cro')              
    return render(request, 'asesor/crud/delete.html', data)

#14 Tabla Observaciones Crono
@login_required
def Cab_crono_observaciones(request): 
    u="Procesos"
    t="Tabla"
    uni=Observaciones.objects.all()        
    data = {          
        'uni_nombre':uni,
        'heading': u,
        'pageview': t 
    } 
    return render(request, "asesor/cronograma/cabecera_crono_Obser.html", data)
@login_required
def buscar_Cab_Cro_ob(request):

        a='Id'
        b='Nombre'        
        c='Observaciones'
        d='Estado'        

        u="Procesos"
        t="Crud"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Observaciones.objects.filter(id_ob__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t } 
                    return render(request, "asesor/cronograma/cabecera_crono_Obser.html", data)

                elif b_ava==b:
                                            
                    uni=Observaciones.objects.filter(Nombre_Cabecera__Nombre__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t } 
                    return render(request, "asesor/cronograma/cabecera_crono_Obser.html", data)
                                            
                elif b_ava==c:

                    uni=Observaciones.objects.filter(Observaciones__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/cabecera_crono_Obser.html", data)
                
                elif b_ava==d:
                                            
                    uni=Observaciones.objects.filter(Nombre_Cabecera__Estado__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t } 
                    return render(request, "asesor/cronograma/cabecera_crono_Obser.html", data)
                                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Observaciones.objects.all()
            data = {  'uni_nombre':uni,'heading': u,'pageview': t }
            return render(request, "asesor/cronograma/cabecera_crono_Obser.html",data)
                

        return HttpResponse(mensaje)
@login_required
def agregar_Cro_ob(request):

    data = {
        'form': Cabecera_Crono_ObForm(),
        'N':"Tabla Observaciones Cronograma",
        'P':"agregar_Cro_ob" 
    }

    if request.method == 'POST':

        formulario = Cabecera_Crono_ObForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('t-cab_crono_observaciones')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('t-cab_crono_observaciones')

    return render(request, 'asesor/crud/agregar_p.html', data)
@login_required
def modificar_Cro_ob(request, id):

    producto = get_object_or_404(Observaciones, id_ob=id)

    data = {
        'form': Cabecera_Crono_ObForm(instance=producto),
        'N':"Tabla Observaciones Cronograma",
        'id':id,
        'h':producto, 
        't':"modificar_Cro_ob"
    }
        
    if request.method == 'POST':
        formulario = Cabecera_Crono_ObForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('t-cab_crono_observaciones')
        else:            
            messages.error(request, 'Error, porfavor repita el proceso q realizaba')
            return redirect('t-cab_crono_observaciones')

    return render(request, 'asesor/crud/editar_p.html', data)
@login_required
def eliminar_Cro_ob(request, id):
    producto = get_object_or_404(Observaciones, id_ob=id)
    data = { 
        'a':id,
        'r':"eliminar_Cro_ob"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('t-cab_crono_observaciones')
    return render(request, 'asesor/crud/delete.html', data)
@login_required
def SolicitarObserva(request):    
    uni=Observaciones.objects.all()    
    data = {                                
        'uni_nombre':uni,              
    }
            
    return render(request, 'asesor/cronograma/report_Obs.html', data)

#15Tabla Reporte crono
@login_required
def Tablas_Reporte_Crono(request): 
    u="Reportes"
    t="Tabla"
    uni=Cabecera_Crono.objects.all()
    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
    return render(request, "asesor/cronograma/reporte_crono.html", data)
@login_required
def SolicitarDatos(request, id):    
    uni=Event.objects.filter(user__Nombre__icontains=id)        
    data = {        
        'N':id,                
        'uni_nombre':uni,              
    }        
    return render(request, 'asesor/cronograma/report_pdf.html', data)
@login_required
def buscar_Reporte_Crono(request):

        a='Id'
        b='Relación del Curso y Asesor'
        c='Nombre De la Cabecera del Cronograma'             
        
        u="Reportes"
        t="Tabla"   

        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>30:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=Cabecera_Crono.objects.filter(Id_Cabecera_Crono__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/reporte_crono.html", data)

                elif b_ava==b:
                                            
                    uni=Cabecera_Crono.objects.filter(Relación__Relacion__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/reporte_crono.html",data)

                elif b_ava==c:
                                            
                    uni=Cabecera_Crono.objects.filter(Nombre__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/cronograma/reporte_crono.html", data)                
                
                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=Cabecera_Crono.objects.all()
            data = {  'uni_nombre':uni,'heading': u,'pageview': t }
            return render(request, "asesor/cronograma/reporte_crono.html",data)
                

        return HttpResponse(mensaje)

#Funciones del calendario

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month)
    return month
@login_required
def llamar_crono(request, id):                         
    h = get_object_or_404(Cabecera_Crono, Nombre=id)    
    mes=Calendar()            
    d = get_date(mes.Obten_mes())
    q = next_month(d)          
    t = prev_month(d)    
    cal = Calendar(d.year, d.month, h.Nombre)
    html_cal = cal.formatmonth(withyear=True)
    u="Calendario"
    g="Apps"  
    data = {   
        'P':h,                   
        'calendar':mark_safe(html_cal),
        'ant':t,
        'seg':q,
        'heading': u,
        'pageview': g 
    }    

    return render(request, 'asesor/cronograma/calendar.html', data)
@login_required
def nextM(request, id, p):   
    u="Calendario"
    g="Apps" 
    h = get_object_or_404(Cabecera_Crono, Nombre=id)  
    d = get_date(p)          
    cal = Calendar(d.year, d.month, h.Nombre)
    q = next_month(d)          
    t = prev_month(d)
    html_cal = cal.formatmonth(withyear=True)
    
    data = {   
        'P':h,                     
        'calendar':mark_safe(html_cal),
        'ant':t,
        'seg':q,
        'heading': u,
        'pageview': g
    }    

    return render(request, 'asesor/cronograma/calendar.html', data)
@login_required
def event_details(request, event_id):    
    event = Event.objects.get(id=event_id)
    context = {
        'id':event_id,
        'event': event,        
    }
    #return context
    return render(request, 'asesor/cronograma/event-details.html', context)
    
#Historia de Cambios
@login_required
def Tabla_Historias(request): 

    u="Historias"
    t="Tabla"      
    uni=registro_historicos.objects.all()
    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
    return render(request, "asesor/base/t-historias.html", data)
@login_required
def B_Tabla_Historias(request):

        a='Id'
        b='Nombre De la Cabecera del Cronograma'        
        c='Nombre del Evento'
        d='Descripción'
        e='Tiempo de Inicio'        
        f='Tiempo Fin'
        g='Dia de creación'

        u="Historias"
        t="Tabla"
        
        if request.GET["prd"]:
            
            producto=request.GET["prd"]
            b_ava=request.GET["opcion"]


            if len(producto)>50:

                mensaje="Texto de busqueda demasiado largo"

            else:

                if b_ava==a:

                    uni=registro_historicos.objects.filter(id__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)

                elif b_ava==b:
                                            
                    uni=registro_historicos.objects.filter(user__Nombre__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)
                                            
                elif b_ava==c:

                    uni=registro_historicos.objects.filter(title__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)
                
                elif b_ava==d:

                    uni=registro_historicos.objects.filter(description__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)
                
                elif b_ava==e:

                    uni=registro_historicos.objects.filter(start_time__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)

                elif b_ava==f:

                    uni=registro_historicos.objects.filter(end_time__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)
                
                elif b_ava==g:

                    uni=registro_historicos.objects.filter(created_date__icontains=producto)
                    data = {  'uni_nombre':uni,'heading': u,'pageview': t }
                    return render(request, "asesor/base/t-historias.html", data)
                

                else:

                    mensaje="Fallo al realizar la búsqueda"

        else:

            uni=registro_historicos.objects.all()
            data = {  'uni_nombre':uni,'heading': u,'pageview': t }
            return render(request, "asesor/base/t-historias.html", data)
            
                

        return HttpResponse(mensaje)
@login_required
def eliminar_Historias(request, id):

    producto = get_object_or_404(registro_historicos, id=id)
    data = { 
        'a':id,
        'r':"eliminar_Historias"           
    }
    if request.method == 'POST':
        producto.delete()
        return redirect('T-Historias')
    return render(request, 'asesor/crud/delete.html', data)
@login_required
def CompararDatos(request, id, user):
        
    uni=registro_historicos.objects.filter(user_id=id)
    #uni2=Event.objects.filter(user__Nombre__icontains=user)
    data = {  'N':user, 'uni_nombre':uni,  }
    return render(request, "asesor/cronograma/report_historias.html", data)    

#Seguimiento Docente
@login_required
def estadistico(request): 


    u="Reporte Estadistico"
    t="Tipo Pastel"        
    opcion2 = Cabecera_Crono.objects.filter(Estado__icontains=2)
    opcion1 = Cabecera_Crono.objects.filter(Estado__icontains=1)
    
    ase=Asesor.objects.all()
    cur=Cursos.objects.all()
    doc=Docentes.objects.all()    
        
    data = {           
        'heading': u,
        'pageview': t,        
        't1':ase.count,
        't2':cur.count,
        't3':doc.count,        
        'sinaprob':opcion1.count,
        'aprob':opcion2.count,        
    }   
    return render(request, "asesor/base/t-estadistico.html", data)
@login_required
def api_curso(request):
    u="Seguimiento Docente"
    t="Cursos"    
    apiBase="http://academyec.com/moodle/webservice/rest/server.php"
    params={"wstoken":TOKEN_MOODLE,
            "wsfunction":"core_course_get_courses",
            "moodlewsrestformat":"json",                                    
            }    
    context={} 
    try:
        response=requests.post(apiBase, params)
        if response.status_code==400:
            return render(request,'lista_cursos.html',context={"context":"Bad request",'heading': u,'pageview': t,})
        if response:
            r=response.json()                       
            context={"context":r,'heading': u,'pageview': t, }  
            for y in r:
                timestamp = datetime.fromtimestamp(y["startdate"])                
                y["startdate"]=timestamp.strftime('%Y-%m-%d')
                 
            for v in r:                
                timestamp = datetime.fromtimestamp(v["enddate"])                
                v["enddate"]=timestamp.strftime('%Y-%m-%d') 

            #lista [] se accede a elementos con indice numerico(0,1,2)
            #diccionario {} se accede con cadena de texto como palabra clave "courses"

    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/lista_cursos.html',context)
@login_required
def listado_estudiante(request, id, nombre):   
    nombre_curso=nombre         
    apiBase="http://academyec.com/moodle/webservice/rest/server.php"
    params={"wstoken":TOKEN_MOODLE,
            "wsfunction":"gradereport_user_get_grade_items",
            "moodlewsrestformat":"json",
            "courseid":id                                   
            }
    context={} 
    try:
        response=requests.post(apiBase, params)
        if response.status_code==400:
            return render(request,'lista_Estudiantes.html',context={"context":"Bad request"})
        if response:
            r=response.json()["usergrades"]                       
            context={"context":r,'nombre':nombre_curso}                        

            #lista [] se accede a elementos con indice numerico(0,1,2)
            #diccionario {} se accede con cadena de texto como palabra clave "courses"

    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/lista_Estudiantes.html',context)
@login_required
def actividades_user(request, id, nombre, idest):   
    nombre_Estudiante=nombre         
    apiBase="http://academyec.com/moodle/webservice/rest/server.php"
    params={"wstoken":TOKEN_MOODLE,
            "wsfunction":"gradereport_user_get_grade_items",
            "moodlewsrestformat":"json",
            "courseid":id,
            "userid":idest            
            }
    context={} 
    try:
        response=requests.post(apiBase, params)
        if response.status_code==400:
            return render(request,'act_pdf.html',context={"context":"Bad request"})
        if response:
            r=response.json()["usergrades"][0]["gradeitems"]
            #print(type(r["usergrades"][0]["gradeitems"]))                       
            context={"context":r,'nombre':nombre_Estudiante}                                    

            #lista [] se accede a elementos con indice numerico(0,1,2)
            #diccionario {} se accede con cadena de texto como palabra clave "courses"

    except Exception as e:
        print(e)
    return render(request,'asesor/seguimiento_docente/act_pdf.html',context)


