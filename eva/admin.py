from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from eva.models import *

admin.site.register(Materia)
admin.site.register(Ciclo)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Parametro)
admin.site.register(ParametrosGeneral)
admin.site.register(AreasConocimiento)


@admin.register(Pregunta)
class PreguntaAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'category', 'type')
