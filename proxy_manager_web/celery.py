import os
from celery import Celery
import dj_database_url

DEFAULT_AMQP = "amqp://guest:guest@localhost//"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxy_manager_web.settings')

app = Celery('proxy_manager_web',
             broker='amqp://kljpxmmt:8DOmdw2f5qzc-QshcdMXN1orLt7F_vpu@woodpecker.rmq.cloudamqp.com/kljpxmmt')
app.BROKER_POOL_LIMIT = 1
#app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()