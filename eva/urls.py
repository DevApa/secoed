from django.conf.urls import url

from eva.views.cursos.views import CursosEva
from eva.views.evaluaciones.views import *
from eva.views.reportes.views import ProcessResultEvaluations
from eva.views.tipo.views import *
from eva.views.docente.views import *
from eva.views.ciclo.views import *
from eva.views.materia.views import *
from eva.views.categoria.views import *
from eva.views.areas.views import *
from eva.views.parametro.views import *
from eva.views.parametros_generales.views import *
from eva.views.preguntas.views import *


app_name = 'eva'

urlpatterns = [
    url(r'^docente/lista/', login_required(TeacherListView.as_view()), name='list-teacher'),
    url(r'^docente/coevaluadores/lista/', TeacherCoevaluatorListView.as_view(), name='list-coevaluators'),
    # TYPE routes
    url(r'^tipo/lista/', login_required(TypeListView.as_view()), name='list-type'),
    url(r'^tipo/crear/', login_required(TypeCreateView.as_view()), name='create-type'),
    url(r'^tipo/editar/(?P<pk>\d+)/$', login_required(TypeUpdateView.as_view()), name='update-type'),
    url(r'^tipo/eliminar/(?P<pk>\d+)/$', login_required(TypeDeleteView.as_view()), name='delete-type'),
    # CYCLE routes
    url(r'^ciclo/lista/', login_required(CycleListView.as_view()), name='list-cycle'),
    url(r'^ciclo/crear/', login_required(CycleCreateView.as_view()), name='create-cycle'),
    url(r'^ciclo/editar/(?P<pk>\d+)/$', login_required(CycleUpdateView.as_view()), name='update-cycle'),
    url(r'^ciclo/eliminar/(?P<pk>\d+)/$', login_required(CycleDeleteView.as_view()), name='delete-cycle'),
    # MATTER routes
    url(r'^materia/lista/', login_required(MatterListView.as_view()), name='list-matter'),
    url(r'^materia/crear/', login_required(MatterCreateView.as_view()), name='create-matter'),
    url(r'^materia/editar/(?P<pk>\d+)/$', login_required(MatterUpdateView.as_view()), name='update-matter'),
    url(r'^materia/eliminar/(?P<pk>\d+)/$', login_required(MatterDeleteView.as_view()), name='delete-matter'),
    # CATEGORY routes
    url(r'^categoria/lista/', login_required(CategoryListView.as_view()), name='list-category'),
    url(r'^categoria/crear/', login_required(CategoryCreateView.as_view()), name='create-category'),
    url(r'^categoria/editar/(?P<pk>\d+)/$', login_required(CategoryUpdateView.as_view()), name='update-category'),
    url(r'^categoria/eliminar/(?P<pk>\d+)/$', login_required(CategoryDeleteView.as_view()), name='delete-category'),
    # Type routes
    url(r'^area/lista/', login_required(KnowledgeAreasListView.as_view()), name='list-area'),
    url(r'^area/crear/', login_required(KnowledgeAreasCreateView.as_view()), name='create-area'),
    url(r'^area/editar/(?P<pk>\d+)/$', login_required(KnowledgeAreasUpdateView.as_view()), name='update-area'),
    url(r'^area/eliminar/(?P<pk>\d+)/$', login_required(KnowledgeAreasDeleteView.as_view()), name='delete-area'),
    # Type routes
    url(r'^parametro/lista/', login_required(ParameterListView.as_view()), name='list-parameter'),
    url(r'^parametro/crear/', login_required(ParameterCreateView.as_view()), name='create-parameter'),
    url(r'^parametro/editar/(?P<pk>\d+)/$', login_required(ParameterUpdateView.as_view()), name='update-parameter'),
    url(r'^parametro/eliminar/(?P<pk>\d+)/$', login_required(ParameterDeleteView.as_view()), name='delete-parameter'),
    # Type routes
    url(r'^parametro_grl/values/lista/', login_required(ParameterGrlListView.as_view()), name='list-parameter-grl'),
    url(r'^parametro_grl/values/crear/', login_required(ParameterGrlCreateView.as_view()), name='create-parameter-grl'),
    url(r'^parametro_grl/values/editar/(?P<pk>\d+)/$', login_required(ParameterGrlUpdateView.as_view()),
        name='update-parameter-grl'),
    url(r'^parametro_grl/values/eliminar/(?P<pk>\d+)/$', login_required(ParameterGrlDeleteView.as_view()),
        name='delete-parameter-grl'),
    # Questions routes
    url(r'^pregunta/lista/', login_required(QuestionsListView.as_view()), name='list-questions'),
    url(r'^pregunta/autoevaluacion/', login_required(PreguntasAutoView.as_view()), name='auto-questions'),
    url(r'^pregunta/coevaluacion/', login_required(PreguntasCoeView.as_view()), name='coe-questions'),
    url(r'^pregunta/crear/', login_required(QuestionsCreateView.as_view()), name='create-questions'),
    url(r'^pregunta/editar/(?P<pk>\d+)/$', login_required(QuestionsUpdateView.as_view()), name='update-questions'),
    url(r'^pregunta/eliminar/(?P<pk>\d+)/$', login_required(QuestionsDeleteView.as_view()), name='delete-questions'),
    # eva
    url(r'^evaluacion/lista/', login_required(TeachersPendingEvaluationList.as_view()), name='list-coevaluar'),
    url(r'^evaluacion/autoevaluar', login_required(AutoEvaluacionCreateView.as_view()), name='create-auto-evaluation'),
    url(r'^evaluacion/co-evaluacion', login_required(CoevaluacionCreateView.as_view()), name='create-coevaluation'),
    # Reports Auto y Co Evaluation
    url(r'^evaluacion/reportes', login_required(ProcessResultEvaluations.as_view()), name='report-evaluation'),
    # Cursos routes
    url(r'^cursos/lista', login_required(CursosEva.as_view()), name='cursos-evaluation'),
]

