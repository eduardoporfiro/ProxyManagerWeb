from django.contrib import admin
from .models import *

admin.site.register(Celery)
admin.site.register(Task)
admin.site.register(If_sensor_numero)
admin.site.register(If_sensor_string)
admin.site.register(If_sensor_dadosensor)
admin.site.register(Atuador_troca_estado)
admin.site.register(Atuador_boolean)
