import os
from celery import Celery
import dj_database_url

DEFAULT_AMQP = "amqp://guest:guest@localhost//"
DEFAULT_DB = "postgres://localhost"
db_url = os.environ.get("DATABASE_URL", DEFAULT_DB)

# Django settings
DATABASES = {"default": dj_database_url.config(default=DEFAULT_DB)}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxy_manager_web.settings')

app = Celery('proxy_manager_web', backend=db_url.replace("postgres://", "db+postgresql://"),
             broker=os.environ.get("CLOUDAMQP_URL", DEFAULT_AMQP))
app.BROKER_POOL_LIMIT = 1
#app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()