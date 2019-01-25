from django.contrib import admin
from tarefa.models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'tipo']

def export_as_json(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
export_as_json.short_description = "Exportar para Json"

@admin.register(Dado)
class DadoAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    search_fields = ['QoS', 'valor_char', 'valor_int']
    list_display = ('QoS', 'valor_char', 'valor_int')
    list_filter = ('QoS', 'sensor', 'valor_char')
    list_per_page = 20
    actions = [export_as_json]

admin.site.register(Job)
admin.site.register(Atuador_troca_estado)
admin.site.register(Atuador_boolean)
admin.site.register(Task)
admin.site.register(If_sensor_numero)
admin.site.register(If_sensor_string)
admin.site.register(If_sensor_dadosensor)
admin.site.register(If_sensor_boolean)
admin.site.register(Settings)
admin.site.register(If_else_sensor_string)
admin.site.register(If_else_sensor_numero)
admin.site.register(If_else_sensor_boolean)
admin.site.register(If_else_sensor_dadosensor)
