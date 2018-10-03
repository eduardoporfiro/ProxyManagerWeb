import django_tables2 as tables
from .models import Mqtt
from django_tables2.utils import A

class MqttTable(tables.Table):
    Editar = tables.LinkColumn(
        'block:edit_mqtt',
        args=[A('pk')],
        empty_values=list(),
        text='Editar')
    Dispositivo = tables.LinkColumn(
        'tarefa:add_dispositivos',
        args=[A('pk')],
        empty_values=list(),
        text='Dispositivo')
    Deletar = tables.LinkColumn(
        'block:delete_mqtt',
        args=[A('pk')],
        empty_values=list(),
        text='Excluir')

    class Meta:
        model = Mqtt
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id','topico', 'QoS','RC')
        fields = ('id','topico', 'QoS','RC')
        empty_text = "Sem MQTT cadastrado para o Broker"