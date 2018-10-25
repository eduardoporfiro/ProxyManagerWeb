from proxy_manager_web.celery import app
from block.models import Mqtt,Proxy, Broker
from tarefa.models import Dispositivo, Task
import requests, json
from block import task as block_task

@app.task
def update_data():
    proxys = Proxy.objects.all()
    for proxy in proxys:
        if proxy.token is not None:
            tenta_conectar(proxy)
            if proxy.valido:
                print('é valido')
                if proxy.proxy_dado == 0:#copiar a partir do Proxy
                    diff_broker(proxy)
                    diff_mqtt(proxy)
                    diff_dispo(proxy)
                else:
                    print('sem espelho')
            else:
                print('inválido')
                block_task.conect_proxy(proxy.pk)
        else:
            block_task.conect_proxy(proxy=proxy.pk)


def diff_task(proxy):
    tasks = Task.objects.filter(proxy=proxy).all()
    head = {'Authorization': 'token {}'.format(proxy.token)}


def diff_dispo(proxy):
    dispos = Dispositivo.objects.filter(proxy=proxy).all()
    head = {'Authorization': 'token {}'.format(proxy.token)}
    #verifica os existentes
    for dispo in dispos:
        url=get_url(proxy.url)
        url+='/api/dispositivo/?id={}'.format(dispo.proxy_alt_id)
        try:
            response = requests.get(url=url, headers=head)
            if response.status_code == 200:
                dispoJson = json.loads(response.text)
                if dispoJson.__len__() >0:
                    dispoJson = dispoJson[0]
                    dispo.nome=dispoJson['nome']
                    dispo.tipo=dispoJson['tipo']
                    dispo.is_int=dispoJson['is_int']
                    dispo.mqtt=Mqtt.objects.filter(proxy_alt_id=dispoJson['mqtt']).get()
                    dispo.save()
        except:
            pass
    url = get_url(proxy.url)
    url += '/api/dispositivo/'
    # atualiza com novos valores
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            dispoJson = json.loads(response.text)
            if dispoJson.__len__() != 0:
                for disposon in dispoJson:
                    if Dispositivo.objects.filter(proxy_alt_id=disposon['id'], proxy=proxy).exists() == False:
                        dispo = Dispositivo(nome=disposon['nome'],
                                    tipo=disposon['tipo'],
                                    is_int=disposon['is_int'],
                                    mqtt=Mqtt.objects.filter(proxy_alt_id=disposon['mqtt'], proxy=proxy).get(),
                                    proxy=proxy,
                                    proxy_alt_id=disposon['id'])
                        dispo.save()
    except Exception as e:
        print(e)


def diff_broker(proxy):
    broker = Broker.objects.filter(proxy=proxy).get()
    url=get_url(proxy.url)
    url+= 'api/broker/'
    head = {'Authorization': 'token {}'.format(broker.proxy.token)}
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            brokerJson = json.loads(response.text)[0]
            broker.proxy_alt_id=brokerJson['id']
            broker.username=brokerJson['username']
            broker.password=brokerJson['password']
            broker.endereco=brokerJson['endereco']
            broker.estado=brokerJson['estado']
            broker.porta=brokerJson['porta']
            broker.save()
        else:
            proxy_valido(proxy, False)
    except:
        proxy_valido(proxy, False)


def diff_mqtt(proxy):
    mqtts = Mqtt.objects.filter(proxy=proxy).all()
    head = {'Authorization': 'token {}'.format(proxy.token)}
    #verfica os que ja temos aqui
    for mqtt in mqtts:
        url=get_url(proxy.url)
        url+='/api/mqtt/?id={}'.format(mqtt.proxy_alt_id)

        try:
            response = requests.get(url=url, headers=head)
            if response.status_code == 200:
                mqttJson = json.loads(response.text)
                if mqttJson.__len__() != 0:
                    mqttJson=mqttJson[0]
                    mqtt.topico=mqttJson['topico']
                    mqtt.QoS=mqttJson['QoS']
                    mqtt.save()
        except:
            pass
    url = get_url(proxy.url)
    url += '/api/mqtt/'
    try:#atualiza com novos valores
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            mqttJson = json.loads(response.text)
            if mqttJson.__len__() != 0:
                for mqttson in mqttJson:
                    if Mqtt.objects.filter(proxy_alt_id=mqttson['id'], proxy=proxy).exists() == False:
                        mqtt = Mqtt(topico=mqttson['topico'],
                                    QoS=mqttson['QoS'],
                                    proxy=proxy,
                                    broker=proxy.broker,
                                    proxy_alt_id=mqttson['id'])
                        mqtt.save()
    except:
        pass


def tenta_conectar(proxy):
    data = {}
    data['username'] = proxy.username
    data['password'] = proxy.password
    url = get_url(proxy.url)
    url += '/api-token-auth/'
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            proxy_valido(proxy, True)
        else:
            proxy_valido(proxy, False)
    except:
        proxy_valido(proxy, False)


def get_url(url):
    if "http://" not in url:
       return 'http://'+url
    else:
        return url

def proxy_valido(proxy, boo):
    proxy.valido=boo
    proxy.save()