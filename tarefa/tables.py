import django_tables2 as tables
from .models import Dispositivo
from django_tables2.utils import A

class DispositivoTable(tables.Table):
    editar = tables.LinkColumn('tarefa:edit_dispositivo',
                               args=[A('pk')],
                               empty_values=list(),
                               text='Editar')
    deletar = tables.LinkColumn('tarefa:delete_dispositivo',
                                args=[A('pk')],
                                empty_values=list(),
                                text='Excluir')
    job = tables.LinkColumn('tarefa:job',
                                args=[A('pk')],
                                empty_values=list(),
                                text='Job')
    class Meta:
        model = Dispositivo
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('id','nome','mqtt', 'tipo', 'editar')
        fields = ('id','nome','mqtt', 'tipo', 'editar')
        empty_text = "Sem Sensores cadastrado para o Proxy"