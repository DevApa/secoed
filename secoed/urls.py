from django.contrib import admin
from django.urls import path

import secoed.views
from secoed import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from secoed.views import Error404View
from secoed.settings import DEBUG
from django.conf.urls import url
from django.views.static import serve
from django.conf.urls import handler500

urlpatterns = [

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # Inicio de sesión
    path('jsnCountLogin', views.AjaxEvent.jsnCountLogin, name="jsnCountLogin"),

    path(r'admin/', admin.site.urls),

    # Dashboards View
    path(r'', views.DashboardView.as_view(), name='dashboard'),

    # Accounts
    path('accounts/login/', views.DashboardView.as_view(), name='dashboard'),

    # Layouts
    path(r'layout/', include('layout.urls')),

    # Authencation
    path(r'authentication/', include('authentication.urls')),

    # Configuraciones
    path(r'conf/', include('conf.urls')),

    # Autoevaluacion
    path('eva/', include('eva.urls')),

    # mis url de mi asesor
    path('asesor/', include('asesor.urls')),
    # Components
    path('components/', include('components.urls')),

    # url de cursos
    path(r'cursos/', include('cursos.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404View.as_view()
handler500 = secoed.views.error_500
