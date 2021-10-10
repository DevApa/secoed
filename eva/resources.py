from import_export import resources
from eva.models import Pregunta


class PreguntasResources(resources.ModelResource):
    class Meta:
        model = Pregunta
        exclude = ('id',)
        fields = ('title', 'description', 'category', 'type')
