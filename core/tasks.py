from proxy_manager_web.celery import app
from block.models import Mqtt,Proxy, Broker
from tarefa.models import *
import requests, json
from block import task as block_task

@app.task
def update_data():
    proxys = Proxy.objects.all()
    for proxy in proxys:
        if proxy.token is not None:
            tenta_conectar(proxy)
            if proxy.valido:
                if proxy.proxy_dado == 0:#copiar a partir do Proxy
                    diff_broker(proxy)
                    diff_mqtt(proxy)
                    diff_dispo(proxy)
                    diff_task(proxy)
                    diff_job(proxy)
                else:
                    print('sem espelho')
            else:
                block_task.conect_proxy(proxy.pk)
        else:
            block_task.conect_proxy(proxy=proxy.pk)


def diff_task(proxy):
    tasks = Task.objects.filter(proxy=proxy).all()
    tasks.delete()
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=0)
    url = get_url(proxy.url)
    url += setting.url_create

    datatask={}

    diff_If_sensor_string(proxy, datatask)
    diff_If_sensor_numero(proxy, datatask)
    diff_If_sensor_boolean(proxy, datatask)
    diff_If_sensor_dadosensor(proxy, datatask)
    diff_Atuador_troca_estado(proxy, datatask)
    diff_Atuador_boolean(proxy, datatask)

    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    if data['tipo'] in (0, 1, 2, 3, 4, 5):
                        task = Task()
                        task.comando = data['comando']
                        task.proxy_alt_id = data['id']
                        task.proxy = proxy
                        task.tipo = Settings.objects.get(task_tipo=data['tipo'])
                        task.save()
                        datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior']}

    except:
        pass
    atualiza_referencia(proxy, datatask)


def atualiza_referencia(proxy, datatask):
    tasks = Task.objects.filter(proxy=proxy).all()
    try:
        for task in tasks:
            if task.tipo.task_tipo in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                dados = datatask[task.pk]
                if dados['sucessor'] is not None:
                    task.task_sucessor = Task.objects.filter(proxy_alt_id=dados['sucessor'], proxy=proxy).get()
                if dados['anterior'] is not None:
                    task.task_anterior = Task.objects.filter(proxy_alt_id=dados['anterior'], proxy=proxy).get()
                task.save()

            elif task.tipo.task_tipo == 9:
                dados = datatask[task.pk]
                task = If_sensor_dadosensor.objects.get(pk=task.pk)
                if dados['sucessor'] is not None:
                    task.task_sucessor = Task.objects.filter(proxy_alt_id=dados['sucessor'], proxy=proxy).get()
                if dados['anterior'] is not None:
                    task.task_anterior = Task.objects.filter(proxy_alt_id=dados['anterior'], proxy=proxy).get()
                if dados['task'] is not None:
                    task.valor = Task.objects.get(proxy_alt_id=dados['task'])
                task.save()

            elif task.tipo.task_tipo == 10:
                dados = datatask[task.pk]
                task = Atuador_troca_estado.objects.get(pk=task.pk)
                if dados['sucessor'] is not None:
                    task.task_sucessor = Task.objects.filter(proxy_alt_id=dados['sucessor'], proxy=proxy).get()
                if dados['anterior'] is not None:
                    task.task_anterior = Task.objects.filter(proxy_alt_id=dados['anterior'], proxy=proxy).get()
                if dados['atuador'] is not None:
                    task.atuador = Dispositivo.objects.get(proxy_alt_id=dados['atuador'], proxy=proxy)
                task.save()
            elif task.tipo.task_tipo == 11:
                dados = datatask[task.pk]
                task = Atuador_boolean.objects.get(pk=task.pk)
                if dados['sucessor'] is not None:
                    task.task_sucessor = Task.objects.filter(proxy_alt_id=dados['sucessor'], proxy=proxy).get()
                if dados['anterior'] is not None:
                    task.task_anterior = Task.objects.filter(proxy_alt_id=dados['anterior'], proxy=proxy).get()
                if dados['atuador'] is not None:
                    task.atuador = Dispositivo.objects.get(proxy_alt_id=dados['atuador'], proxy=proxy)
                task.save()

    except Exception as e:
        print('REFERENCIA')
        print(e)


def diff_If_sensor_string(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=6)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = If_sensor_string()
                    task.comando = data['comando']
                    task.condicao = data['condicao']
                    task.valor = data['valor']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor' : data['task_sucessor'], 'anterior': data['task_anterior']}
    except:
        pass


def diff_If_sensor_numero(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=7)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = If_sensor_numero()
                    task.comando = data['comando']
                    task.condicao = data['condicao']
                    task.valor = data['valor']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior']}

    except:
        pass


