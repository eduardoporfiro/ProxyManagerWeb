import django_tables2 as tables
from .models import Dispositivo, Dado
from django_tables2.utils import A

class DispositivoTable(tables.Table):
    TEMPLATE = '''
    {% if record.tipo == 0 %}
        <strong>Sem Job</strong>
    {% else %}
        <a href="{% url 'tarefa:job' record.pk %}">Job</a>
    {% endif %}
    '''
    TEMPLATE_DADO = '''
    {% if record.tipo == 0 %}
        <strong>Sem Dado</strong>
    {% else %}
        <a href="{% url 'tarefa:load_dado' record.pk %}">Dado</a>
    {% endif %}
    '''
    editar = tables.LinkColumn('tarefa:edit_dispositivo',
                               args=[A('pk')],
                               empty_values=list(),
                               text='Editar')
    deletar = tables.LinkColumn('tarefa:delete_dispositivo',
                                args=[A('pk')],
                                empty_values=list(),
                                text='Excluir')
    Job = tables.TemplateColumn(TEMPLATE)
    Dado = tables.TemplateColumn(TEMPLATE_DADO)
    class Meta:
        model = Dispositivo
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id','nome','mqtt', 'tipo', 'editar')
        fields = ('id','nome','mqtt', 'tipo', 'editar')
        empty_text = "Sem Dispositivos cadastrados para o Proxy"


class DadoTable(tables.Table):
    class Meta:
        model = Dado
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id', 'QoS', 'valor_char', 'valor_int', 'date')
        fields = ('id', 'QoS', 'valor_char', 'valor_int', 'date')
        empty_text = "Sem dados para este dispositivo"