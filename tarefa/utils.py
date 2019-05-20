from tarefa.models import *
from block.models import Proxy
from tarefa import task as celery


def tarefas(task, proxy_pk):
    proxy = Proxy.objects.get(pk=proxy_pk)
    tasks = []
    celery = []
    var_else = False
    count_else = 0
    object_else = 0
    elsecount = 0
    tarefas = task.split(';')
    print(tarefas)
    count = 0
    for subtarefa in tarefas:#split do comando inteiro
        if subtarefa != '':
            tipo = 0
            tarefa = subtarefa.split(':')
            t = Task()
            t.comando = subtarefa
            if 'if_sensor_string' in tarefa[0]:
                tipo=1
                t = If_sensor_string()
                t.tipo = Settings.objects.get(task_tipo=6)
                t.comando = subtarefa
                t.condicao=tarefa[1]
                try:
                    t.valor = tarefa[2]
                except:
                    t.valor = None

            elif 'if_sensor_numero' in tarefa[0]:
                tipo = 2
                t = If_sensor_numero()
                t.tipo = Settings.objects.get(task_tipo=7)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                try:
                    t.valor = int(tarefa[2])
                except:
                    t.valor = None

            elif 'atuador_troca_estado' in tarefa[0]:
                tipo = 3
                t = Atuador_troca_estado()
                t.tipo = Settings.objects.get(task_tipo=10)
                t.comando = subtarefa
                dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
                t.atuador = dis

            elif 'atuador_boolean' in tarefa[0]:
                tipo = 4
                t = Atuador_boolean()
                t.tipo = Settings.objects.get(task_tipo=11)
                dis = Dispositivo.objects.filter(pk=tarefa[1]).get()
                t.comando = subtarefa
                t.atuador = dis
                try:
                    t.estado = bool(tarefa[2])
                except:
                    t.estado = None

            elif 'if_sensor_boolena' in tarefa[0]:
                tipo = 5
                t = If_sensor_boolean()
                t.tipo = Settings.objects.get(task_tipo=8)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                try:
                    t.valor = bool(tarefa[2])
                except:
                    t.valor = None
            elif 'if_sensor_dadosensor' in tarefa[0]:
                tipo = 6
                t = If_sensor_dadosensor()
                t.tipo = Settings.objects.get(task_tipo=9)
                t.comando = subtarefa
                t.condicao = tarefa[1]

            elif 'if_else_sensor_boolena' in tarefa[0]:
                tipo = 13
                t = If_else_sensor_boolean()
                t.tipo = Settings.objects.get(task_tipo=13)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                if count != 0:
                    object_else = count - 1
                else:
                    object_else = count
                try:
                    t.valor = bool(tarefa[2])
                except:
                    t.valor = None

            elif 'if_else_sensor_dadosensor' in tarefa[0]:
                tipo = 14
                t = If_sensor_dadosensor()
                t.tipo = Settings.objects.get(task_tipo=14)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                if count != 0:
                    object_else = count - 1
                else:
                    object_else = count

            elif 'if_else_sensor_number' in tarefa[0]:
                tipo = 15
                t = If_else_sensor_numero()
                t.tipo = Settings.objects.get(task_tipo=15)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                if count != 0:
                    object_else = count - 1
                else:
                    object_else = count
                try:
                    t.valor = int(tarefa[2])
                except:
                    t.valor = None

            elif 'if_else_sensor_string' in tarefa[0]:
                tipo = 12
                t = If_else_sensor_string()
                t.tipo = Settings.objects.get(task_tipo=12)
                t.comando = subtarefa
                t.condicao = tarefa[1]
                if count != 0:
                    object_else = count - 1
                else:
                    object_else = count
                try:
                    t.valor = tarefa[2]
                except:
                    t.valor = None
            elif 'else' in tarefa[0]:
                tipo = 22
                var_else = True
                count_else = count
                elsecount = elsecount + 1

            elif 'save_database' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=0)

            elif 'dado_sensor_numero' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=1)

            elif 'dado_sensor_string' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=2)

            elif 'dados_sensor_media' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=3)

            elif 'dado_sensor_min' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=4)

            elif 'dado_sensor_max' in tarefa[0]:
                t.tipo = Settings.objects.get(task_tipo=5)

            if count != 0 and var_else is False:
                anterior = tasks.pop()
                t.task_anterior = anterior
                t.proxy = proxy
                t.save()
                anterior.task_sucessor = t
                anterior.save()
                tasks.insert(count-1, anterior)
                tasks.insert(count, t)
                celery.insert(count, {tipo: t})
                count = count + 1

            elif count != count_else and var_else is True:
                taskelse = tasks[object_else]
                t.task_anterior = taskelse
                t.proxy = proxy
                t.save()
                taskelse.elsetask = t
                taskelse.save()
                tasks[object_else] = taskelse
                tasks.insert(count, t)
                var_else = False
                celery.insert(count, {tipo: t})
                count = count + 1

            elif count == 0 and var_else is False:
                tasks.insert(count, t)
                t.proxy = proxy
                t.save()
                celery.insert(count, {tipo: t})
                count = count + 1
            else:
                count = count + 1

    for task in celery:
        for key in task.keys():
            create_celery_task(task.get(key).pk, key, proxy_pk)

        for key in task.keys():
            update_celery_task(task.get(key).pk, key, proxy_pk)

    return tasks


