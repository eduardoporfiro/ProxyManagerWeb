from celery.utils.log import get_task_logger
from proxy_manager_web.celery import app

from tarefa.models import Dispositivo
from core.models import Celery
import requests, json

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
            celery.desc = 'Respondeu'
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
        if response.status_code == 200:
            celery.desc = 'Respondeu e delete'
            celery.save()
        else:
            celery.desc = 'delete não foi completo'
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:tarefa:delete_dispo', desc='erro',
                        exception=e, task='')
        celery.save()


def get_url(url):
    if "http://" not in url:
       return 'http://'+url
    else:
        return url