from core.models import *
from tarefa.models import Dispositivo, Atuador_troca_estado, Atuador_boolean
def tarefas(task):
    tasks = []
    tarefas = task.split(';')
    count = 0
    tarefas.pop()
    for subtarefa in tarefas:#split do comando inteiro
        tarefa = subtarefa.split(':')
        t = Task()
        t.comando = subtarefa
        if tarefa[0] == 'if_sensor_string':
            t = If_sensor_string()
            t.comando = subtarefa
            t.condicao=tarefa[1]
            try:
                t.valor = tarefa[2]
            except:
                t.valor = None

        elif tarefa[0] == 'if_sensor_numero':
            t = If_sensor_numero()
            t.comando = subtarefa
            t.condicao = tarefa[1]
            try:
                t.valor = int(tarefa[2])
            except:
                t.valor = None

        elif tarefa[0] == 'atuador_troca_estado':
            t = Atuador_troca_estado()
            t.comando = subtarefa
            dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
            t.atuador = dis

        elif tarefa[0] == 'atuador_boolean':
            t = Atuador_boolean()
            dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
            t.comando = subtarefa
            t.atuador = dis
            try:
                t.estado = bool(tarefa[2])
            except:
                t.estado = None

        elif tarefa[0] == 'if_sensor_boolena':
            t = If_sensor_boolean()
            t.comando = subtarefa
            t.condicao = tarefa[1]
            try:
                t.valor = bool(tarefa[2])
            except:
                t.valor = None

        elif tarefa[0] == 'save_database':
            t.tipo = 0

        elif tarefa[0] == 'dado_sensor_numero':
            t.tipo = 1

        elif tarefa[0] == 'dado_sensor_string':
            t.tipo = 2

        elif tarefa[0] == 'dados_sensor_media':
            t.tipo = 3

        elif tarefa[0] == 'dado_sensor_min':
            t.tipo = 4

        elif tarefa[0] == 'dado_sensor_max':
            t.tipo = 5

        if count != 0:
            anterior = tasks.pop()
            t.task_anterior = anterior
            t.save()
            anterior.task_sucessor = t
            anterior.save()
            tasks.insert(count-1, anterior)
            tasks.insert(count,t)
        else:
            tasks.insert(count, t)
            t.save()
        count=count+1
    return tasks