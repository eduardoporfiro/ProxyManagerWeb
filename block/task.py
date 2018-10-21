from celery.utils.log import get_task_logger
from proxy_manager_web.celery import app

from block.models import Broker, Proxy, Mqtt
from tarefa.models import Dispositivo
from core.models import Celery
import requests, json

logger = get_task_logger(__name__)


def get_dispositivo(proxy):
    celery = Celery(app='ProxyManagerWeb:block:conect_proxy', task='get_dispositivo')
    url = get_url(proxy.url)
    url += '/api/dispositivo/'
    head = {'Authorization': 'token {}'.format(proxy.token)}
    try:
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            jsondispo = json.loads(response.text)
            for jsons in jsondispo:
                mqtt = Mqtt.objects.get(proxy_alt_id=jsons['mqtt'], proxy=proxy)
                dispositivo = Dispositivo.objects.filter(proxy=proxy, mqtt=mqtt).exists()
                if dispositivo is False:
                    dispo = Dispositivo(mqtt=mqtt, proxy=proxy,
                                              tipo=jsons['tipo'], is_int=jsons['is_int'],
                                              nome=jsons['nome'], proxy_alt_id=jsons['id'])
                    dispo.save()
                else:
                    dispositivo = Dispositivo.objects.filter(proxy=proxy, mqtt=mqtt).first()
                    dispositivo.nome=jsons['nome']
                    dispositivo.tipo=jsons['tipo']
                    dispositivo.is_int=jsons['is_int']
                    dispositivo.proxy_alt_id=jsons['id']
                    dispositivo.save()
        elif response.status_code == 404:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()

        elif response.status_code == 400:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()
    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:conect_proxy', desc='get_dispositivo',
                        exception=e, task='get_dispositivo')
        celery.save()


def get_mqtt(proxy):
    celery = Celery(app='ProxyManagerWeb:block:conect_proxy', task='get_mqtt')
    url = get_url(proxy.url)
    url += '/api/mqtt/'
    head = {'Authorization': 'token {}'.format(proxy.token)}
    try:
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            mqttjson = json.loads(response.text)
            for jsons in mqttjson:
                mqtts = Mqtt.objects.filter(topico=jsons['topico'], proxy=proxy).exists()
                if mqtts is False:
                    mqtt = Mqtt(topico=jsons['topico'],broker=proxy.broker,proxy=proxy,QoS=jsons['QoS'],
                                proxy_alt_id=jsons['id'])
                    mqtt.save()
                else:
                    mqtts = Mqtt.objects.filter(topico=jsons['topico'], proxy=proxy)
                    for mqtt in mqtts:
                        mqtt.topico=jsons['topico']
                        mqtt.QoS=jsons['QoS']
                        mqtt.proxy_alt_id=jsons['id']
                        mqtt.save()
        elif response.status_code == 404:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()

        elif response.status_code == 400:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:conect_proxy', desc='get_mqtt',
                        exception=e, task='get_mqtt')
        celery.save()


def get_broker(proxy):
    celery = Celery(app='ProxyManagerWeb:block:conect_proxy', task='get_broker')
    url = get_url(proxy.url)
    url += '/api/broker/'
    head = {'Authorization': 'token {}'.format(proxy.token)}
    try:
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            brokerjson = json.loads(response.text)[0]
            try:
                broker = proxy.broker
            except:
                broker = Broker()
            broker = save_broker(broker, brokerjson)
            proxy.broker = broker
            proxy.save()
            broker.save()

        elif response.status_code == 404:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()
        elif response.status_code == 400:
            celery.desc = 'Proxy não respondeu'
            celery.exception = response.text
            celery.save()
    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:conect_proxy', desc='Get Broker',
                        exception=e, task='get_broker')
        celery.save()


@app.task
def conect_proxy(proxy):
    celery = Celery(app='ProxyManagerWeb:block', task='conect_proxy')
    proxy = Proxy.objects.get(pk=proxy)
    data = {}
    data['username']=proxy.username
    data['password']=proxy.password
    url = get_url(proxy.url)
    url += '/api-token-auth/'
    try:
        response = requests.post(url,json=data)
        if response.status_code == 200:
            celery.desc='Proxy Respondeu'
            celery.save()
            proxy.status = 1  # conectado com token
            proxy.token = json.loads(response.text)['token']
            proxy.save()
            get_broker(proxy)
            get_mqtt(proxy)
            get_dispositivo(proxy)
        elif response.status_code == 404:
            celery.desc = 'Proxy não respondeu Respondeu'
            #celery.exception = response.text
            celery.save()
            proxy.status = 4  # não existe
            proxy.token = ''
            proxy.save()
        elif response.status_code == 400:
            proxy.status = 2  # erro
            celery.desc = 'Proxy não respondeu Respondeu'
            celery.exception = response.text
            celery.save()
            proxy.token = ''
            proxy.save()

    except Exception as e:
        proxy.status = 2  # erro
        proxy.token = ''
        celery = Celery(app='ProxyManagerWeb:block', desc='Criar conexão Proxy',
                        exception=e, task='conect_proxy')
        celery.save()
        print(e)
        proxy.save()


