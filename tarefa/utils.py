from core.models import *
from tarefa.models import Dispositivo, Atuador_troca_estado, Atuador_boolean
from tarefa import task as celery

def tarefas(task, proxy_pk):
    tipo = 0
    tipo_anterior=0
    tasks = []
    tarefas = task.split(';')
    print(tarefas)
    count = 0
    for subtarefa in tarefas:#split do comando inteiro
        if subtarefa != '':
            tarefa = subtarefa.split(':')
            t = Task()
            t.comando = subtarefa
            if tarefa[0] == 'if_sensor_string':
                tipo_anterior=tipo
                tipo=1
                t = If_sensor_string()
                t.comando = subtarefa
                t.condicao=tarefa[1]
                try:
                    t.valor = tarefa[2]
                except:
                    t.valor = None

            elif tarefa[0] == 'if_sensor_numero':
                tipo_anterior = tipo
                tipo = 2
                t = If_sensor_numero()
                t.comando = subtarefa
                t.condicao = tarefa[1]
                try:
                    t.valor = int(tarefa[2])
                except:
                    t.valor = None

            elif tarefa[0] == 'atuador_troca_estado':
                tipo_anterior = tipo
                tipo = 3
                t = Atuador_troca_estado()
                t.comando = subtarefa
                dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
                t.atuador = dis

            elif tarefa[0] == 'atuador_boolean':
                tipo_anterior = tipo
                tipo = 4
                t = Atuador_boolean()
                dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
                t.comando = subtarefa
                t.atuador = dis
                try:
                    t.estado = bool(tarefa[2])
                except:
                    t.estado = None

            elif tarefa[0] == 'if_sensor_boolena':
                tipo_anterior = tipo
                tipo = 5
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
                create_celer_task(anterior.pk, tipo_anterior, proxy_pk)
                tasks.insert(count-1, anterior)
                tasks.insert(count,t)
            else:
                create_celer_task(t.pk, tipo, proxy_pk)
                tasks.insert(count, t)
                t.save()
            count=count+1
    return tasks

def create_celer_task(task_pk, tipo, proxy_pk):
    if tipo == 1:
        celery.create_if_sensor_string.delay(task_pk, proxy_pk)
    elif tipo == 2:
        celery.create_if_sensor_numero.delay(task_pk, proxy_pk)
    elif tipo == 3:
        celery.create_atuador_troca_estado.delay(task_pk, proxy_pk)
    elif tipo == 4:
        celery.create_atuador_boolean.delay(task_pk, proxy_pk)
    elif tipo == 5:
        celery.create_if_sensor_boolena.delay(task_pk, proxy_pk)
    else:
        print('passei')
        celery.create_task.delay(task_pk, proxy_pk)