import django_tables2 as tables
from .models import Dispositivo
from django_tables2.utils import A

class DispositivoTable(tables.Table):
    TEMPLATE = '''
    {% if record.tipo == 0 %}
        <strong>Sem Job</strong>
    {% else %}
        <a href="{% url 'tarefa:job' record.pk %}">Job</a>
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
    class Meta:
        model = Dispositivo
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id','nome','mqtt', 'tipo', 'editar')
        fields = ('id','nome','mqtt', 'tipo', 'editar')
        empty_text = "Sem Sensores cadastrado para o Proxy"