@app.task
def create_broker(broker_id):
    broker = Broker.objects.get(pk=broker_id)
    if broker.proxy.token:
        url = get_url(broker.proxy.url)
        url+='/api/brokerUpdate/1/'
        data={}
        data['endereco']=broker.endereco
        data['porta'] = broker.porta
        data['username'] = broker.username
        data['password'] = broker.password
        head= {'Authorization':'token {}'.format(broker.proxy.token)}
        try:
            response = requests.put(url, json=data, headers=head)
            if response.status_code == 200:
                brokerjson=json.loads(response.text)
                broker.proxy_alt_id=brokerjson['id']
                broker.save()
                print("Respondeu")

            elif response.status_code == 404:
                print("Deu pau")
        except:
            print("ERRO GERAL")


def get_url(url):
    if "http://" not in url:
       return 'http://'+url
    else:
        return url


def save_broker(broker, brokerjson):
    if broker != None:
        broker.password = brokerjson["password"]
        broker.username = brokerjson["username"]
        broker.estado = brokerjson["estado"]
        broker.porta = brokerjson["porta"]
        broker.endereco = brokerjson["endereco"]
        broker.proxy_alt_id = brokerjson["id"]
        return broker


@app.task
def create_mqtt(mqtt_id):
    mqtt = Mqtt.objects.get(pk=mqtt_id)
    celery = Celery(app='ProxyManagerWeb:block:create_mqtt', task='')
    url = get_url(mqtt.proxy.url)
    url += '/api/mqtt/'
    head = {'Authorization': 'token {}'.format(mqtt.proxy.token)}

    data={}
    data['topico']=mqtt.topico
    data['QoS'] = mqtt.QoS
    data['broker'] = '1'
    try:
        response = requests.post(url, json=data, headers=head)
        if response.status_code == 200:
            mqttjson = json.loads(response.text)
            mqtt.proxy_alt_id=mqttjson['id']
            mqtt.save()
            celery.desc='Respondeu'
            celery.save()

        elif response.status_code == 404:
            celery.desc = 'Respondeu'
            celery.save()

    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:conect_proxy', desc='get_mqtt',
                        exception=e, task='get_mqtt')
        celery.save()


@app.task
def update_mqtt(mqtt_pk):
    mqtt = Mqtt.objects.get(pk=mqtt_pk)
    celery = Celery(app='ProxyManagerWeb:block:update_mqtt', task='')
    url = get_url(mqtt.proxy.url)
    url += '/api/{}/mqttUpdate/'.format(mqtt.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(mqtt.proxy.token)}

    data = {}
    data['topico'] = mqtt.topico
    data['QoS'] = mqtt.QoS
    data['broker'] = '1'

    try:
        response = requests.put(url,json=data, headers=head)
        if response.status_code == 200:
            celery.desc='Respondeu e Update'
            celery.save()
        else:
            celery.desc = 'Update não foi completo'
            celery.save()
    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:conect_proxy', desc='get_mqtt',
                        exception=e, task='get_mqtt')
        celery.save()


@app.task
def delete_mqtt(mqtt_pk):
    mqtt = Mqtt.objects.get(pk=mqtt_pk)
    celery = Celery(app='ProxyManagerWeb:block:delete_mqtt', task='')
    url = get_url(mqtt.proxy.url)
    url += '/api/{}/mqttUpdate/'.format(mqtt.proxy_alt_id)
    head = {'Authorization': 'token {}'.format(mqtt.proxy.token)}

    try:
        response = requests.delete(url,headers=head)
        if response.status_code == 200:
            celery.desc='Respondeu e delete'
            celery.save()
        else:
            celery.desc = 'delete não foi completo'
            celery.save()
    except Exception as e:
        celery = Celery(app='ProxyManagerWeb:block:delete_mqtt', desc='get_mqtt',
                        exception=e, task='get_mqtt')
        celery.save()
