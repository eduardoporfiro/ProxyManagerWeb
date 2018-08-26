from core.models import *
from django.contrib.auth.models import User
from django.db import models

class Broker(AbstractBroker):
    def __str__(self):
        return self.endereco


class Mqtt(AbstractMqtt):
    broker = models.ForeignKey(Broker, on_delete=True)
    def __str__(self):
        return self.topico

class Dado(AbstractDado):
    mqtt = models.ForeignKey(Mqtt, on_delete=models.CASCADE, editable=False)
