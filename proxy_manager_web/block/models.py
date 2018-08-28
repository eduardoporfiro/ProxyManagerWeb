from core.models import *
from django.conf import settings
from django.db import models

class Proxy(models.Model):
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    def __str__(self):
        return self.name

class Broker(AbstractBroker):
    name = models.CharField(max_length=100, blank=True)
    proxy = models.OneToOneField(Proxy, on_delete=models.CASCADE, related_name='broker')
    def __str__(self):
        return self.name


class Mqtt(AbstractMqtt):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='mqtt')
    def __str__(self):
        return self.topico

class Dado(AbstractDado):
    mqtt = models.ForeignKey(Mqtt, on_delete=models.CASCADE, editable=False, related_name='dado')

