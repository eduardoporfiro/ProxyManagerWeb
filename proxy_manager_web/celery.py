import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxy_manager_web.settings')

app = Celery('proxy_manager_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()