from django.contrib import admin
from tarefa.models import Dispositivo,Dado, Job, Atuador_troca_estado,Atuador_boolean
admin.site.register(Dispositivo)
admin.site.register(Dado)
admin.site.register(Job)
admin.site.register(Atuador_troca_estado)
admin.site.register(Atuador_boolean)