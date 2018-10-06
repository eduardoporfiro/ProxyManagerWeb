from celery.utils.log import get_task_logger
from proxy_manager_web.celery import app
from django.core.serializers import serialize

from block.models import Broker, Proxy
import requests, json
from requests.auth import HTTPBasicAuth

logger = get_task_logger(__name__)

def get_broker(proxy):
    url = get_url(proxy.url)
    url += '/api/broker/'
    head = {'Authorization': 'token {}'.format(proxy.token)}
    print(head)
    try:
        response = requests.get(url, head=head)
        if (response.status_code == 200):
            print("Respondeu Broker")
            brokerjson = json.loads(response.text)[0]
            #save_broker(broker, brokerjson)
            print(brokerjson)
        else:
            print("TESTE")
    except:
        print("Erro Broker")

@app.task
def conect_proxy(proxy):
    proxy = Proxy.objects.get(pk=proxy)
    data={}
    data['username']=proxy.username
    data['password']=proxy.password
    url = get_url(proxy.url)
    url+='/api/api-token-auth/'
    try:
        response = requests.post(url,json=data)
        if (response.status_code == 200):
            print("Respondeu")
            proxy.status = 1  # conectado com token
            proxy.token = json.loads(response.text)['token']
            print(proxy.token)
            print(json.loads(response.text)['token'])
            if proxy.broker:
                get_broker(proxy)
            else:
                proxy.broker = Broker()
                proxy.save()
                get_broker(proxy)
        elif (response.status_code == 404):
            print("Deu pau")
            proxy.status = 4  # não existe
            proxy.token = ''
            proxy.save()
        elif (response.status_code == 400):
            proxy.status = 2  # erro
            proxy.token = ''
            proxy.save()

    except:
        proxy.status = 2  # erro
        proxy.token = ''
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
            if (response.status_code == 200):
                print("Respondeu")

            elif (response.status_code == 404):
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
        broker.save()
