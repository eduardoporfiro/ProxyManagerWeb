import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxy_manager_web.settings')

app = Celery('proxy_manager_web')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
app.autodiscover_tasks()
