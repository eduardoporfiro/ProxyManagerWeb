from celery.utils.log import get_task_logger
from proxy_manager_web.celery import app
from block.models import Broker, Proxy
import requests, json

logger = get_task_logger(__name__)

@app.task
def update_broker(broker_id):
    broker = Broker.objects.get(pk=broker_id)
    if broker.proxy.token:
        url = get_url(broker.proxy.url)
        url+='/api/brokerUpdate/1/'
        data={}
        data['endereco']=broker.endereco
        data['porta'] = broker.porta
        data['user'] = broker.username
        data['password'] = broker.password
        head= {'Authorization':'token {}'.format(broker.proxy.token)}
        response = requests.put(url, json=data, headers=head)

@app.task
def conect_proxy(proxy):
    proxy = Proxy.objects.get(pk=proxy)
    data={}
    data['username']=proxy.username
    data['password']=proxy.password
    url = get_url(proxy.url)
    url+='/api/api-token-auth/'
    response = requests.post(url,json=data)
    if (response.status_code == 200):
        print("Respondeu")
        proxy.status=1#conectado com token
        proxy.token = json.loads(response.text)['token']
        proxy.save()
    elif (response.status_code == 404):
        print("Deu pau")
        proxy.status=4#não existe
        proxy.token=''
        proxy.save()
    elif (response.status_code == 400):
        proxy.status=2#erro
        proxy.token = ''
        proxy.save()

def get_url(url):
    if "http://" not in url:
       return 'http://'+url
    else:
        return url
