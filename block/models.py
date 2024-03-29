from core.models import AbstractMqtt, AbstractBroker
from django.conf import settings
from django.db import models


class Proxy(models.Model):
    status = [
        (0, 'Conectando'),
        (1, 'Conectado'),
        (2, 'ERRO'),
        (3, 'Parado'),
        (4, 'Não Existe'),
    ]

    espelho = [
        (0,'Proxy'),
        (1, 'Local')
    ]
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    token = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(choices=status, default=3)
    valido = models.NullBooleanField()
    proxy_dado = models.IntegerField(choices=espelho, default=0)

    def __str__(self):
        return self.name



class Broker(AbstractBroker):
    name = models.CharField(max_length=100, blank=True)
    proxy = models.OneToOneField(Proxy, on_delete=models.CASCADE, related_name='broker')
    def __str__(self):
        return self.name


class Mqtt(AbstractMqtt):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='mqtt')
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, related_name='mqtt', default=1)
    def __str__(self):
        return self.topico