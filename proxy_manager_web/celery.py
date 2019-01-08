import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxy_manager_web.settings')

app = Celery('proxy_manager_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_data': {
        'task': 'core.tasks.update_data',
        'schedule': crontab(hour=2),
        'args': ''
    },
}