def diff_If_sensor_boolean(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=8)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = If_sensor_boolean()
                    task.comando = data['comando']
                    task.condicao = data['condicao']
                    task.valor = data['valor']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior']}

    except:
        pass


def diff_If_sensor_dadosensor(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=9)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = If_sensor_dadosensor()
                    task.comando = data['comando']
                    task.condicao = data['condicao']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior'],
                                         'task' : data['valor']}
                    print(datatask)

    except:
        pass


def diff_Atuador_troca_estado(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=10)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = Atuador_troca_estado()
                    task.comando = data['comando']
                    task.estado_atual = data['estado_atual']
                    task.estado_anterior = data['estado_anterior']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior'],
                                         'atuador': data['atuador']}

    except:
        pass


def diff_Atuador_boolean(proxy, datatask):
    head = {'Authorization': 'token {}'.format(proxy.token)}
    setting = Settings.objects.get(task_tipo=11)
    url = get_url(proxy.url)
    url += setting.url_create
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jsoon = json.loads(response.text)
            if jsoon.__len__() > 0:
                for data in jsoon:
                    task = Atuador_boolean()
                    task.comando = data['comando']
                    task.estado = data['estado']
                    task.proxy_alt_id = data['id']
                    task.proxy = proxy
                    task.tipo = setting
                    task.save()
                    datatask[task.pk] = {'sucessor': data['task_sucessor'], 'anterior': data['task_anterior'],
                                         'atuador': data['atuador']}

    except:
        pass


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
                    dispo.nome = dispoJson['nome']
                    dispo.tipo = dispoJson['tipo']
                    dispo.is_int = dispoJson['is_int']
                    dispo.mqtt = Mqtt.objects.filter(proxy_alt_id=dispoJson['mqtt']).get()
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


def diff_job(proxy):
    jobs = Job.objects.filter(proxy=proxy).all()
    head = {'Authorization': 'token {}'.format(proxy.token)}
    # verifica os existentes
    for job in jobs:
        url = get_url(proxy.url)
        url += '/api/job/?id={}'.format(job.proxy_alt_id)
        try:
            response = requests.get(url=url, headers=head)
            if response.status_code == 200:
                jobJson = json.loads(response.text)
                if jobJson.__len__() > 0:
                    jobJson = jobJson[0]
                    job.workspace = jobJson['workspace']
                    job.last_update = jobJson['last_update']
                    job.dispositivo = Dispositivo.objects.filter(proxy_alt_id=jobJson['dispositivo']).get()
                    job.firs_task = Task.objects.filter(proxy_alt_id=jobJson['firs_task']).get()
                    job.save()
        except:
            pass

    url = get_url(proxy.url)
    url += '/api/job/'
    # atualiza com novos valores
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            jobJson = json.loads(response.text)
            if jobJson.__len__() != 0:
                for jobson in jobJson:
                    if Job.objects.filter(proxy_alt_id=jobson['id'], proxy=proxy).exists() == False:
                        job = Job(workspace=jobson['workspace'],
                                  last_update=jobson['last_update'],
                                  firs_task=Task.objects.filter(proxy_alt_id=jobson['firs_task'], proxy=proxy).get(),
                                  dispositivo=Dispositivo.objects.filter(proxy_alt_id=jobson['dispositivo'], proxy=proxy).get(),
                                  proxy_alt_id=jobson['id'],
                                  proxy=proxy)
                        job.save()
    except Exception as e:
        print(e)


def diff_broker(proxy):
    broker = Broker.objects.filter(proxy=proxy).get()
    url=get_url(proxy.url)
    url+= '/api/broker/'
    head = {'Authorization': 'token {}'.format(broker.proxy.token)}
    try:
        response = requests.get(url=url, headers=head)
        if response.status_code == 200:
            brokerJson = json.loads(response.text)[0]
            broker.proxy_alt_id = brokerJson['id']
            broker.username = brokerJson['username']
            broker.password = brokerJson['password']
            broker.endereco = brokerJson['endereco']
            broker.estado = brokerJson['estado']
            broker.porta = brokerJson['porta']
            broker.RC = brokerJson['RC']
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
        url = get_url(proxy.url)
        url += '/api/mqtt/?id={}'.format(mqtt.proxy_alt_id)

        try:
            response = requests.get(url=url, headers=head)
            if response.status_code == 200:
                mqttJson = json.loads(response.text)
                if mqttJson.__len__() != 0:
                    mqttJson = mqttJson[0]
                    mqtt.topico = mqttJson['topico']
                    mqtt.QoS = mqttJson['QoS']
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
    proxy.valido = boo
    proxy.save()