def create_celery_task(task_pk, tipo, proxy_pk):
    if tipo == 1:
        celery.create_if_sensor_string.delay(task_pk, proxy_pk)
    elif tipo == 2:
        celery.create_if_sensor_numero.delay(task_pk, proxy_pk)
    elif tipo == 3:
        celery.create_atuador_troca_estado.delay(task_pk, proxy_pk)
    elif tipo == 4:
        celery.create_atuador_boolean.delay(task_pk, proxy_pk)
    elif tipo == 5:
        celery.create_if_sensor_boolean.delay(task_pk, proxy_pk)
    elif tipo == 6:
        celery.create_if_sensor_dadosensor.delay(task_pk, proxy_pk)
    elif tipo == 12:
        celery.create_if_else_sensor_string.delay(task_pk, proxy_pk)
    elif tipo == 13:
        celery.create_if_else_sensor_boolean.delay(task_pk, proxy_pk)
    elif tipo == 14:
        celery.create_if_else_sensor_dadosensor.delay(task_pk, proxy_pk)
    elif tipo == 15:
        celery.create_if_else_sensor_numero.delay(task_pk, proxy_pk)
    else:
        celery.create_task.delay(task_pk, proxy_pk)


def update_celery_task(task_pk, tipo, proxy_pk):
    if tipo == 1:
        celery.edit_if_sensor_string.delay(task_pk, proxy_pk)
    elif tipo == 2:
        celery.edit_if_sensor_numero.delay(task_pk, proxy_pk)
    elif tipo == 3:
        celery.edit_atuador_troca_estado.delay(task_pk, proxy_pk)
    elif tipo == 4:
        celery.edit_atuador_boolean.delay(task_pk, proxy_pk)
    elif tipo == 5:
        celery.edit_if_sensor_boolean.delay(task_pk, proxy_pk)
    elif tipo == 6:
        celery.edit_if_sensor_dadosensor.delay(task_pk, proxy_pk)
    elif tipo == 12:
        celery.edit_if_else_sensor_string.delay(task_pk, proxy_pk)
    elif tipo == 13:
        celery.edit_if_else_sensor_boolean.delay(task_pk, proxy_pk)
    elif tipo == 14:
        celery.edit_if_else_sensor_dadosensor.delay(task_pk, proxy_pk)
    elif tipo == 15:
        celery.edit_if_else_sensor_numero.delay(task_pk, proxy_pk)
    else:
        celery.edit_task.delay(task_pk, proxy_pk)
