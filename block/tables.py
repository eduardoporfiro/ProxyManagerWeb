import django_tables2 as tables
from .models import Mqtt
from django_tables2.utils import A

class MqttTable(tables.Table):
    editar = tables.LinkColumn('block:edit_mqtt', args=[A('pk')], empty_values=list(),text='Editar')
    editarDispo = tables.LinkColumn('tarefa:add_dispositivos', args=[A('pk')], empty_values=list(), text='Dispositivo')
    class Meta:
        model = Mqtt
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id','topico', 'QoS','RC')
        fields = ('id','topico', 'QoS','RC', 'editar', 'editarDispo')
        empty_text = "Sem MQTT cadastrado para o Broker"