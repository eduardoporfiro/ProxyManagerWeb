from import_export import resources
from .models import Dado

class DadoResource(resources.ModelResource):
    class Meta:
        model = Dado