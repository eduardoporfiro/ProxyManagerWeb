from proxy_manager_web.celery import app
from block.models import Proxy
from tarefa.models import *
from core.models import Celery
import requests
import json


@app.task
def create_dispo(dispo_pk):
    dispo = Dispositivo.objects.get(pk=dispo_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_dispo', task='')
    url = get_url(dispo.mqtt.proxy.url)
    url += '/api/dispositivo/'
    head = {'Authorization': 'token {}'.format(dispo.mqtt.proxy.token)}

    data = {}
    data['nome']=dispo.nome
    data['tipo'] = dispo.tipo
    data['is_int']=dispo.is_int
    data['mqtt']=dispo.mqtt.proxy_alt_id
    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            dispo.proxy_alt_id=jsondis['id']
            dispo.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            print(str(response.text))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_dispo', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_dispo(dispo_pk):
    dispo = Dispositivo.objects.get(pk=dispo_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_dispo', task='')
    url = get_url(dispo.mqtt.proxy.url)
    url += '/api/dispositivo/'
    head = {'Authorization': 'token {}'.format(dispo.mqtt.proxy.token)}

    data = {}
    data['nome'] = dispo.nome
    data['tipo'] = dispo.tipo
    data['is_int'] = dispo.is_int
    data['mqtt'] = dispo.mqtt.proxy_alt_id
    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu e Update'
            celery.save()
        else:
            celery.desc = 'Update não foi completo'
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:edit_dispo', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def delete_dispo(dispo_pk):
    dispo = Dispositivo.objects.get(pk=dispo_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:delete_dispo', task='')
    url = get_url(dispo.mqtt.proxy.url)
    url += '/api/dispositivo/'
    head = {'Authorization': 'token {}'.format(dispo.mqtt.proxy.token)}

    try:
        response = requests.delete(url, headers=head)
        if response.status_code == 204:
            celery.desc = 'Respondeu e delete'
            celery.save()
        else:
            celery.desc = 'delete não foi completo'
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:delete_dispo', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_job(job_pk):
    job = Job.objects.get(pk=job_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_job', task='')
    url = get_url(job.dispositivo.mqtt.proxy.url)
    url += '/api/job/'
    head = {'Authorization': 'token {}'.format(job.dispositivo.mqtt.proxy.token)}

    data = {}
    data['dispositivo'] = job.dispositivo.proxy_alt_id
    data['workspace'] = job.workspace
    try:
        data['firs_task'] = job.firs_task.proxy_alt_id
    except:
        pass
    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            job.proxy_alt_id = jsondis['id']
            job.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            print(str(response.text))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()
            create_job(job_pk)

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_job', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_job(job_pk):
    job = Job.objects.get(pk=job_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_job', task='')
    url = get_url(job.dispositivo.mqtt.proxy.url)
    url += '/api/{}/jobUpdate/'.format(job.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(job.dispositivo.mqtt.proxy.token)}

    data = {}
    data['dispositivo'] = job.dispositivo.proxy_alt_id
    data['workspace'] = job.workspace
    try:
        data['firs_task'] = job.firs_task.proxy_alt_id
    except:
        pass
    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_job', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def delete_job(proxyId, url, token):
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_job', task='')
    url = get_url(url)
    url += '/api/{}/jobUpdate/'.format(proxyId)
    head = {'Authorization': 'token {}'.format(token)}

    try:
        response = requests.delete(url, headers=head)
        if response.status_code == 204:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            print(str(response.text))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:delete_job', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def get_job(proxy_pk):
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:get_job', task='')
    url = get_url(proxy.url)
    url += '/api/job/'
    head = {'Authorization': 'token {}'.format(proxy.token)}

    try:
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            jsonjo = json.loads(response.text)
            if jsonjo.__len__()>0:
                for job in jsonjo:
                    joob = Job(workspace=job['workspace'],
                               firs_task=Task.objects.filter(proxy_alt_id=job['firs_task'], proxy=proxy).get(),
                               proxy_alt_id=job['id'],
                               dispositivo=Dispositivo.objects.filter(proxy_alt_id=job['dispositivo'], proxy=proxy).get(),
                               proxy=proxy)
                    joob.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:get_job', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_task(task_pk, proxy_pk):
    task = Task.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_task', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['tipo']=task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()


    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_task(task_pk, proxy_pk):
    task = Task.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_task', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def delete_task(task_pk, proxy_pk):
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:delete_task', task='')
    url = get_url(proxy.url)
    url += '/api/{}/taskUpdate/'.format(task_pk)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    try:
        response = requests.delete(url, headers=head)
        if response.status_code == 204:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:delete_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_sensor_string(task_pk, proxy_pk):
    task = If_sensor_string.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_sensor_string', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'+response.text
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_sensor_string(task_pk, proxy_pk):
    task = If_sensor_string.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_sensor_string', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}
    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404' + response.text
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_sensor_boolean(task_pk, proxy_pk):
    task = If_sensor_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_sensor_boolean', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_sensor_boolean(task_pk, proxy_pk):
    task = If_sensor_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_sensor_boolean', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_sensor_numero(task_pk, proxy_pk):
    task = If_sensor_numero.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_sensor_numero', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_sensor_numero(task_pk, proxy_pk):
    task = If_sensor_numero.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_sensor_numero', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_sensor_dadosensor(task_pk, proxy_pk):
    task = If_sensor_dadosensor.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_sensor_dadosensor', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor.proxy_alt_id
    data['tipo'] = task.tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_sensor_dadosensor(task_pk, proxy_pk):
    task = If_sensor_dadosensor.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_sensor_dadosensor', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_atuador_boolean(task_pk, proxy_pk):
    task = Atuador_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_atuador_boolean', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['estado']=task.estado
    data['atuador'] = task.atuador.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_atuador_boolean(task_pk, proxy_pk):
    task = Atuador_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_atuador_boolean', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['estado']=task.estado
    data['atuador'] = task.atuador.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            print(response.text)
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_atuador_troca_estado(task_pk, proxy_pk):
    print(task_pk)
    task = Atuador_troca_estado.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_atuador_troca_estado', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['estado_atual'] = task.estado_atual
    data['estado_anterior'] = task.estado_anterior
    data['atuador'] = task.atuador.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            print(str(response.text))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_atuador_troca_estado(task_pk, proxy_pk):
    print(task_pk)
    task = Atuador_troca_estado.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_atuador_troca_estado', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['estado_atual'] = task.estado_atual
    data['estado_anterior'] = task.estado_anterior
    data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    data['atuador'] = task.atuador.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            print(str(response.text))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_else_sensor_dadosensor(task_pk, proxy_pk):
    task = If_else_sensor_dadosensor.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_else_sensor_dadosensor', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor.proxy_alt_id
    data['tipo'] = task.tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_else_sensor_dadosensor(task_pk, proxy_pk):
    task = If_else_sensor_dadosensor.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_else_sensor_dadosensor', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando

    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    if task.elsetask != None:
        while task.elsetask.proxy_alt_id == None:
            task.refresh_from_db()
        data['elsetask'] = task.task_sucessor.proxy_alt_id

    data['condicao']=task.condicao
    data['valor'] = task.valor.proxy_alt_id
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_else_sensor_string(task_pk, proxy_pk):
    task = If_else_sensor_string.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_else_sensor_string', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    print(url)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'+response.text
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_else_sensor_string(task_pk, proxy_pk):
    task = If_else_sensor_string.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_else_sensor_string', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}
    print(url)
    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    if task.elsetask != None:
        while task.elsetask.proxy_alt_id == None:
            task.refresh_from_db()
        data['elsetask'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404' + response.text
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_else_sensor_boolean(task_pk, proxy_pk):
    task = If_else_sensor_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_else_sensor_boolean', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_else_sensor_boolean(task_pk, proxy_pk):
    task = If_else_sensor_boolean.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_else_sensor_boolean', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    if task.elsetask != None:
        while task.elsetask.proxy_alt_id == None:
            task.refresh_from_db()
        data['elsetask'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def create_if_else_sensor_numero(task_pk, proxy_pk):
    task = If_else_sensor_numero.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:create_if_else_sensor_numero', task='')
    url = get_url(proxy.url)
    url += task.tipo.url_create
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 201:
            jsondis = json.loads(response.text)
            task.proxy_alt_id = jsondis['id']
            task.save()
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


@app.task
def edit_if_else_sensor_numero(task_pk, proxy_pk):
    task = If_else_sensor_numero.objects.get(pk=task_pk)
    proxy = Proxy.objects.get(pk=proxy_pk)
    celery = Celery(app='ProxyManagerWeb:tarefa:edit_if_else_sensor_numero', task='')
    url = get_url(proxy.url)
    while task.proxy_alt_id == None:
        task.refresh_from_db()
    url += task.tipo.url_update.format(task.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(proxy.token)}

    data = {}
    data['comando'] = task.comando
    if task.task_anterior != None:
        while task.task_anterior.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_anterior'] = task.task_anterior.proxy_alt_id
    if task.task_sucessor != None:
        while task.task_sucessor.proxy_alt_id == None:
            task.refresh_from_db()
        data['task_sucessor'] = task.task_sucessor.proxy_alt_id
    if task.elsetask != None:
        while task.elsetask.proxy_alt_id == None:
            task.refresh_from_db()
        data['elsetask'] = task.task_sucessor.proxy_alt_id
    data['condicao']=task.condicao
    data['valor'] = task.valor
    data['tipo'] = task.tipo.task_tipo

    try:
        response = requests.put(url, json=data, headers=head)
        if response.status_code == 200:
            celery.desc = 'Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Não Respondeu: 404'
            celery.save()
        else:
            print('Não Respondeu: {}'.format(str(response.status_code)))
            celery.desc = 'Não Respondeu: {}'.format(str(response.status_code))
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:create_task', desc='erro',
                        exception=e, task='')
        celery.save()


def get_url(url):
    if "http://" not in url:
       return 'http://'+url
    else:
        return url
